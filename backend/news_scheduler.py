import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import sessionmaker
from database import engine
from news_intelligence import news_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class NewsScheduler:
    """
    Scheduler for automatic news updates
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    async def fetch_news_job(self):
        """Scheduled job to fetch and update news"""
        logger.info("Starting scheduled news fetch...")
        
        try:
            # Create database session
            db = SessionLocal()
            
            # Run news update
            result = await news_agent.update_news_feed(db)
            logger.info(f"News update completed: {result}")
            
        except Exception as e:
            logger.error(f"Error in scheduled news fetch: {e}")
        finally:
            db.close()
    
    def start_scheduler(self):
        """Start the news scheduler"""
        if self.is_running:
            return
        
        # Schedule news updates every 4 hours
        self.scheduler.add_job(
            self.fetch_news_job,
            trigger=IntervalTrigger(hours=4),
            id='news_update_job',
            name='Fetch Financial News',
            replace_existing=True
        )
        
        # Also run once at startup (with a small delay)
        self.scheduler.add_job(
            self.fetch_news_job,
            trigger='date',
            run_date=datetime.now(),
            id='startup_news_fetch',
            name='Startup News Fetch'
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("News scheduler started - will fetch news every 4 hours")
    
    def stop_scheduler(self):
        """Stop the news scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("News scheduler stopped")

# Global scheduler instance
news_scheduler = NewsScheduler()

# Function to run manual news update
async def run_manual_update():
    """Run a manual news update"""
    db = SessionLocal()
    try:
        result = await news_agent.update_news_feed(db)
        print(f"Manual news update completed: {result}")
        return result
    except Exception as e:
        print(f"Error in manual news update: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    # Run manual update when script is executed directly
    asyncio.run(run_manual_update())
