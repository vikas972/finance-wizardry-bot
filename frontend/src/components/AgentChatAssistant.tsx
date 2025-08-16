import React, { useState, useEffect, useRef } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Bot, 
  MessageSquare, 
  Newspaper,
  CreditCard,
  User,
  BarChart3,
  Brain,
  Users,
  Activity
} from "lucide-react";
import { cn } from "@/lib/utils";
import { agentService, AgentChatResponse } from "@/services/agentService";

interface Message extends AgentChatResponse {
  timestamp: string;
  isLoading?: boolean;
}

interface AgentChatAssistantProps {
  customerId?: number | null;
}

const agentTypes = [
  {
    id: "news_intelligence",
    name: "News Intelligence",
    icon: Newspaper,
    color: "bg-blue-500",
    description: "Market sentiment and financial news analysis",
    queries: [
      "What's the current market sentiment?",
      "Latest financial news affecting my portfolio",
      "Market trends for this week",
      "Economic indicators analysis"
    ]
  },
  {
    id: "financial_advisor",
    name: "Financial Advisor",
    icon: User,
    color: "bg-yellow-500", 
    description: "Personalized financial advice and planning",
    queries: [
      "Should I invest $10,000 in stocks?",
      "How can I improve my financial situation?",
      "Investment strategy for retirement",
      "Tax planning recommendations"
    ]
  },
  {
    id: "credit_card_specialist",
    name: "Credit Specialist",
    icon: CreditCard,
    color: "bg-amber-500",
    description: "Credit analysis and card recommendations",
    queries: [
      "How can I improve my credit score?",
      "Best credit cards for my profile",
      "Credit utilization optimization",
      "Debt management strategy"
    ]
  }
];

const workflows = [
  {
    id: "comprehensive",
    name: "Comprehensive Analysis",
    icon: BarChart3,
    description: "Complete financial profile analysis using all agents"
  },
  {
    id: "market",
    name: "Market Analysis", 
    icon: Activity,
    description: "Market trends and sentiment analysis"
  }
];

