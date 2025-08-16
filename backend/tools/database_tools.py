"""
Database Tools for Multi-Agent Architecture
Provides standardized API tools for database operations
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from datetime import datetime, timedelta
import json

from database import get_db
from models import (
    Customer, AAData, BureauData, ITRData, 
    NewsArticle, CreditCard, CustomerCreditCardPreference
)


class CustomerDataTool(BaseTool):
    """Tool for fetching customer data"""
    
    name: str = "customer_data_fetcher"
    description: str = """
    Fetches comprehensive customer data including profile, financial metrics, and related information.
    Input should be customer_id (integer) or 'all' for all customers.
    Returns structured customer data in JSON format.
    """
    
    def _run(self, customer_id: str) -> str:
        """Fetch customer data from database"""
        try:
            db = next(get_db())
            
            if customer_id.lower() == 'all':
                customers = db.query(Customer).all()
                result = []
                for customer in customers:
                    customer_data = {
                        "id": customer.id,
                        "name": customer.name,
                        "email": customer.email,
                        "phone": customer.phone,
                        "date_of_birth": customer.date_of_birth.isoformat() if customer.date_of_birth else None,
                        "created_at": customer.created_at.isoformat() if customer.created_at else None
                    }
                    result.append(customer_data)
                return json.dumps(result, indent=2)
            
            else:
                customer = db.query(Customer).filter(Customer.id == int(customer_id)).first()
                if not customer:
                    return f"Customer with ID {customer_id} not found"
                
                # Get AA data (financial metrics)
                aa_data = db.query(AAData).filter(
                    AAData.customer_id == customer.id
                ).first()
                
                customer_data = {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "date_of_birth": customer.date_of_birth.isoformat() if customer.date_of_birth else None,
                    "created_at": customer.created_at.isoformat() if customer.created_at else None,
                    "aa_data": {
                        "annual_income": aa_data.annual_income if aa_data else None,
                        "monthly_expenses": aa_data.monthly_expenses if aa_data else None,
                        "existing_loans": aa_data.existing_loans if aa_data else None,
                        "total_assets": aa_data.total_assets if aa_data else None,
                        "last_updated": aa_data.last_updated.isoformat() if aa_data and aa_data.last_updated else None
                    } if aa_data else None
                }
                
                return json.dumps(customer_data, indent=2)
                
        except Exception as e:
            return f"Error fetching customer data: {str(e)}"
        finally:
            db.close()


class AssetAllocationTool(BaseTool):
    """Tool for fetching asset allocation data from AA data"""
    
    name: str = "asset_allocation_fetcher"
    description: str = """
    Fetches asset allocation data for a specific customer from AA data.
    Input should be customer_id (integer).
    Returns asset allocation breakdown in JSON format.
    """
    
    def _run(self, customer_id: str) -> str:
        """Fetch asset allocation data"""
        try:
            db = next(get_db())
            
            aa_data = db.query(AAData).filter(
                AAData.customer_id == int(customer_id)
            ).first()
            
            if not aa_data:
                return f"No AA data found for customer {customer_id}"
            
            result = {
                "customer_id": customer_id,
                "account_summary": aa_data.account_summary,
                "spending_patterns": aa_data.spending_patterns,
                "assets": aa_data.assets,
                "created_at": aa_data.created_at.isoformat() if aa_data.created_at else None
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error fetching asset allocation: {str(e)}"
        finally:
            db.close()


class CreditDataTool(BaseTool):
    """Tool for fetching credit and bureau data"""
    
    name: str = "credit_data_fetcher"
    description: str = """
    Fetches credit-related data including credit card recommendations and bureau data.
    Input should be customer_id (integer).
    Returns credit information in JSON format.
    """
    
    def _run(self, customer_id: str) -> str:
        """Fetch credit-related data"""
        try:
            db = next(get_db())
            
            # Get credit card preferences
            preferences = db.query(CustomerCreditCardPreference).filter(
                CustomerCreditCardPreference.customer_id == int(customer_id)
            ).all()
            
            # Get bureau data
            bureau_data = db.query(BureauData).filter(
                BureauData.customer_id == int(customer_id)
            ).first()
            
            result = {
                "credit_card_preferences": [],
                "bureau_data": None
            }
            
            for pref in preferences:
                pref_data = {
                    "card_id": pref.card_id,
                    "preference_score": pref.preference_score,
                    "created_at": pref.created_at.isoformat() if pref.created_at else None
                }
                result["credit_card_preferences"].append(pref_data)
            
            if bureau_data:
                result["bureau_data"] = {
                    "credit_score": bureau_data.credit_score,
                    "credit_utilization": bureau_data.repayment_history.get("credit_utilization", 0) if bureau_data.repayment_history else 0,
                    "payment_history": bureau_data.repayment_history.get("on_time_payments", "N/A") if bureau_data.repayment_history else "N/A",
                    "loan_details": bureau_data.loan_details if bureau_data.loan_details else {},
                    "repayment_history": bureau_data.repayment_history if bureau_data.repayment_history else {},
                    "created_at": bureau_data.created_at.isoformat() if bureau_data.created_at else None
                }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error fetching credit data: {str(e)}"
        finally:
            db.close()


class NewsDataTool(BaseTool):
    """Tool for fetching news data"""
    
    name: str = "news_data_fetcher"
    description: str = """
    Fetches financial news articles with optional filtering.
    Input can be: 'latest' for recent news, 'trending' for trending topics, 
    'category:technology' for specific category, or 'sentiment:positive' for sentiment filtering.
    Returns news data in JSON format.
    """
    
    def _run(self, query: str) -> str:
        """Fetch news data based on query"""
        try:
            db = next(get_db())
            
            base_query = db.query(NewsArticle).filter(NewsArticle.is_active == True)
            
            if query.lower() == 'latest':
                articles = base_query.order_by(desc(NewsArticle.published_date)).limit(10).all()
            elif query.lower() == 'trending':
                # Get articles with high impact scores from last 24 hours
                yesterday = datetime.now() - timedelta(days=1)
                articles = base_query.filter(
                    and_(
                        NewsArticle.published_date >= yesterday,
                        NewsArticle.impact_score >= 0.6
                    )
                ).order_by(desc(NewsArticle.impact_score)).limit(15).all()
            elif query.startswith('category:'):
                category = query.split(':', 1)[1]
                articles = base_query.filter(
                    NewsArticle.category.ilike(f'%{category}%')
                ).order_by(desc(NewsArticle.published_date)).limit(20).all()
            elif query.startswith('sentiment:'):
                sentiment = query.split(':', 1)[1]
                articles = base_query.filter(
                    NewsArticle.sentiment_label == sentiment.lower()
                ).order_by(desc(NewsArticle.published_date)).limit(20).all()
            else:
                # Default to latest
                articles = base_query.order_by(desc(NewsArticle.published_date)).limit(10).all()
            
            result = []
            for article in articles:
                article_data = {
                    "id": article.id,
                    "title": article.title,
                    "url": article.url,
                    "source": article.source,
                    "published_date": article.published_date.isoformat() if article.published_date else None,
                    "snippet": article.snippet,
                    "category": article.category,
                    "sentiment_score": article.sentiment_score,
                    "sentiment_label": article.sentiment_label,
                    "impact_score": article.impact_score,
                    "symbols": article.symbols,
                    "keywords": article.keywords,
                    "market_region": article.market_region
                }
                result.append(article_data)
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error fetching news data: {str(e)}"
        finally:
            db.close()


class ITRDataTool(BaseTool):
    """Tool for fetching ITR (Income Tax Return) data"""
    
    name: str = "itr_data_fetcher"
    description: str = """
    Fetches ITR (Income Tax Return) data for tax planning and analysis.
    Input should be customer_id (integer).
    Returns ITR data in JSON format.
    """
    
    def _run(self, customer_id: str) -> str:
        """Fetch ITR data"""
        try:
            db = next(get_db())
            
            itr_data = db.query(ITRData).filter(
                ITRData.customer_id == int(customer_id)
            ).first()
            
            if not itr_data:
                return f"No ITR data found for customer {customer_id}"
            
            result = {
                "financial_year": itr_data.financial_year,
                "gross_total_income": itr_data.gross_total_income,
                "total_deductions": itr_data.total_deductions,
                "taxable_income": itr_data.taxable_income,
                "tax_paid": itr_data.tax_paid,
                "refund_due": itr_data.refund_due,
                "filing_status": itr_data.filing_status,
                "last_updated": itr_data.last_updated.isoformat() if itr_data.last_updated else None
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error fetching ITR data: {str(e)}"
        finally:
            db.close()


class PortfolioDataTool(BaseTool):
    """Tool for fetching portfolio data from AA data assets"""
    
    name: str = "portfolio_data_fetcher"
    description: str = """
    Fetches portfolio and investment data for a customer from AA data.
    Input should be customer_id (integer).
    Returns portfolio information in JSON format.
    """
    
    def _run(self, customer_id: str) -> str:
        """Fetch portfolio data from AA data"""
        try:
            db = next(get_db())
            
            # Get AA data which contains assets information
            aa_data = db.query(AAData).filter(
                AAData.customer_id == int(customer_id)
            ).first()
            
            if not aa_data:
                return f"No portfolio data found for customer {customer_id}"
            
            result = {
                "customer_id": customer_id,
                "assets": aa_data.assets,
                "account_summary": aa_data.account_summary,
                "spending_patterns": aa_data.spending_patterns,
                "created_at": aa_data.created_at.isoformat() if aa_data.created_at else None
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error fetching portfolio data: {str(e)}"
        finally:
            db.close()


# Initialize all tools
def get_database_tools() -> List[BaseTool]:
    """Get all database tools for agents"""
    return [
        CustomerDataTool(),
        AssetAllocationTool(),
        CreditDataTool(),
        NewsDataTool(),
        ITRDataTool(),
        PortfolioDataTool()
    ]
