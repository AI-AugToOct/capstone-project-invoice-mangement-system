,import logging
from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import invoices, vlm

# إعداد اللوقز
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء الجداول (لو مش موجودة)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables created successfully.")
except Exception as e:
    logger.error(f"❌ Error creating tables: {e}")

# تعريف التطبيق
app = FastAPI(
    title="Smart Invoice Management System",
    version="1.0.0",
    description="FastAPI backend with Supabase + HuggingFace VLM"
)

@app.get("/")
def root():
    return {"msg": "Hello from FastAPI + Supabase + HuggingFace VLM"}

# تضمين الراوترات
app.include_router(invoices.router)
app.include_router(vlm.router)
