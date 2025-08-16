import asyncio
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from duckduckgo_search import DDGS
from textblob import TextBlob

from database import get_db
from models import NewsArticle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsIntelligenceAgent:
    """
    News Intelligence Agent for fetching, analyzing, and storing financial news
    """
    
    def __init__(self):
        self.financial_keywords = [
            "stocks", "market", "economy", "inflation", "GDP", "Federal Reserve", 
            "interest rates", "earnings", "revenue", "profit", "financial",
            "investment", "trading", "NYSE", "NASDAQ", "S&P 500", "Dow Jones",
            "bonds", "commodities", "crypto", "bitcoin", "ethereum",
            "tech stocks", "healthcare", "energy", "banking", "real estate"
        ]
        
        self.company_symbols = {
            "Apple": "AAPL", "Microsoft": "MSFT", "Amazon": "AMZN", "Google": "GOOGL",
            "Tesla": "TSLA", "Meta": "META", "Netflix": "NFLX", "NVIDIA": "NVDA",
            "JPMorgan": "JPM", "Goldman Sachs": "GS", "Bank of America": "BAC",
            "Wells Fargo": "WFC", "Citigroup": "C", "Morgan Stanley": "MS"
        }
    
    def extract_stock_symbols(self, text: str) -> List[str]:
        """Extract stock symbols from text"""
        symbols = []
        
        # Look for explicit mentions of companies
        for company, symbol in self.company_symbols.items():
            if company.lower() in text.lower():
                symbols.append(symbol)
        
        # Look for stock symbols in format $SYMBOL or SYMBOL:
        symbol_pattern = r'\$([A-Z]{1,5})\b|([A-Z]{1,5}):'
        matches = re.findall(symbol_pattern, text)
        for match in matches:
            symbol = match[0] or match[1]
            if len(symbol) <= 5:  # Valid stock symbols are usually 1-5 characters
                symbols.append(symbol)
        
        return list(set(symbols))  # Remove duplicates
    
    def categorize_article(self, title: str, snippet: str) -> str:
        """Categorize news article based on content"""
        content = f"{title} {snippet}".lower()
        
        if any(word in content for word in ["technology", "tech", "ai", "artificial intelligence", "software"]):
            return "technology"
        elif any(word in content for word in ["healthcare", "pharma", "medical", "biotech"]):
            return "healthcare"
        elif any(word in content for word in ["energy", "oil", "gas", "renewable", "solar"]):
            return "energy"
        elif any(word in content for word in ["bank", "financial", "credit", "loan", "mortgage"]):
            return "financial"
        elif any(word in content for word in ["federal reserve", "fed", "interest rate", "inflation", "gdp"]):
            return "economy"
        elif any(word in content for word in ["market", "trading", "stock", "nasdaq", "dow"]):
            return "markets"
        else:
            return "general"
    
    def analyze_sentiment(self, text: str) -> tuple[float, str]:
        """Analyze sentiment of the text using TextBlob"""
        try:
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity  # -1 to 1
            
            if sentiment_score > 0.1:
                sentiment_label = "positive"
            elif sentiment_score < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return sentiment_score, sentiment_label
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 0.0, "neutral"
    
    def calculate_impact_score(self, title: str, snippet: str, symbols: List[str]) -> float:
        """Calculate the potential market impact score (0-1)"""
        impact_score = 0.0
        content = f"{title} {snippet}".lower()
        
        # High impact keywords
        high_impact_words = [
            "federal reserve", "fed", "interest rate", "inflation", "gdp", 
            "unemployment", "earnings", "bankruptcy", "merger", "acquisition",
            "ipo", "stock split", "dividend", "recession", "bull market", "bear market"
        ]
        
        # Count high impact words
        for word in high_impact_words:
            if word in content:
                impact_score += 0.15
        
        # Add score for stock symbols mentioned
        impact_score += len(symbols) * 0.1
        
        # Boost score for major financial publications
        if any(source in content for source in ["wall street journal", "financial times", "bloomberg", "reuters"]):
            impact_score += 0.2
        
        return min(impact_score, 1.0)  # Cap at 1.0
    
    def extract_keywords(self, title: str, snippet: str) -> List[str]:
        """Extract relevant financial keywords from the text"""
        content = f"{title} {snippet}".lower()
        found_keywords = []
        
        for keyword in self.financial_keywords:
            if keyword.lower() in content:
                found_keywords.append(keyword)
        
        return found_keywords
    
    async def fetch_news_articles(self, queries: List[str], max_results: int = 10) -> List[Dict]:
        """Fetch news articles from DuckDuckGo for given queries"""
        all_articles = []
        
        try:
            with DDGS() as ddgs:
                for query in queries:
                    logger.info(f"Fetching news for query: {query}")
                    
                    # Add financial context to queries
                    financial_query = f"{query} financial market stock economy"
                    
                    try:
                        news_results = ddgs.news(
                            keywords=financial_query,
                            region="us-en",
                            safesearch="moderate",
                            timelimit="d",  # Last day
                            max_results=max_results
                        )
                        
                        for article in news_results:
                            if article not in all_articles:  # Avoid duplicates
                                all_articles.append(article)
                    
                    except Exception as e:
                        logger.error(f"Error fetching news for query '{query}': {e}")
                        continue
                
                # Remove duplicates based on URL
                unique_articles = []
                seen_urls = set()
                for article in all_articles:
                    if article.get('url') not in seen_urls:
                        unique_articles.append(article)
                        seen_urls.add(article.get('url'))
                
                logger.info(f"Fetched {len(unique_articles)} unique articles")
                return unique_articles
                
        except Exception as e:
            logger.error(f"Error in fetch_news_articles: {e}")
            return []
    
    def process_and_store_articles(self, articles: List[Dict], db: Session) -> int:
        """Process and store articles in the database"""
        stored_count = 0
        
        for article_data in articles:
            try:
                # Extract basic information
                title = article_data.get('title', '')
                url = article_data.get('url', '')
                source = article_data.get('source', '')
                snippet = article_data.get('body', '')
                
                if not all([title, url, snippet]):
                    logger.warning(f"Skipping article with missing data: {title}")
                    continue
                
                # Parse date
                date_str = article_data.get('date', '')
                try:
                    published_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except:
                    published_date = datetime.utcnow()
                
                # Process article content
                symbols = self.extract_stock_symbols(f"{title} {snippet}")
                category = self.categorize_article(title, snippet)
                sentiment_score, sentiment_label = self.analyze_sentiment(f"{title} {snippet}")
                impact_score = self.calculate_impact_score(title, snippet, symbols)
                keywords = self.extract_keywords(title, snippet)
                
                # Create news article object
                news_article = NewsArticle(
                    title=title,
                    url=url,
                    source=source,
                    published_date=published_date,
                    snippet=snippet[:1000],  # Limit snippet length
                    body=snippet,
                    category=category,
                    symbols=symbols,
                    sentiment_score=sentiment_score,
                    sentiment_label=sentiment_label,
                    impact_score=impact_score,
                    market_region="US",
                    keywords=keywords,
                    is_active=True
                )
                
                # Store in database
                db.add(news_article)
                db.commit()
                stored_count += 1
                
                logger.info(f"Stored article: {title[:50]}...")
                
            except IntegrityError:
                # Article already exists (duplicate URL)
                db.rollback()
                logger.info(f"Article already exists: {title[:50]}...")
                continue
            except Exception as e:
                db.rollback()
                logger.error(f"Error storing article '{title}': {e}")
                continue
        
        return stored_count
    
    async def update_news_feed(self, db: Session = None) -> Dict:
        """Main method to fetch and update news feed"""
        if db is None:
            db = next(get_db())
        
        # Define search queries for financial news
        queries = [
            "stock market",
            "federal reserve",
            "economic indicators",
            "earnings report",
            "tech stocks",
            "cryptocurrency",
            "oil prices",
            "inflation data",
            "interest rates",
            "market volatility"
        ]
        
        try:
            # Fetch articles
            articles = await self.fetch_news_articles(queries, max_results=5)
            
            if not articles:
                return {"status": "error", "message": "No articles fetched"}
            
            # Process and store articles
            stored_count = self.process_and_store_articles(articles, db)
            
            # Clean up old articles (older than 7 days)
            cutoff_date = datetime.utcnow() - timedelta(days=7)
            old_articles = db.query(NewsArticle).filter(
                NewsArticle.published_date < cutoff_date
            ).update({"is_active": False})
            db.commit()
            
            return {
                "status": "success",
                "fetched": len(articles),
                "stored": stored_count,
                "archived": old_articles or 0
            }
            
        except Exception as e:
            logger.error(f"Error in update_news_feed: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            db.close()

# Global instance
news_agent = NewsIntelligenceAgent()
