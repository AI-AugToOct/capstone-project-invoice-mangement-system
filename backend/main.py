import logging
from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import invoices, items, vlm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.main")

try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables created successfully.")
except Exception as e:
    logger.error(f"❌ Error creating tables: {e}")

app = FastAPI(
    title="Smart Invoice Management System",
    version="1.0.0",
    description="FastAPI backend with Supabase + HuggingFace VLM"
)

@app.get("/")
def root():
    return {"msg": "Hello from FastAPI + Supabase + VLM"}

app.include_router(invoices.router)
app.include_router(items.router)
app.include_router(vlm.router)
