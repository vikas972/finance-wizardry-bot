"""
Agent Configuration for Finance Wizardry Bot
Centralized configuration for all agents and LLM settings
"""

import os
from typing import Dict, Any
from pydantic_settings import BaseSettings


class AgentConfig(BaseSettings):
    """Configuration class for agents"""
    
    # LLM Configuration
    openai_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "llama3"
    
    # Database Configuration
    database_url: str = "postgresql://postgres:password@localhost/financebot"
    
    # Agent Settings
    enable_memory: bool = True
    max_iterations: int = 5
    verbose: bool = True
    
    # Tools Configuration
    enable_internet_search: bool = True
    search_max_results: int = 10
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Agent role definitions
AGENT_ROLES = {
    "news_intelligence": {
        "role": "Financial News Intelligence Specialist",
        "goal": "Gather, analyze, and provide insights from financial news and market data",
        "backstory": """You are an expert financial news analyst with deep understanding of market trends, 
        economic indicators, and their impact on investments. You excel at processing large volumes of 
        financial news and extracting actionable insights."""
    },
    
    "financial_advisor": {
        "role": "Personal Financial Advisor",
        "goal": "Provide personalized financial advice and investment recommendations",
        "backstory": """You are a certified financial advisor with 15+ years of experience helping clients 
        achieve their financial goals. You specialize in risk assessment, portfolio optimization, and 
        comprehensive financial planning."""
    },
    
    "credit_card_specialist": {
        "role": "Credit Card and Credit Analysis Expert",
        "goal": "Analyze credit profiles and recommend optimal credit card products",
        "backstory": """You are a credit specialist with extensive knowledge of credit scoring, credit card 
        products, and lending practices. You help clients optimize their credit utilization and select 
        the best credit products for their needs."""
    },
    
    "portfolio_manager": {
        "role": "Portfolio Management Specialist",
        "goal": "Monitor and optimize investment portfolios for maximum returns",
        "backstory": """You are a portfolio manager with expertise in asset allocation, risk management, 
        and performance optimization. You use quantitative analysis and market insights to make 
        data-driven investment decisions."""
    },
    
    "data_analyst": {
        "role": "Financial Data Analyst",
        "goal": "Extract, process, and analyze financial data from various sources",
        "backstory": """You are a financial data analyst specialized in working with databases, APIs, 
        and various data sources. You excel at data extraction, transformation, and providing clean, 
        structured data for analysis."""
    }
}

# Task templates
TASK_TEMPLATES = {
    "analyze_news": """
    Analyze the latest financial news and provide a comprehensive report including:
    1. Key market movements and trends
    2. Sector-specific impacts
    3. Economic indicators and their implications
    4. Investment opportunities and risks
    5. Actionable recommendations
    
    Focus on news from the last 24 hours and prioritize high-impact events.
    """,
    
    "provide_financial_advice": """
    Based on the customer's financial profile and goals, provide personalized advice including:
    1. Risk assessment and tolerance analysis
    2. Investment recommendations
    3. Portfolio optimization suggestions
    4. Tax planning strategies
    5. Financial goal planning
    
    Customer ID: {customer_id}
    Specific query: {query}
    """,
    
    "analyze_credit_profile": """
    Analyze the customer's credit profile and provide recommendations:
    1. Current credit score analysis
    2. Credit utilization optimization
    3. Credit card product recommendations
    4. Credit improvement strategies
    5. Debt management advice
    
    Customer ID: {customer_id}
    """,
    
    "portfolio_analysis": """
    Perform comprehensive portfolio analysis:
    1. Current allocation review
    2. Performance metrics calculation
    3. Risk assessment
    4. Rebalancing recommendations
    5. Market outlook impact
    
    Customer ID: {customer_id}
    Portfolio type: {portfolio_type}
    """,
    
    "fetch_customer_data": """
    Retrieve and process customer data from the database:
    1. Customer profile information
    2. Financial metrics and KPIs
    3. Transaction history
    4. Asset allocation data
    5. Credit information
    
    Customer ID: {customer_id}
    Data type: {data_type}
    """
}

# Initialize configuration
config = AgentConfig()
