"""
Base Agent Class for Finance Wizardry Bot
Provides common functionality for all specialized agents
"""

from typing import List, Optional, Dict, Any
from crewai import Agent, Task, Crew
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

from config.agents_config import config, AGENT_ROLES


class BaseFinanceAgent:
    """Base class for all finance agents"""
    
    def __init__(self, agent_type: str, tools: List[BaseTool] = None):
        self.agent_type = agent_type
        self.tools = tools or []
        self.llm = self._get_llm()
        self.agent = self._create_agent()
    
    def _get_llm(self):
        """Get the appropriate LLM based on configuration"""
        if config.openai_api_key:
            return ChatOpenAI(
                model="gpt-4",
                api_key=config.openai_api_key,
                temperature=0.7
            )
        else:
            return Ollama(
                model=config.default_model,
                base_url=config.ollama_base_url,
                temperature=0.7
            )
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        if self.agent_type not in AGENT_ROLES:
            raise ValueError(f"Unknown agent type: {self.agent_type}")
        
        role_config = AGENT_ROLES[self.agent_type]
        
        return Agent(
            role=role_config["role"],
            goal=role_config["goal"],
            backstory=role_config["backstory"],
            tools=self.tools,
            llm=self.llm,
            verbose=config.verbose,
            allow_delegation=False,
            max_iter=config.max_iterations
        )
    
    def create_task(self, description: str, expected_output: str = None) -> Task:
        """Create a task for this agent"""
        return Task(
            description=description,
            expected_output=expected_output or "Comprehensive analysis and recommendations in structured format",
            agent=self.agent
        )
    
    def execute_task(self, task_description: str, expected_output: str = None) -> str:
        """Execute a single task"""
        task = self.create_task(task_description, expected_output)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=config.verbose
        )
        
        result = crew.kickoff()
        return str(result)
    
    def collaborate_with(self, other_agents: List['BaseFinanceAgent'], tasks: List[Task]) -> str:
        """Collaborate with other agents on multiple tasks"""
        all_agents = [self.agent] + [agent.agent for agent in other_agents]
        
        crew = Crew(
            agents=all_agents,
            tasks=tasks,
            verbose=config.verbose
        )
        
        result = crew.kickoff()
        return str(result)


class AgentFactory:
    """Factory class for creating finance agents"""
    
    @staticmethod
    def create_agent(agent_type: str, tools: List[BaseTool] = None) -> BaseFinanceAgent:
        """Create an agent of the specified type"""
        from .news_intelligence_agent import NewsIntelligenceAgent
        from .financial_advisor_agent import FinancialAdvisorAgent
        from .credit_card_agent import CreditCardAgent
        from .portfolio_agent import PortfolioAgent
        from .data_analyst_agent import DataAnalystAgent
        
        agent_classes = {
            "news_intelligence": NewsIntelligenceAgent,
            "financial_advisor": FinancialAdvisorAgent,
            "credit_card_specialist": CreditCardAgent,
            "portfolio_manager": PortfolioAgent,
            "data_analyst": DataAnalystAgent
        }
        
        if agent_type not in agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_classes[agent_type](tools=tools)
