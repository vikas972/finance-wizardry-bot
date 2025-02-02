import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { FinancialMetrics } from "@/components/FinancialMetrics";
import { FinancialCharts } from "@/components/FinancialCharts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Lightbulb, 
  MessageSquare, 
  LayoutDashboard,
  Calculator,
  RefreshCw,
  PiggyBank,
  CreditCard,
  Home,
  Briefcase,
  Landmark
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  text: string;
  isAi: boolean;
  timestamp: string;
  isLoading?: boolean;
}

interface ChatResponse {
  query: string;
  response: string;
  financial_context: any;
}

interface Customer {
  id: number;
  name: string;
  email: string;
}

const API_URL = 'http://localhost:3000';

interface ProductSuite {
  icon: any;
  text: string;
  category: string;
  description: string;
  recommendedQueries: string[];
}

const productSuites: ProductSuite[] = [
  {
    icon: Home,
    text: "Home Loans & Mortgages",
    category: "Property Finance",
    description: "Explore our range of home financing solutions",
    recommendedQueries: [
      "Check home loan eligibility",
      "Current home loan EMI details",
      "Available interest rates",
      "EMI reduction options",
      "Balance transfer benefits"
    ]
  },
  {
    icon: Briefcase,
    text: "Business Banking",
    category: "Corporate Solutions",
    description: "Complete suite of business banking services",
    recommendedQueries: [
      "Business loan eligibility",
      "Current business loan rates",
      "Business credit score",
      "Working capital options",
      "Expansion loan details"
    ]
  },
  {
    icon: CreditCard,
    text: "Personal Banking",
    category: "Retail Banking",
    description: "Day-to-day banking and credit solutions",
    recommendedQueries: [
      "Show my credit score",
      "Monthly spending analysis",
      "Credit utilization",
      "Credit score improvement",
      "Savings optimization"
    ]
  },
  {
    icon: Landmark,
    text: "Wealth Management",
    category: "Investment Services",
    description: "Grow and protect your wealth",
    recommendedQueries: [
      "Investment portfolio summary",
      "Tax saving options",
      "Available tax deductions",
      "Investment suggestions",
      "Returns optimization"
    ]
  },
  {
    icon: Calculator,
    text: "Income Tax Returns",
    category: "Tax Services",
    description: "Tax planning and filing assistance",
    recommendedQueries: [
      "Tax saving analysis",
      "Deductions overview",
      "ITR filing status",
      "Tax liability calculation",
      "Investment proof status"
    ]
  }
];

