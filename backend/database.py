from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("backend.database")

# Get DATABASE_URL and ensure proper format
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

# Strip any accidental "DATABASE_URL=" prefix
if DATABASE_URL.startswith("DATABASE_URL="):
    DATABASE_URL = DATABASE_URL.replace("DATABASE_URL=", "")

# Ensure SSL and encoding parameters are in the URL
if "?" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require&client_encoding=utf8"
else:
    if "sslmode" not in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    if "client_encoding" not in DATABASE_URL:
        DATABASE_URL += "&client_encoding=utf8"

logger.info(f"🔗 Connecting to database (host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'})")

# Create engine with proper configuration for Supabase
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Disable connection pooling for serverless
    echo=False,
    connect_args={
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
)

# Test connection on startup
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT now()"))
        db_time = result.scalar()
        logger.info(f"✅ Database connected successfully! DB Time: {db_time}")
except Exception as e:
    logger.error(f"❌ Database connection failed: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
