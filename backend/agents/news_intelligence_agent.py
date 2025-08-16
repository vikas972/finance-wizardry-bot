"""
News Intelligence Agent
Specialized agent for financial news analysis and market intelligence
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from crewai import Task

from .base_agent import BaseFinanceAgent
from tools.database_tools import NewsDataTool
from config.agents_config import TASK_TEMPLATES


class NewsIntelligenceAgent(BaseFinanceAgent):
    """Agent specialized in financial news analysis and market intelligence"""
    
    def __init__(self, tools: List[BaseTool] = None):
        # Add news-specific tools
        news_tools = [NewsDataTool()]
        if tools:
            news_tools.extend(tools)
        
        super().__init__("news_intelligence", news_tools)
    
    def analyze_latest_news(self) -> str:
        """Analyze the latest financial news"""
        task_description = TASK_TEMPLATES["analyze_news"]
        
        expected_output = """
        A comprehensive financial news analysis report including:
        1. Executive Summary of key market events
        2. Sector Impact Analysis (Technology, Finance, Healthcare, Energy, etc.)
        3. Economic Indicators Update
        4. Market Sentiment Assessment
        5. Investment Opportunities and Risks
        6. Short-term and Long-term Market Outlook
        7. Actionable Recommendations for investors
        
        Format the response in clear sections with bullet points for easy reading.
        """
        
        return self.execute_task(task_description, expected_output)
    
    def get_trending_topics(self) -> str:
        """Get trending financial topics"""
        task_description = """
        Analyze trending financial topics and provide insights:
        1. Identify the most discussed topics in recent financial news
        2. Analyze the sentiment around each trending topic
        3. Assess the potential market impact of these trends
        4. Provide context and background for each trend
        5. Suggest investment strategies related to these trends
        
        Use the news_data_fetcher tool with 'trending' parameter to get high-impact news.
        """
        
        expected_output = """
        A trending topics report with:
        1. Top 5-10 trending financial topics
        2. Sentiment analysis for each topic (Bullish/Bearish/Neutral)
        3. Impact assessment (High/Medium/Low)
        4. Related stock symbols or sectors
        5. Investment implications
        6. Timeline and expected duration of trend
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_sector_news(self, sector: str) -> str:
        """Analyze news for a specific sector"""
        task_description = f"""
        Analyze financial news specifically for the {sector} sector:
        1. Gather recent news articles related to {sector}
        2. Identify key developments and trends
        3. Analyze regulatory changes affecting the sector
        4. Assess competitive landscape changes
        5. Evaluate growth prospects and challenges
        6. Provide sector-specific investment recommendations
        
        Use the news_data_fetcher tool with 'category:{sector}' parameter.
        """
        
        expected_output = f"""
        A {sector} sector analysis report including:
        1. Sector Overview and Recent Performance
        2. Key News Events and Developments
        3. Regulatory Environment Changes
        4. Company-specific Updates (top players)
        5. Technical and Fundamental Analysis
        6. Investment Opportunities and Risks
        7. Price Targets and Recommendations
        """
        
        return self.execute_task(task_description, expected_output)
    
    def get_market_sentiment(self) -> str:
        """Analyze overall market sentiment"""
        task_description = """
        Provide a comprehensive market sentiment analysis:
        1. Analyze sentiment across different news sources
        2. Identify bullish and bearish indicators
        3. Assess investor mood and confidence levels
        4. Examine fear and greed indicators
        5. Compare current sentiment to historical patterns
        6. Predict short-term market direction based on sentiment
        
        Use news_data_fetcher with 'sentiment:positive' and 'sentiment:negative' to compare.
        """
        
        expected_output = """
        A market sentiment report including:
        1. Overall Sentiment Score (scale 1-10)
        2. Bullish Indicators and Supporting Evidence
        3. Bearish Indicators and Risk Factors
        4. Sentiment by Sector
        5. Fear & Greed Index Analysis
        6. Contrarian Indicators
        7. Short-term Market Direction Prediction
        8. Investment Strategy Recommendations based on sentiment
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_earnings_news(self) -> str:
        """Analyze earnings-related news and reports"""
        task_description = """
        Analyze recent earnings news and quarterly reports:
        1. Identify companies reporting earnings
        2. Analyze earnings beats and misses
        3. Examine guidance changes and forward-looking statements
        4. Assess market reactions to earnings
        5. Identify earnings-driven investment opportunities
        6. Provide earnings season overview and outlook
        
        Focus on high-impact earnings that could affect broader market trends.
        """
        
        expected_output = """
        An earnings analysis report with:
        1. Earnings Season Summary
        2. Notable Earnings Beats and Misses
        3. Guidance Updates and Revisions
        4. Market Reaction Analysis
        5. Sector Performance During Earnings
        6. Key Takeaways and Themes
        7. Post-earnings Investment Opportunities
        8. Upcoming Earnings to Watch
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_news_summary(self, customer_id: Optional[int] = None) -> str:
        """Create a personalized news summary"""
        if customer_id:
            task_description = f"""
            Create a personalized financial news summary for customer {customer_id}:
            1. Analyze the customer's investment profile and interests
            2. Filter news relevant to their portfolio and preferences
            3. Highlight news affecting their current investments
            4. Provide sector-specific updates based on their allocation
            5. Include general market overview
            6. Offer personalized insights and recommendations
            
            First use customer_data_fetcher and portfolio_data_fetcher to understand the customer profile.
            """
        else:
            task_description = """
            Create a general financial news summary:
            1. Top market headlines and developments
            2. Major economic indicators and releases
            3. Sector rotation and performance updates
            4. Central bank and policy news
            5. Geopolitical events affecting markets
            6. Currency and commodity updates
            """
        
        expected_output = """
        A concise news summary (500-750 words) with:
        1. Executive Summary (2-3 sentences)
        2. Top Headlines (3-5 key stories)
        3. Market Impact Analysis
        4. Key Numbers and Data Points
        5. What to Watch (upcoming events/catalysts)
        6. Bottom Line (actionable takeaway)
        """
        
        return self.execute_task(task_description, expected_output)