const starterQueries = [
  "Can I buy a car in Dec 2025?",
  "Should I transfer my home loan?",
  "Monthly retirement savings needed?",
  "Review my spending patterns",
  "How to reduce EMI burden?",
  "Suggest investment options"
];

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello! I'm your AI financial advisor. I can help you make informed decisions about loans, investments, and your overall financial health. What would you like to know?",
      isAi: true,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState<Array<{ role: string; content: string }>>([]);
  const [selectedProduct, setSelectedProduct] = useState<ProductSuite | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState<number | null>(null);
  
  // Add ref for chat container
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Function to scroll to bottom
  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Reset chat when customer changes
  const handleCustomerChange = (customerId: number) => {
    setSelectedCustomerId(customerId);
    // Reset chat to initial state
    setMessages([
      {
        text: "Hello! I'm your AI financial advisor. I can help you make informed decisions about loans, investments, and your overall financial health. What would you like to know?",
        isAi: true,
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
    setConversationHistory([]);
    setSelectedProduct(null);
  };

  // Fetch customers when component mounts
  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch(`${API_URL}/customers/`);
        if (response.ok) {
          const data = await response.json();
          setCustomers(data);
          // Set first customer as default if available
          if (data.length > 0) {
            handleCustomerChange(data[0].id);
          }
        }
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    };
    fetchCustomers();
  }, []);

  const callChatAPI = async (userMessage: string) => {
    if (!selectedCustomerId) {
      return "Please select a customer first.";
    }

    try {
      // First, ensure we have fresh customer data
      const response = await fetch(`${API_URL}/customers/${selectedCustomerId}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage,
          conversation_history: [
            // Only include the last few messages for context, but not too many to avoid confusion
            ...conversationHistory.slice(-4).map(msg => ({
              role: msg.role,
              content: msg.content
            })),
            { role: "user", content: userMessage }
          ]
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('API Error:', errorData);
        throw new Error(errorData.detail || 'API call failed');
      }

      const data: ChatResponse = await response.json();
      
      // Update conversation history with only the latest exchange
      const newHistory = [
        ...conversationHistory.slice(-4), // Keep only last 4 messages for context
        { role: "user", content: userMessage },
        { role: "assistant", content: data.response }
      ];
      setConversationHistory(newHistory);

      return data.response;
    } catch (error) {
      console.error('Error calling chat API:', error);
      return "I apologize, but I'm having trouble accessing the financial data right now. Please try again in a moment.";
    }
  };

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);
    
    // Add user message
    const userMessage = {
      text: message,
      isAi: false,
      timestamp: new Date().toLocaleTimeString(),
    };
    
    // Add loading message
    const loadingMessage = {
      text: "",
      isAi: true,
      timestamp: new Date().toLocaleTimeString(),
      isLoading: true
    };
    
    setMessages(prev => [...prev, userMessage, loadingMessage]);

    // Get AI response
    const aiResponse = await callChatAPI(message);
    
    // Replace loading message with actual response
    const aiMessage = {
      text: aiResponse,
      isAi: true,
      timestamp: new Date().toLocaleTimeString(),
    };
    
    setMessages(prev => prev.slice(0, -1).concat(aiMessage));
    setIsLoading(false);
  };

  const handleProductClick = (product: ProductSuite) => {
    setSelectedProduct(product);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">AI Financial Advisor</h1>
          <div className="flex items-center gap-4">
            <select
              className="p-2 border rounded-md"
              value={selectedCustomerId || ''}
              onChange={(e) => handleCustomerChange(Number(e.target.value))}
            >
              <option value="">Select Customer</option>
              {customers.map(customer => (
                <option key={customer.id} value={customer.id}>
                  {customer.name} ({customer.email})
                </option>
              ))}
            </select>
          </div>
        </div>

        {selectedCustomerId ? (
          <Tabs defaultValue="dashboard" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8">
              <TabsTrigger value="dashboard" className="flex items-center gap-2">
                <LayoutDashboard className="w-4 h-4" />
                Dashboard
              </TabsTrigger>
              <TabsTrigger value="chat" className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4" />
                Chat Assistant
              </TabsTrigger>
            </TabsList>

            <TabsContent value="dashboard" className="space-y-8">
              <FinancialMetrics customerId={selectedCustomerId!} />
              <FinancialCharts />
            </TabsContent>

            <TabsContent value="chat">
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                <Card className="lg:col-span-3 overflow-hidden flex flex-col h-[600px]">
                  <div className="flex-1 overflow-y-auto" ref={chatContainerRef}>
                    {messages.map((message, index) => (
                      <ChatMessage
                        key={index}
                        message={message.text}
                        isAi={message.isAi}
                        timestamp={message.timestamp}
                        isLoading={message.isLoading}
                      />
                    ))}
                  </div>
                  <div className="border-t">
                    <div className="p-4 bg-accent/50">
                      <h3 className="font-semibold mb-2 flex items-center gap-2">
                        <Lightbulb className="w-4 h-4" />
                        {selectedProduct ? selectedProduct.text : "Suggested Questions"}
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {selectedProduct ? (
                          // Show product-specific questions
                          selectedProduct.recommendedQueries.map((query, index) => (
                            <Button
                              key={index}
                              variant="outline"
                              className="w-full justify-start text-left"
                              onClick={() => handleSendMessage(query)}
                            >
                              <MessageSquare className="w-4 h-4 mr-2" />
                              <div>
                                <p className="text-sm font-medium">{query}</p>
                              </div>
                            </Button>
                          ))
                        ) : (
                          // Show default starter queries
                          starterQueries.map((query, index) => (
                            <Button
                              key={index}
                              variant="outline"
                              className="w-full justify-start text-left"
                              onClick={() => handleSendMessage(query)}
                            >
                              <MessageSquare className="w-4 h-4 mr-2" />
                              <div>
                                <p className="text-sm font-medium">{query}</p>
                              </div>
                            </Button>
                          ))
                        )}
                      </div>
                      {selectedProduct && (
                        <Button
                          className="mt-4 w-full"
                          variant="secondary"
                          onClick={() => setSelectedProduct(null)}
                        >
                          Back to Suggested Questions
                        </Button>
                      )}
                    </div>
                    <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
                  </div>
                </Card>

                <Card className="p-4">
                  <h3 className="font-semibold mb-4">Financial Products</h3>
                  <div className="space-y-2">
                    {productSuites.map((product, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        className={cn(
                          "w-full justify-start text-left",
                          selectedProduct?.text === product.text && "bg-accent"
                        )}
                        onClick={() => handleProductClick(product)}
                      >
                        <product.icon className="w-4 h-4 mr-2" />
                        <div>
                          <p className="text-sm font-medium">{product.text}</p>
                          <p className="text-xs text-muted-foreground">{product.category}</p>
                        </div>
                      </Button>
                    ))}
                  </div>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        ) : (
          <Card className="p-8 text-center">
            <h2 className="text-xl font-semibold mb-4">Welcome to AI Financial Advisor</h2>
            <p className="text-muted-foreground">Please select a customer to continue.</p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Index;