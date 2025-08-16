/**
 * Multi-Agent Service for Finance Wizardry Bot
 * Provides interface to interact with the backend multi-agent architecture
 */

import { config } from '@/config';

export interface AgentChatRequest {
  query: string;
  customer_id?: number;
}

export interface AgentChatResponse {
  response: string;
  agent_type: string;
  agent_role: string;
  customer_id?: number;
}

export interface WorkflowRequest {
  customer_id?: number;
  investment_amount?: number;
  investment_goal?: string;
  timeline?: string;
}

export interface ComprehensiveAnalysis {
  customer_id: number;
  analysis: {
    market_sentiment: any;
    latest_news: any;
    customer_profile: any;
    credit_analysis: any;
  };
  timestamp: string;
}

export interface AvailableAgent {
  type: string;
  role: string;
  description: string;
}

export interface AvailableAgentsResponse {
  agents: Record<string, AvailableAgent>;
}

class AgentService {
  private baseUrl = config.apiUrl;

  /**
   * Chat with a specific agent
   */
  async chatWithAgent(agentType: string, request: AgentChatRequest): Promise<AgentChatResponse> {
    const response = await fetch(`${this.baseUrl}/agents/chat/${agentType}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Agent chat failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Intelligent chat that auto-routes to the best agent
   */
  async intelligentChat(customerId: number, message: string): Promise<AgentChatResponse> {
    const response = await fetch(`${this.baseUrl}/customers/${customerId}/chat-agent/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Intelligent chat failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get comprehensive analysis using multiple agents
   */
  async getComprehensiveAnalysis(customerId: number): Promise<ComprehensiveAnalysis> {
    const response = await fetch(`${this.baseUrl}/agents/workflow/comprehensive-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ customer_id: customerId }),
    });

    if (!response.ok) {
      throw new Error(`Comprehensive analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get investment recommendation
   */
  async getInvestmentRecommendation(request: WorkflowRequest): Promise<any> {
    const response = await fetch(`${this.baseUrl}/agents/workflow/investment-recommendation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Investment recommendation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get market analysis
   */
  async getMarketAnalysis(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/agents/workflow/market-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Market analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get credit optimization analysis
   */
  async getCreditOptimization(customerId: number): Promise<any> {
    const response = await fetch(`${this.baseUrl}/agents/workflow/credit-optimization`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ customer_id: customerId }),
    });

    if (!response.ok) {
      throw new Error(`Credit optimization failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get available agents
   */
  async getAvailableAgents(): Promise<AvailableAgentsResponse> {
    const response = await fetch(`${this.baseUrl}/agents/available`);

    if (!response.ok) {
      throw new Error(`Failed to get available agents: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get available workflows
   */
  async getAvailableWorkflows(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/agents/workflows`);

    if (!response.ok) {
      throw new Error(`Failed to get available workflows: ${response.statusText}`);
    }

    return response.json();
  }
}

export const agentService = new AgentService();