export default function AgentChatAssistant({ customerId }: AgentChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      response: "Hello! I'm your AI financial advisor team. I can connect you with specialized agents for news analysis, financial planning, or credit optimization. How can we help you today?",
      agent_type: "system",
      agent_role: "System",
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [availableAgents, setAvailableAgents] = useState<any>(null);
  
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Load available agents on mount
  useEffect(() => {
    const loadAgents = async () => {
      try {
        const agents = await agentService.getAvailableAgents();
        setAvailableAgents(agents);
      } catch (error) {
        console.error('Failed to load agents:', error);
      }
    };
    loadAgents();
  }, []);

  const handleSendMessage = async (message: string) => {
    if (!customerId) return;

    setIsLoading(true);
    
    // Add user message
    const userMessage: Message = {
      response: message,
      agent_type: "user",
      agent_role: "User",
      timestamp: new Date().toLocaleTimeString(),
      customer_id: customerId
    };
    
    // Add loading message
    const loadingMessage: Message = {
      response: "",
      agent_type: "system",
      agent_role: "Processing",
      timestamp: new Date().toLocaleTimeString(),
      isLoading: true
    };
    
    setMessages(prev => [...prev, userMessage, loadingMessage]);

    try {
      let response: AgentChatResponse;
      
      if (selectedAgent && selectedAgent !== "intelligent") {
        // Chat with specific agent
        response = await agentService.chatWithAgent(selectedAgent, {
          query: message,
          customer_id: customerId
        });
      } else {
        // Use intelligent routing
        response = await agentService.intelligentChat(customerId, message);
      }
      
      // Replace loading message with actual response
      const aiMessage: Message = {
        ...response,
        timestamp: new Date().toLocaleTimeString(),
      };
      
      setMessages(prev => prev.slice(0, -1).concat(aiMessage));
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        response: 'Sorry, I encountered an error processing your request.',
        agent_type: "error",
        agent_role: "Error",
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => prev.slice(0, -1).concat(errorMessage));
    }
    
    setIsLoading(false);
  };

  const handleWorkflowTrigger = async (workflowType: string) => {
    if (!customerId) return;

    setIsLoading(true);
    
    try {
      let result;
      const timestamp = new Date().toLocaleTimeString();
      
      if (workflowType === "comprehensive") {
        result = await agentService.getComprehensiveAnalysis(customerId);
        
        const workflowMessage: Message = {
          response: `## Comprehensive Financial Analysis\n\n**Generated:** ${result.timestamp}\n\n### Market Sentiment\n${JSON.stringify(result.analysis.market_sentiment, null, 2)}\n\n### Customer Profile\n${JSON.stringify(result.analysis.customer_profile, null, 2)}\n\n### Credit Analysis\n${JSON.stringify(result.analysis.credit_analysis, null, 2)}`,
          agent_type: "workflow",
          agent_role: "Multi-Agent Analysis",
          timestamp,
          customer_id: customerId
        };
        
        setMessages(prev => [...prev, workflowMessage]);
      } else if (workflowType === "market") {
        result = await agentService.getMarketAnalysis();
        
        const workflowMessage: Message = {
          response: `## Market Analysis Report\n\n**Generated:** ${result.analysis.timestamp}\n\n### Market Sentiment\n${JSON.stringify(result.analysis.market_sentiment, null, 2)}\n\n### Latest News\n${JSON.stringify(result.analysis.latest_news, null, 2)}`,
          agent_type: "workflow", 
          agent_role: "Market Analysis",
          timestamp,
        };
        
        setMessages(prev => [...prev, workflowMessage]);
      }
    } catch (error) {
      console.error('Error running workflow:', error);
    }
    
    setIsLoading(false);
  };

  const getAgentBadgeColor = (agentType: string) => {
    const agent = agentTypes.find(a => a.id === agentType);
    return agent?.color || "bg-gray-500";
  };

  if (!customerId) {
    return (
      <div className="p-6">
        <Card className="p-8 text-center">
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-12 h-12 text-blue-500" />
          </div>
          <h2 className="text-xl font-semibold mb-4">Multi-Agent AI Assistant</h2>
          <p className="text-gray-600">Please select a customer to start using the intelligent agent system.</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center gap-3">
        <Brain className="w-8 h-8 text-blue-500" />
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Multi-Agent AI Assistant</h1>
          <p className="text-gray-600">Intelligent financial advice from specialized AI agents</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Chat Area */}
        <Card className="lg:col-span-3 overflow-hidden flex flex-col h-[700px]">
          <CardHeader className="border-b">
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              Multi-Agent Chat
              {selectedAgent && (
                <Badge variant="secondary" className={cn("ml-2", getAgentBadgeColor(selectedAgent))}>
                  {agentTypes.find(a => a.id === selectedAgent)?.name || "Intelligent Routing"}
                </Badge>
              )}
            </CardTitle>
          </CardHeader>
          
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4" ref={chatContainerRef}>
            {messages.map((message, index) => (
              <div key={index} className="mb-4">
                <div className="flex items-start gap-3">
                  {message.agent_type !== "user" && (
                    <div className={cn("w-8 h-8 rounded-full flex items-center justify-center text-white text-xs flex-shrink-0", 
                      getAgentBadgeColor(message.agent_type))}>
                      {message.agent_type === "system" ? "S" : 
                       message.agent_type === "workflow" ? "W" :
                       message.agent_type === "error" ? "E" :
                       message.agent_type.charAt(0).toUpperCase()}
                    </div>
                  )}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium truncate">{message.agent_role}</span>
                      <span className="text-xs text-gray-500 flex-shrink-0">{message.timestamp}</span>
                    </div>
                    <div className="break-words overflow-hidden">
                      <ChatMessage
                        message={message.response}
                        isAi={message.agent_type !== "user"}
                        timestamp={message.timestamp}
                        isLoading={message.isLoading}
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {/* Chat Input */}
          <div className="border-t">
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
          </div>
        </Card>

        {/* Agent Selection Sidebar */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">AI Agents</CardTitle>
          </CardHeader>
          <CardContent className="p-4">
            <Tabs defaultValue="agents" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="agents">Agents</TabsTrigger>
                <TabsTrigger value="workflows">Workflows</TabsTrigger>
              </TabsList>
              
              <TabsContent value="agents" className="space-y-3 mt-4">
                <Button
                  variant={selectedAgent === null ? "default" : "outline"}
                  className="w-full justify-start"
                  onClick={() => setSelectedAgent(null)}
                >
                  <Brain className="w-4 h-4 mr-2" />
                  <div className="text-left">
                    <p className="text-sm font-medium">Intelligent Routing</p>
                    <p className="text-xs text-gray-500">Auto-select best agent</p>
                  </div>
                </Button>
                
                {agentTypes.map((agent) => (
                  <Button
                    key={agent.id}
                    variant={selectedAgent === agent.id ? "default" : "outline"}
                    className="w-full justify-start h-auto p-3"
                    onClick={() => setSelectedAgent(agent.id)}
                  >
                    <agent.icon className="w-4 h-4 mr-3 flex-shrink-0" />
                    <div className="text-left">
                      <p className="text-sm font-medium">{agent.name}</p>
                      <p className="text-xs text-gray-500">{agent.description}</p>
                    </div>
                  </Button>
                ))}
              </TabsContent>
              
              <TabsContent value="workflows" className="space-y-3 mt-4">
                {workflows.map((workflow) => (
                  <Button
                    key={workflow.id}
                    variant="outline"
                    className="w-full justify-start h-auto p-3"
                    onClick={() => handleWorkflowTrigger(workflow.id)}
                    disabled={isLoading}
                  >
                    <workflow.icon className="w-4 h-4 mr-3 flex-shrink-0" />
                    <div className="text-left">
                      <p className="text-sm font-medium">{workflow.name}</p>
                      <p className="text-xs text-gray-500">{workflow.description}</p>
                    </div>
                  </Button>
                ))}
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      {selectedAgent && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {React.createElement(agentTypes.find(a => a.id === selectedAgent)?.icon || Bot, { className: "w-5 h-5" })}
              {agentTypes.find(a => a.id === selectedAgent)?.name} - Quick Actions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2">
              {agentTypes.find(a => a.id === selectedAgent)?.queries.map((query, index) => (
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
          </CardContent>
        </Card>
      )}
    </div>
  );
}
