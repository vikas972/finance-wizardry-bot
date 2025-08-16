"""
Agent Coordinator
Manages multi-agent workflows and orchestrates collaboration between specialized agents
"""

from typing import List, Dict, Any, Optional, Union
from crewai import Crew, Task
from enum import Enum

from .base_agent import BaseFinanceAgent, AgentFactory
from tools.database_tools import get_database_tools
from config.agents_config import config


class WorkflowType(Enum):
    """Types of multi-agent workflows"""
    COMPREHENSIVE_ANALYSIS = "comprehensive_analysis"
    INVESTMENT_RECOMMENDATION = "investment_recommendation"
    FINANCIAL_PLANNING = "financial_planning"
    CREDIT_OPTIMIZATION = "credit_optimization"
    PORTFOLIO_REVIEW = "portfolio_review"
    MARKET_ANALYSIS = "market_analysis"
    CUSTOMER_ONBOARDING = "customer_onboarding"


class AgentCoordinator:
    """Coordinates and orchestrates multi-agent workflows"""
    
    def __init__(self):
        self.agents = {}
        self.tools = get_database_tools()
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        agent_types = [
            "news_intelligence",
            "financial_advisor", 
            "credit_card_specialist",
            "portfolio_manager",
            "data_analyst"
        ]
        
        for agent_type in agent_types:
            self.agents[agent_type] = AgentFactory.create_agent(agent_type, self.tools)
    
    def get_agent(self, agent_type: str) -> BaseFinanceAgent:
        """Get a specific agent instance"""
        if agent_type not in self.agents:
            raise ValueError(f"Agent type {agent_type} not found")
        return self.agents[agent_type]
    
    def execute_comprehensive_analysis(self, customer_id: int) -> str:
        """Execute comprehensive customer analysis using multiple agents"""
        
        # Define tasks for each agent
        tasks = []
        
        # Data Analyst: Extract and analyze customer data
        data_task = Task(
            description=f"""
            Extract and analyze comprehensive customer data for customer {customer_id}.
            Provide a detailed customer profile including financial metrics, portfolio status,
            credit profile, and behavioral patterns. This will serve as the foundation for
            other agents' analyses.
            """,
            expected_output="Comprehensive customer data analysis with key insights",
            agent=self.agents["data_analyst"].agent
        )
        tasks.append(data_task)
        
        # Portfolio Manager: Analyze portfolio performance
        portfolio_task = Task(
            description=f"""
            Analyze portfolio performance and provide optimization recommendations for customer {customer_id}.
            Review asset allocation, risk metrics, and rebalancing needs. Consider the customer
            data analysis from the data analyst when making recommendations.
            """,
            expected_output="Portfolio performance analysis and optimization recommendations",
            agent=self.agents["portfolio_manager"].agent
        )
        tasks.append(portfolio_task)
        
        # Financial Advisor: Provide comprehensive financial advice
        advisor_task = Task(
            description=f"""
            Provide comprehensive financial advice for customer {customer_id} based on their
            complete financial profile. Include investment strategy, retirement planning,
            tax optimization, and goal achievement strategies. Consider insights from both
            the data analyst and portfolio manager.
            """,
            expected_output="Comprehensive financial advice and planning recommendations",
            agent=self.agents["financial_advisor"].agent
        )
        tasks.append(advisor_task)
        
        # Credit Specialist: Analyze credit profile
        credit_task = Task(
            description=f"""
            Analyze credit profile and provide credit optimization recommendations for customer {customer_id}.
            Review credit score, utilization, and recommend credit card strategies. Consider
            the overall financial picture provided by other agents.
            """,
            expected_output="Credit analysis and optimization recommendations",
            agent=self.agents["credit_card_specialist"].agent
        )
        tasks.append(credit_task)
        
        # News Intelligence: Provide market context
        news_task = Task(
            description=f"""
            Provide personalized market analysis and news summary for customer {customer_id}.
            Focus on news and trends relevant to their portfolio and investment interests.
            Consider the portfolio analysis and financial profile from other agents.
            """,
            expected_output="Personalized market analysis and news summary",
            agent=self.agents["news_intelligence"].agent
        )
        tasks.append(news_task)
        
        # Execute the crew
        crew = Crew(
            agents=[agent.agent for agent in self.agents.values()],
            tasks=tasks,
            verbose=config.verbose
        )
        
        result = crew.kickoff()
        return str(result)
    
    def execute_investment_recommendation(self, customer_id: int, investment_amount: float, 
                                        investment_goal: str, timeline: str) -> str:
        """Execute investment recommendation workflow"""
        
        tasks = []
        
        # Data Analyst: Analyze customer investment profile
        data_task = Task(
            description=f"""
            Analyze customer {customer_id}'s investment profile and current portfolio.
            Focus on risk tolerance, current allocation, and investment experience.
            Investment context: ${investment_amount:,.2f} for {investment_goal} over {timeline}.
            """,
            expected_output="Customer investment profile and portfolio analysis",
            agent=self.agents["data_analyst"].agent
        )
        tasks.append(data_task)
        
        # News Intelligence: Market opportunity analysis
        news_task = Task(
            description=f"""
            Analyze current market conditions and identify investment opportunities.
            Consider market trends, sector performance, and economic outlook that
            could impact investment decisions for {investment_goal}.
            """,
            expected_output="Market conditions and investment opportunity analysis",
            agent=self.agents["news_intelligence"].agent
        )
        tasks.append(news_task)
        
        # Portfolio Manager: Investment strategy
        portfolio_task = Task(
            description=f"""
            Develop specific investment strategy for customer {customer_id}.
            Amount: ${investment_amount:,.2f}, Goal: {investment_goal}, Timeline: {timeline}.
            Consider customer profile from data analyst and market opportunities from news intelligence.
            """,
            expected_output="Detailed investment strategy and specific recommendations",
            agent=self.agents["portfolio_manager"].agent
        )
        tasks.append(portfolio_task)
        
        # Financial Advisor: Integration and planning
        advisor_task = Task(
            description=f"""
            Integrate the investment recommendation into the customer's overall financial plan.
            Ensure the investment aligns with their goals, risk tolerance, and tax situation.
            Provide implementation guidance and monitoring recommendations.
            """,
            expected_output="Integrated investment plan with implementation guidance",
            agent=self.agents["financial_advisor"].agent
        )
        tasks.append(advisor_task)
        
        crew = Crew(
            agents=[
                self.agents["data_analyst"].agent,
                self.agents["news_intelligence"].agent,
                self.agents["portfolio_manager"].agent,
                self.agents["financial_advisor"].agent
            ],
            tasks=tasks,
            verbose=config.verbose
        )
        
        result = crew.kickoff()
        return str(result)
    
    def execute_market_analysis_workflow(self) -> str:
        """Execute comprehensive market analysis workflow"""
        
        tasks = []
        
        # News Intelligence: Latest market analysis
        news_task = Task(
            description="""
            Provide comprehensive analysis of current market conditions, trends, and sentiment.
            Include sector analysis, economic indicators, and investment opportunities.
            """,
            expected_output="Comprehensive market analysis and trends report",
            agent=self.agents["news_intelligence"].agent
        )
        tasks.append(news_task)
        
        # Data Analyst: Market data and patterns
        data_task = Task(
            description="""
            Analyze market data patterns and trends. Provide quantitative analysis
            of market metrics, volatility patterns, and correlation analysis.
            Complement the news intelligence with data-driven insights.
            """,
            expected_output="Quantitative market analysis and data insights",
            agent=self.agents["data_analyst"].agent
        )
        tasks.append(data_task)
        
        # Portfolio Manager: Investment implications
        portfolio_task = Task(
            description="""
            Analyze the investment implications of current market conditions.
            Provide strategic and tactical asset allocation recommendations
            based on market analysis and data patterns.
            """,
            expected_output="Investment strategy recommendations based on market analysis",
            agent=self.agents["portfolio_manager"].agent
        )
        tasks.append(portfolio_task)
        
        crew = Crew(
            agents=[
                self.agents["news_intelligence"].agent,
                self.agents["data_analyst"].agent,
                self.agents["portfolio_manager"].agent
            ],
            tasks=tasks,
            verbose=config.verbose
        )
        
        result = crew.kickoff()
        return str(result)
    
    def execute_credit_optimization_workflow(self, customer_id: int) -> str:
        """Execute credit optimization workflow"""
        
        tasks = []
        
        # Data Analyst: Credit profile analysis
        data_task = Task(
            description=f"""
            Analyze customer {customer_id}'s complete credit and financial profile.
            Include credit history, current obligations, and financial capacity.
            """,
            expected_output="Comprehensive credit and financial profile analysis",
            agent=self.agents["data_analyst"].agent
        )
        tasks.append(data_task)
        
        # Credit Specialist: Credit optimization strategy
        credit_task = Task(
            description=f"""
            Develop comprehensive credit optimization strategy for customer {customer_id}.
            Include credit improvement plan, utilization optimization, and product recommendations.
            Base recommendations on the detailed profile from the data analyst.
            """,
            expected_output="Comprehensive credit optimization strategy and recommendations",
            agent=self.agents["credit_card_specialist"].agent
        )
        tasks.append(credit_task)
        
        # Financial Advisor: Financial integration
        advisor_task = Task(
            description=f"""
            Integrate credit optimization into overall financial planning for customer {customer_id}.
            Consider impact on cash flow, investment capacity, and long-term financial goals.
            """,
            expected_output="Integrated financial plan with credit optimization",
            agent=self.agents["financial_advisor"].agent
        )
        tasks.append(advisor_task)
        
        crew = Crew(
            agents=[
                self.agents["data_analyst"].agent,
                self.agents["credit_card_specialist"].agent,
                self.agents["financial_advisor"].agent
            ],
            tasks=tasks,
            verbose=config.verbose
        )
        
        result = crew.kickoff()
        return str(result)
    
    def execute_workflow(self, workflow_type: WorkflowType, **kwargs) -> str:
        """Execute a specific workflow type"""
        
        workflow_map = {
            WorkflowType.COMPREHENSIVE_ANALYSIS: self.execute_comprehensive_analysis,
            WorkflowType.INVESTMENT_RECOMMENDATION: self.execute_investment_recommendation,
            WorkflowType.MARKET_ANALYSIS: self.execute_market_analysis_workflow,
            WorkflowType.CREDIT_OPTIMIZATION: self.execute_credit_optimization_workflow,
        }
        
        if workflow_type not in workflow_map:
            raise ValueError(f"Workflow type {workflow_type} not implemented")
        
        return workflow_map[workflow_type](**kwargs)
    
    def chat_with_agent(self, agent_type: str, query: str, customer_id: Optional[int] = None) -> str:
        """Chat with a specific agent"""
        if agent_type not in self.agents:
            raise ValueError(f"Agent type {agent_type} not found")
        
        agent = self.agents[agent_type]
        
        # Add customer context to query if provided
        if customer_id:
            enhanced_query = f"For customer {customer_id}: {query}"
        else:
            enhanced_query = query
        
        return agent.execute_task(enhanced_query)


# Global coordinator instance
coordinator = AgentCoordinator()
