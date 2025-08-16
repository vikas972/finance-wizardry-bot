"""
Simplified Multi-Agent System without complex dependencies
Works with existing codebase and provides agent-like functionality
"""

import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from database import get_db
from models import Customer, AAData, BureauData, ITRData, NewsArticle
from news_intelligence import NewsIntelligenceAgent
from llm_utils import OllamaLLM
from datetime import datetime, timedelta
from sqlalchemy import desc


class SimpleFinanceAgent:
    """Base class for simple finance agents"""
    
    def __init__(self, agent_type: str, role: str):
        self.agent_type = agent_type
        self.role = role
    
    def process_query(self, query: str, customer_id: Optional[int] = None) -> str:
        """Process a query and return a response"""
        return f"[{self.role}] Processing: {query}"


class SimpleNewsIntelligenceAgent(SimpleFinanceAgent):
    """Simplified News Intelligence Agent"""
    
    def __init__(self):
        super().__init__("news_intelligence", "News Intelligence Specialist")
        self.news_agent = NewsIntelligenceAgent()
        self.llm = OllamaLLM()
    
    def get_latest_news(self, limit: int = 10) -> Dict[str, Any]:
        """Get latest news articles"""
        try:
            db = next(get_db())
            articles = db.query(NewsArticle).filter(
                NewsArticle.is_active == True
            ).order_by(desc(NewsArticle.published_date)).limit(limit).all()
            
            result = []
            for article in articles:
                result.append({
                    "title": article.title,
                    "source": article.source,
                    "published_date": article.published_date.isoformat() if article.published_date else None,
                    "sentiment_label": article.sentiment_label,
                    "impact_score": article.impact_score,
                    "category": article.category
                })
            
            return {"news": result, "count": len(result)}
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'db' in locals():
                db.close()
    
    def get_market_sentiment(self) -> Dict[str, Any]:
        """Analyze market sentiment from news"""
        try:
            db = next(get_db())
            yesterday = datetime.now() - timedelta(days=1)
            
            articles = db.query(NewsArticle).filter(
                NewsArticle.published_date >= yesterday,
                NewsArticle.is_active == True
            ).all()
            
            if not articles:
                return {"sentiment": "neutral", "confidence": 0, "articles_analyzed": 0}
            
            # Calculate average sentiment
            total_sentiment = sum(article.sentiment_score or 0 for article in articles)
            avg_sentiment = total_sentiment / len(articles)
            
            # Determine sentiment label
            if avg_sentiment > 0.1:
                sentiment = "positive"
            elif avg_sentiment < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": avg_sentiment,
                "confidence": abs(avg_sentiment),
                "articles_analyzed": len(articles)
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'db' in locals():
                db.close()
    
    def get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        """Get customer profile for context"""
        try:
            db = next(get_db())
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            aa_data = db.query(AAData).filter(AAData.customer_id == customer_id).first()
            bureau_data = db.query(BureauData).filter(BureauData.customer_id == customer_id).first()
            
            profile = {
                "customer_info": {
                    "name": customer.name if customer else "Unknown",
                    "email": customer.email if customer else "Unknown"
                },
                "financial_data": {
                    "account_summary": aa_data.account_summary if aa_data else None,
                    "spending_patterns": aa_data.spending_patterns if aa_data else None
                },
                "credit_score": bureau_data.credit_score if bureau_data else None
            }
            
            return profile
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'db' in locals():
                db.close()
    
    def process_query(self, query: str, customer_id: Optional[int] = None) -> str:
        """Process news-related queries with real-time data and AI responses"""
        try:
            # Get fresh real-time news data
            print("🔄 Fetching fresh news data...")
            self.news_agent.update_news_feed()
            
            # Get latest news and sentiment
            latest_news = self.get_latest_news(10)
            market_sentiment = self.get_market_sentiment()
            
            # Get customer context if available
            customer_context = ""
            if customer_id:
                customer_profile = self.get_customer_profile(customer_id)
                customer_context = f"Customer Profile: {json.dumps(customer_profile, indent=2)}\n\n"
            
            # Prepare context for Ollama
            news_context = f"""
            Latest Market News ({len(latest_news.get('news', []))} articles):
            {json.dumps(latest_news, indent=2)}
            
            Market Sentiment Analysis:
            {json.dumps(market_sentiment, indent=2)}
            
            {customer_context}
            User Query: {query}
            """
            
            system_prompt = """You are a financial news intelligence specialist. Analyze the provided market news and sentiment data to give personalized, contextual responses. Focus on:
            1. Current market trends and sentiment
            2. Relevant news that impacts the customer's financial interests
            3. Actionable insights based on news analysis
            4. Professional but conversational tone
            
            Always provide specific insights based on the actual news data provided. Keep responses concise but informative."""
            
            # Generate dynamic response using Ollama
            print("🤖 Generating AI response...")
            ai_response = self.llm.generate_response(
                prompt=news_context,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=800
            )
            
            return ai_response
            
        except Exception as e:
            print(f"❌ Error in news agent: {str(e)}")
            return f"I apologize, but I encountered an error analyzing the latest market news: {str(e)}. Please try again."


