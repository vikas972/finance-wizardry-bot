import { useState } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { FinancialMetrics } from "@/components/FinancialMetrics";
import { Card } from "@/components/ui/card";

interface Message {
  text: string;
  isAi: boolean;
  timestamp: string;
}

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello! I'm your AI financial advisor. I can help you make informed decisions about loans, investments, and your overall financial health. What would you like to know?",
      isAi: true,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const mockAiResponse = async (userMessage: string) => {
    // Simulate AI processing
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1500));

    let response = "";
    if (userMessage.toLowerCase().includes("car")) {
      response = "Based on your current financial profile:\n\n" +
        "- Monthly Income: ₹85,000\n" +
        "- Current EMIs: ₹25,000\n" +
        "- Credit Score: 750\n\n" +
        "You could potentially afford a car loan of up to ₹8,00,000 with an EMI of ₹15,000. However, I recommend keeping your total EMIs under 40% of your income. Would you like to explore specific car loan options?";
    } else if (userMessage.toLowerCase().includes("home loan")) {
      response = "I've analyzed your home loan situation:\n\n" +
        "Current interest rate: 8.5%\n" +
        "Available rates in market: Starting from 7.2%\n\n" +
        "A balance transfer could save you approximately ₹2,500 per month. Would you like me to show you detailed calculations and top lender options?";
    } else {
      response = "I understand you're asking about your finances. Could you please provide more specific details about what you'd like to know? I can help with:\n\n" +
        "- Loan affordability calculations\n" +
        "- Investment recommendations\n" +
        "- Savings strategies\n" +
        "- Debt management advice";
    }

    setMessages(prev => [...prev, {
      text: response,
      isAi: true,
      timestamp: new Date().toLocaleTimeString(),
    }]);
    setIsLoading(false);
  };

  const handleSendMessage = async (message: string) => {
    const newMessage = {
      text: message,
      isAi: false,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages(prev => [...prev, newMessage]);
    await mockAiResponse(message);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8">
        <h1 className="text-4xl font-bold text-center mb-8">AI Financial Advisor</h1>
        
        <FinancialMetrics />

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-4 gap-8">
          <Card className="lg:col-span-3 overflow-hidden flex flex-col max-h-[600px]">
            <div className="flex-1 overflow-y-auto">
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  message={message.text}
                  isAi={message.isAi}
                  timestamp={message.timestamp}
                />
              ))}
            </div>
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
          </Card>

          <Card className="p-4">
            <h3 className="font-semibold mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => handleSendMessage("Can I afford to buy a car in December 2025?")}
              >
                Car Loan Eligibility
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => handleSendMessage("Should I transfer my home loan?")}
              >
                Home Loan Transfer
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => handleSendMessage("How can I improve my credit score?")}
              >
                Credit Score Tips
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index;