import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env vars
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "invoices"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Missing Supabase credentials in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter(prefix="/upload", tags=["Upload"])
logger = logging.getLogger("backend.upload")

@router.post("/")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        logger.info(f"⬆️ Uploading {file.filename} to Supabase...")

        file_bytes = await file.read()
        file_path = f"{file.filename}"

       
        res = supabase.storage.from_(BUCKET_NAME).upload(file_path, file_bytes)

        if "error" in str(res).lower():
            raise HTTPException(status_code=400, detail=f"Upload failed: {res}")

        # Build proper public URL
        # Format: https://[PROJECT].supabase.co/storage/v1/object/public/invoices/filename.jpg
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
        logger.info(f"✅ Uploaded successfully: {public_url}")

        return {"url": public_url}

    except Exception as e:
        logger.error(f"❌ Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
