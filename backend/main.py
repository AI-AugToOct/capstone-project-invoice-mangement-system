# backend/main.py
import logging
from fastapi import FastAPI
from .database import Base, engine
from .routers import vlm, upload, chat, dashboard, invoices  # ✅ أضفنا invoices هنا

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
# Routers
# --------------------------
app.include_router(upload.router)
app.include_router(vlm.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(invoices.router)  # ✅ الآن المسار موجود

# --------------------------
# Startup event
# --------------------------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting FastAPI...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created successfully.")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")

# --------------------------
# Root endpoint
# --------------------------
@app.get("/")
def root():
    return {"message": "Hello from FastAPI + Supabase + HuggingFace VLM 🚀"}
