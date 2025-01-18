import { useState } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { FinancialMetrics } from "@/components/FinancialMetrics";
import { FinancialCharts } from "@/components/FinancialCharts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Lightbulb, TrendingUp, ShieldCheck, Calculator, RefreshCw, PiggyBank } from "lucide-react";

interface Message {
  text: string;
  isAi: boolean;
  timestamp: string;
}

const recommendedQueries = [
  {
    icon: Calculator,
    text: "Can I afford to buy a car in December 2025?",
    category: "Auto Loan",
  },
  {
    icon: RefreshCw,
    text: "Should I transfer my home loan to get better rates?",
    category: "Home Loan",
  },
  {
    icon: PiggyBank,
    text: "How can I optimize my monthly EMIs?",
    category: "Financial Planning",
  },
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

  const mockAiResponse = async (userMessage: string) => {
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1500));

    let response = "";
    if (userMessage.toLowerCase().includes("car")) {
      response = "Based on your financial profile:\n\n" +
        "- Loan Eligibility Score: 785 (Excellent)\n" +
        "- Debt-to-Income Ratio: 32%\n" +
        "- Current EMI Load: ₹45,000\n\n" +
        "Given your excellent credit profile but considering your current EMI load, I recommend:\n" +
        "1. Consider a car loan up to ₹8L with 3-year tenure\n" +
        "2. Aim for EMI not exceeding ₹15,000\n" +
        "3. Look for interest rates between 7.5-8.5%\n\n" +
        "Would you like me to show you pre-approved car loan offers?";
    } else if (userMessage.toLowerCase().includes("home loan")) {
      response = "I've analyzed your home loan situation:\n\n" +
        "Current market rates start from 7.2%\n" +
        "Your profile qualifies for preferential rates\n\n" +
        "Recommendations:\n" +
        "1. Consider balance transfer if current rate > 8.5%\n" +
        "2. Negotiate with current lender first\n" +
        "3. Check for zero processing fee offers\n\n" +
        "Would you like to see detailed calculations and top lender options?";
    } else {
      response = "Based on your financial profile, I can assist with:\n\n" +
        "1. Loan eligibility assessment\n" +
        "2. EMI optimization strategies\n" +
        "3. Credit score improvement tips\n" +
        "4. Investment recommendations\n\n" +
        "What specific aspect would you like to explore?";
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
        <FinancialCharts />

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
            <div className="border-t">
              <div className="p-4 bg-accent/50">
                <h3 className="font-semibold mb-2 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  Recommended Actions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <TrendingUp className="w-4 h-4" />
                    Consider debt consolidation to optimize EMIs
                  </div>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <ShieldCheck className="w-4 h-4" />
                    Review credit report for better rates
                  </div>
                </div>
              </div>
              <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
            </div>
          </Card>

          <Card className="p-4">
            <h3 className="font-semibold mb-4">Recommended Queries</h3>
            <div className="space-y-2">
              {recommendedQueries.map((query, index) => (
                <Button
                  key={index}
                  variant="outline"
                  className="w-full justify-start text-left"
                  onClick={() => handleSendMessage(query.text)}
                >
                  <query.icon className="w-4 h-4 mr-2" />
                  <div>
                    <p className="text-sm">{query.text}</p>
                    <p className="text-xs text-muted-foreground">{query.category}</p>
                  </div>
                </Button>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index;