class SimpleFinancialAdvisorAgent(SimpleFinanceAgent):
    """Simplified Financial Advisor Agent"""
    
    def __init__(self):
        super().__init__("financial_advisor", "Financial Advisor")
        self.llm = OllamaLLM()
    
    def get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        """Get customer financial profile"""
        try:
            db = next(get_db())
            
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                return {"error": "Customer not found"}
            
            aa_data = db.query(AAData).filter(AAData.customer_id == customer_id).first()
            bureau_data = db.query(BureauData).filter(BureauData.customer_id == customer_id).first()
            
            profile = {
                "customer_id": customer_id,
                "name": customer.name,
                "email": customer.email,
                "aa_data": {
                    "account_summary": aa_data.account_summary if aa_data else None,
                    "assets": aa_data.assets if aa_data else None,
                    "spending_patterns": aa_data.spending_patterns if aa_data else None
                },
                "credit_score": bureau_data.credit_score if bureau_data else None,
                "credit_utilization": bureau_data.repayment_history.get("credit_utilization", 0) if bureau_data and bureau_data.repayment_history else None
            }
            
            return profile
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'db' in locals():
                db.close()
    
    def provide_financial_advice(self, customer_id: int, query: str) -> str:
        """Provide basic financial advice"""
        profile = self.get_customer_profile(customer_id)
        
        if "error" in profile:
            return f"Unable to provide personalized advice: {profile['error']}"
        
        advice = f"Hello {profile['name']}! Based on your profile, here's my advice:\n\n"
        
        query_lower = query.lower()
        
        if "investment" in query_lower or "invest" in query_lower:
            advice += "💰 Investment Advice:\n"
            advice += "- Diversify your portfolio across different asset classes\n"
            advice += "- Consider your risk tolerance and investment timeline\n"
            advice += "- Start with low-cost index funds if you're a beginner\n"
            
            if profile.get("credit_score"):
                if profile["credit_score"] > 750:
                    advice += "- With your excellent credit score, you have access to better investment products\n"
                elif profile["credit_score"] < 650:
                    advice += "- Focus on improving your credit score before taking on investment debt\n"
        
        elif "credit" in query_lower or "debt" in query_lower:
            advice += "💳 Credit Management:\n"
            if profile.get("credit_score"):
                advice += f"- Your current credit score is {profile['credit_score']}\n"
                if profile.get("credit_utilization"):
                    advice += f"- Your credit utilization is {profile['credit_utilization']}%\n"
                    if profile["credit_utilization"] > 30:
                        advice += "- Try to keep credit utilization below 30% for better scores\n"
                    else:
                        advice += "- Great job keeping your credit utilization low!\n"
            
            advice += "- Pay bills on time to maintain good credit history\n"
            advice += "- Consider paying off high-interest debt first\n"
        
        elif "budget" in query_lower or "expense" in query_lower:
            advice += "📊 Budgeting Tips:\n"
            advice += "- Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings\n"
            advice += "- Track your expenses to identify spending patterns\n"
            advice += "- Build an emergency fund with 3-6 months of expenses\n"
        
        else:
            advice += "I can help you with:\n"
            advice += "- Investment strategies and portfolio planning\n"
            advice += "- Credit management and debt reduction\n"
            advice += "- Budgeting and expense management\n"
            advice += "- Retirement planning and savings goals\n"
        
        return advice
    
    def process_query(self, query: str, customer_id: Optional[int] = None) -> str:
        """Process financial advice queries with AI and customer context"""
        try:
            if not customer_id:
                return "[Financial Advisor] I'd be happy to help with financial advice! Please provide your customer ID for personalized recommendations."
            
            # Get comprehensive customer profile
            customer_profile = self.get_customer_profile(customer_id)
            
            if "error" in customer_profile:
                return f"Unable to access customer data: {customer_profile['error']}"
            
            # Prepare context for Ollama
            financial_context = f"""
            Customer Financial Profile:
            {json.dumps(customer_profile, indent=2)}
            
            User Query: {query}
            """
            
            system_prompt = """You are an expert financial advisor with years of experience. Analyze the customer's complete financial profile and provide personalized, actionable financial advice. Focus on:
            
            1. Personalized recommendations based on their specific financial situation
            2. Investment strategies aligned with their profile
            3. Risk assessment and mitigation advice  
            4. Debt management and optimization
            5. Tax planning opportunities
            6. Long-term financial planning
            
            Be specific, professional, and provide concrete steps they can take. Always consider their current financial status, credit profile, and spending patterns."""
            
            # Generate dynamic response using Ollama
            print("🤖 Generating personalized financial advice...")
            ai_response = self.llm.generate_response(
                prompt=financial_context,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            return ai_response
            
        except Exception as e:
            print(f"❌ Error in financial advisor: {str(e)}")
            return f"I apologize, but I encountered an error providing financial advice: {str(e)}. Please try again."


class SimpleCreditCardAgent(SimpleFinanceAgent):
    """Simplified Credit Card Specialist Agent"""
    
    def __init__(self):
        super().__init__("credit_card_specialist", "Credit Card Specialist")
        self.llm = OllamaLLM()
    
    def analyze_credit_profile(self, customer_id: int) -> Dict[str, Any]:
        """Analyze customer's credit profile"""
        try:
            db = next(get_db())
            
            bureau_data = db.query(BureauData).filter(BureauData.customer_id == customer_id).first()
            
            if not bureau_data:
                return {"error": "No credit data found"}
            
            analysis = {
                "credit_score": bureau_data.credit_score,
                "credit_utilization": bureau_data.repayment_history.get("credit_utilization", 0) if bureau_data.repayment_history else 0,
                "payment_history": bureau_data.repayment_history.get("on_time_payments", "N/A") if bureau_data.repayment_history else "N/A",
                "loan_details": bureau_data.loan_details if bureau_data.loan_details else {},
                "recommendations": []
            }
            
            # Generate recommendations based on credit profile
            if bureau_data.credit_score:
                if bureau_data.credit_score >= 750:
                    analysis["recommendations"].append("Excellent credit! You qualify for premium rewards cards")
                elif bureau_data.credit_score >= 700:
                    analysis["recommendations"].append("Good credit score. Consider cashback or travel rewards cards")
                elif bureau_data.credit_score >= 650:
                    analysis["recommendations"].append("Fair credit. Look for secured cards to improve your score")
                else:
                    analysis["recommendations"].append("Focus on credit building cards and improving payment history")
            
            credit_utilization = bureau_data.repayment_history.get("credit_utilization", 0) if bureau_data.repayment_history else 0
            if credit_utilization:
                if credit_utilization > 30:
                    analysis["recommendations"].append("Reduce credit utilization below 30% to improve your score")
                elif credit_utilization < 10:
                    analysis["recommendations"].append("Excellent credit utilization! Keep it up")
            
            return analysis
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'db' in locals():
                db.close()
    
    def process_query(self, query: str, customer_id: Optional[int] = None) -> str:
        """Process credit card related queries with AI analysis"""
        try:
            if not customer_id:
                return "[Credit Card Specialist] Please provide your customer ID for personalized credit card recommendations."
            
            # Get detailed credit analysis
            credit_analysis = self.analyze_credit_profile(customer_id)
            
            if "error" in credit_analysis:
                return f"Unable to analyze credit profile: {credit_analysis['error']}"
            
            # Prepare context for Ollama
            credit_context = f"""
            Customer Credit Profile Analysis:
            {json.dumps(credit_analysis, indent=2)}
            
            User Query: {query}
            """
            
            system_prompt = """You are a credit specialist and financial advisor with expertise in credit cards, credit optimization, and debt management. Analyze the customer's credit profile and provide personalized recommendations. Focus on:
            
            1. Credit score improvement strategies
            2. Credit utilization optimization
            3. Best credit card recommendations based on their profile
            4. Debt management and consolidation advice
            5. Credit building strategies
            6. Specific action steps they can take
            
            Be specific about credit products, strategies, and timeline for improvements. Always consider their current credit standing and financial capacity."""
            
            # Generate dynamic response using Ollama
            print("🤖 Generating personalized credit advice...")
            ai_response = self.llm.generate_response(
                prompt=credit_context,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            return ai_response
            
        except Exception as e:
            print(f"❌ Error in credit specialist: {str(e)}")
            return f"I apologize, but I encountered an error analyzing your credit profile: {str(e)}. Please try again."


class SimpleAgentCoordinator:
    """Coordinates all simple agents"""
    
    def __init__(self):
        self.agents = {
            "news_intelligence": SimpleNewsIntelligenceAgent(),
            "financial_advisor": SimpleFinancialAdvisorAgent(),
            "credit_card_specialist": SimpleCreditCardAgent()
        }
    
    def route_query(self, query: str, customer_id: Optional[int] = None) -> Dict[str, Any]:
        """Route query to appropriate agent"""
        query_lower = query.lower()
        
        # Determine which agent should handle the query
        if any(keyword in query_lower for keyword in ['news', 'market', 'sentiment', 'economic']):
            agent_type = "news_intelligence"
        elif any(keyword in query_lower for keyword in ['credit', 'card', 'score', 'debt', 'utilization']):
            agent_type = "credit_card_specialist"
        else:
            agent_type = "financial_advisor"
        
        agent = self.agents[agent_type]
        response = agent.process_query(query, customer_id)
        
        return {
            "response": response,
            "agent_used": agent_type,
            "agent_role": agent.role
        }
    
    def get_available_agents(self) -> Dict[str, Any]:
        """Get information about available agents"""
        return {
            "agents": {
                agent_type: {
                    "type": agent_type,
                    "role": agent.role,
                    "description": f"Specialized in {agent_type.replace('_', ' ')}"
                }
                for agent_type, agent in self.agents.items()
            }
        }
    
    def comprehensive_analysis(self, customer_id: int) -> Dict[str, Any]:
        """Perform comprehensive analysis using multiple agents"""
        results = {}
        
        # Get news intelligence
        news_agent = self.agents["news_intelligence"]
        results["market_sentiment"] = news_agent.get_market_sentiment()
        results["latest_news"] = news_agent.get_latest_news(3)
        
        # Get financial advice
        advisor_agent = self.agents["financial_advisor"]
        results["customer_profile"] = advisor_agent.get_customer_profile(customer_id)
        
        # Get credit analysis
        credit_agent = self.agents["credit_card_specialist"]
        results["credit_analysis"] = credit_agent.analyze_credit_profile(customer_id)
        
        return {
            "customer_id": customer_id,
            "analysis": results,
            "timestamp": datetime.now().isoformat()
        }


# Global coordinator instance
simple_coordinator = SimpleAgentCoordinator()
