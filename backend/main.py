# backend/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.routers import vlm, upload, chat, dashboard, invoices, items

# --------------------------
# Logging setup
# --------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.main")

# --------------------------
# FastAPI app
# --------------------------
app = FastAPI(
    title="📑 Smart Invoice Analyzer API",
    version="1.0.0",
    description="Backend for analyzing invoices using Supabase + HuggingFace VLM",
)

# --------------------------
# CORS Middleware
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000",  # Docker
        "http://localhost:8501",  # Streamlit
        "https://*.vercel.app",  # Vercel deployments
        "*",  # Allow all in development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Health & Root Endpoints (for Railway)
# --------------------------
@app.get("/")
def root():
    """Root endpoint - confirms API is running"""
    return {"status": "✅ Smart Invoice Analyzer is running successfully!"}

@app.get("/healthz")
def health_check():
    """Health check endpoint for Railway"""
    return {"ok": True}

# --------------------------
# Routers
# --------------------------
app.include_router(upload.router)
app.include_router(vlm.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(invoices.router)
app.include_router(items.router)

# --------------------------
# Startup event
# --------------------------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting FastAPI...")
    logger.info("📊 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables ready!")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        logger.error(f"   Make sure DATABASE_URL is correct and Supabase is accessible")
        # Don't crash the app - let it start for debugging
        logger.warning("⚠️  Continuing startup without tables...")
