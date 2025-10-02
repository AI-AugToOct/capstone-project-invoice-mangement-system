from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Connection strings from Supabase Dashboard
# Password: Invoce_123@ (URL-encoded as Invoce_123%40)
SUPABASE_DIRECT = "postgresql://postgres:Invoce_123%40@db.pcktfzshbxaljkbedrar.supabase.co:5432/postgres"
SUPABASE_TRANSACTION_POOLER = "postgresql://postgres.pcktfzshbxaljkbedrar:Invoce_123%40@aws-1-eu-central-1.pooler.supabase.com:6543/postgres"
SUPABASE_SESSION_POOLER = "postgresql://postgres.pcktfzshbxaljkbedrar:Invoce_123%40@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"
SQLITE_URL = "sqlite:///./invoices.db"

# Try Supabase connections in order of preference, fallback to SQLite
def create_database_engine():
    # List of connection strings to try (in order of preference for FastAPI)
    connection_options = [
        ("Session Pooler (Best for FastAPI)", SUPABASE_SESSION_POOLER), 
        ("Transaction Pooler", SUPABASE_TRANSACTION_POOLER),
        ("Direct Connection", SUPABASE_DIRECT)
    ]
    
    for name, url in connection_options:
        try:
            print(f"Attempting {name} to Supabase...")
            print(f"URL: {url.replace('Invoce_123%40', '[PASSWORD]')}")  # Hide password in logs
            
            engine = create_engine(url)
            # Test the connection with proper SQLAlchemy text()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print(f"{name}: Connection successful!")
                
                # Test if we can access the invoices table
                try:
                    result = conn.execute(text("SELECT COUNT(*) FROM invoices"))
                    count = result.fetchone()[0]
                    print(f"Found {count} invoices in Supabase database")
                    print(f"SUCCESS! Connected to Supabase via {name}")
                except Exception as e:
                    print(f"Warning: Could not access invoices table: {e}")
                
                return engine
                
        except Exception as e:
            print(f"{name} failed: {e}")
            continue
    
    # If all Supabase connections fail, fall back to SQLite
    print("All Supabase connections failed, falling back to local SQLite database...")
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    print("Using local SQLite database!")
    return engine

# Create engine with fallback
engine = create_database_engine()

#Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for models
Base = declarative_base()