import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
from models import Base
from database import engine

# Load environment variables
load_dotenv()

def create_database():
    # Database connection parameters
    dbname = "postgres"
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    target_db = os.getenv("POSTGRES_DB")

    # Connect to default postgres database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Check if database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{target_db}'")
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Creating database {target_db}")
        cursor.execute(f'CREATE DATABASE {target_db}')
    else:
        print(f"Database {target_db} already exists")

    cursor.close()
    conn.close()

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_database()
    create_tables() 