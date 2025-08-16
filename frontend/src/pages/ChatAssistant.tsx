import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Lightbulb, 
  MessageSquare, 
  Calculator,
  PiggyBank,
  CreditCard,
  Home,
  Briefcase,
  Landmark,
  Bot
} from "lucide-react";
import { cn } from "@/lib/utils";
import { config } from "@/config";

interface Message {
  text: string;
  isAi: boolean;
  timestamp: string;
  isLoading?: boolean;
}

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
    text: "Credit Cards",
    category: "Card Services",
    description: "Discover the perfect credit card for your lifestyle",
    recommendedQueries: [
      "What credit cards would you recommend for me?",
      "Show me the best travel credit cards",
      "Which cards offer maximum cashback?",
      "Compare premium credit cards",
      "Credit cards with lowest annual fees",
      "Show me cards with best reward points",
      "Which cards have good welcome benefits?",
      "Cards with best dining privileges"
    ]
  },
  {
    icon: PiggyBank,
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

interface ChatAssistantProps {
  customerId?: number | null;
}

export default function ChatAssistant({ customerId }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello! I'm your AI financial advisor. I can help you make informed decisions about loans, investments, and your overall financial health. What would you like to know?",
      isAi: true,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<ProductSuite | null>(null);
  
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

  const callChatAPI = async (message: string, customerId: number) => {
    try {
      const response = await fetch(`${config.apiUrl}/customers/${customerId}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: message,
          conversation_history: []
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      // Check if the response contains credit card recommendations
      if (data.response && (
        message.toLowerCase().includes('credit card') ||
        message.toLowerCase().includes('card recommendation') ||
        data.response.toLowerCase().includes('credit card') ||
        data.response.toLowerCase().includes('recommend')
      )) {
        localStorage.setItem(`chatRecommendation_${customerId}`, data.response);
        window.dispatchEvent(new CustomEvent('creditCardRecommendationUpdate', {
          detail: { recommendation: data.response }
        }));
      }

      return data.response;
    } catch (error) {
      console.error('Error calling chat API:', error);
      return 'Sorry, I encountered an error processing your request.';
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!customerId) {
      return;
    }

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
    const aiResponse = await callChatAPI(message, customerId);
    
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

  if (!customerId) {
    return (
      <div className="p-6">
        <Card className="p-8 text-center">
          <div className="flex items-center justify-center mb-4">
            <Bot className="w-12 h-12 text-cyan-500" />
          </div>
          <h2 className="text-xl font-semibold mb-4">AI Chat Assistant</h2>
          <p className="text-gray-600">Please select a customer to start chatting with the AI financial advisor.</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center gap-3">
        <Bot className="w-8 h-8 text-cyan-500" />
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Chat Assistant</h1>
          <p className="text-gray-600">Get personalized financial advice and recommendations</p>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Chat Area */}
        <Card className="lg:col-span-3 overflow-hidden flex flex-col h-[700px]">
          <CardHeader className="border-b">
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              Financial Advisory Chat
            </CardTitle>
          </CardHeader>
          
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4" ref={chatContainerRef}>
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
          
          {/* Suggested Questions */}
          <div className="border-t bg-gray-50">
            <div className="p-4">
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Lightbulb className="w-4 h-4" />
                {selectedProduct ? selectedProduct.text : "Suggested Questions"}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-4">
                {selectedProduct ? (
                  // Show product-specific questions
                  selectedProduct.recommendedQueries.slice(0, 4).map((query, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      className="w-full justify-start text-left h-auto p-2"
                      onClick={() => handleSendMessage(query)}
                    >
                      <MessageSquare className="w-3 h-3 mr-2 flex-shrink-0" />
                      <span className="text-xs">{query}</span>
                    </Button>
                  ))
                ) : (
                  // Show default starter queries
                  starterQueries.slice(0, 4).map((query, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      className="w-full justify-start text-left h-auto p-2"
                      onClick={() => handleSendMessage(query)}
                    >
                      <MessageSquare className="w-3 h-3 mr-2 flex-shrink-0" />
                      <span className="text-xs">{query}</span>
                    </Button>
                  ))
                )}
              </div>
              {selectedProduct && (
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => setSelectedProduct(null)}
                  className="w-full"
                >
                  Back to General Questions
                </Button>
              )}
            </div>
            
            {/* Chat Input */}
            <div className="border-t">
              <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
            </div>
          </div>
        </Card>

        {/* Financial Products Sidebar */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Financial Products</CardTitle>
            <p className="text-sm text-gray-600">Get specialized advice for different financial services</p>
          </CardHeader>
          <CardContent className="p-4">
            <div className="space-y-2">
              {productSuites.map((product, index) => (
                <Button
                  key={index}
                  variant="outline"
                  className={cn(
                    "w-full justify-start text-left h-auto p-3",
                    selectedProduct?.text === product.text && "bg-cyan-50 border-cyan-200"
                  )}
                  onClick={() => handleProductClick(product)}
                >
                  <product.icon className="w-4 h-4 mr-3 flex-shrink-0" />
                  <div className="text-left">
                    <p className="text-sm font-medium">{product.text}</p>
                    <p className="text-xs text-gray-500">{product.category}</p>
                  </div>
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Product Details */}
      {selectedProduct && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <selectedProduct.icon className="w-5 h-5" />
              {selectedProduct.text}
            </CardTitle>
            <p className="text-sm text-gray-600">{selectedProduct.description}</p>
          </CardHeader>
          <CardContent>
            <div>
              <h4 className="font-semibold mb-3">Recommended Questions:</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                {selectedProduct.recommendedQueries.map((query, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    className="justify-start text-left h-auto p-2"
                    onClick={() => handleSendMessage(query)}
                  >
                    <span className="text-xs">{query}</span>
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
