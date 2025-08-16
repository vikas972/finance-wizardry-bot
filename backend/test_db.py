from sqlalchemy import create_engine
from database import SQLALCHEMY_DATABASE_URL
from models import Base

def test_db_connection():
    try:
        # Create test engine
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        # Try to create all tables
        Base.metadata.create_all(bind=engine)
        
        print("Database connection successful!")
        print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")
        
        # Test if tables exist
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        print("\nAvailable tables:")
        for table in tables:
            print(f"- {table}")
            
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_db_connection() 