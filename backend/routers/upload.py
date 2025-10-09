import os
import logging
import io
import requests
from fastapi import APIRouter, UploadFile, File, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from PIL import Image
import fitz  # PyMuPDF

# Load env vars
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "invoices"

# Use service role key for admin operations (upload/delete)
SUPABASE_KEY = SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Missing Supabase credentials in .env")

router = APIRouter(prefix="/upload", tags=["Upload"])
logger = logging.getLogger("backend.upload")

# Log which key is being used (masked for security)
if SUPABASE_SERVICE_KEY:
    logger.info(f"🔑 Using SERVICE ROLE KEY: ...{SUPABASE_SERVICE_KEY[-10:]}")
else:
    logger.warning(f"⚠️ Using ANON KEY (may have limited permissions): ...{SUPABASE_ANON_KEY[-10:] if SUPABASE_ANON_KEY else 'NOT SET'}")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pdf_to_image(pdf_bytes: bytes) -> bytes:
    """
    Convert the first page of a PDF to a JPEG image.
    Returns image bytes.
    """
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Get first page
        first_page = pdf_document[0]
        
        # Render page to image at 300 DPI for good quality
        zoom = 2  # Higher zoom = higher resolution
        mat = fitz.Matrix(zoom, zoom)
        pix = first_page.get_pixmap(matrix=mat)
        
        # Convert pixmap to PIL Image
        img_data = pix.tobytes("jpeg")
        
        pdf_document.close()
        
        logger.info(f"✅ Successfully converted PDF to image")
        return img_data
    
    except Exception as e:
        logger.error(f"❌ PDF conversion error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to convert PDF: {str(e)}")

@router.post("/")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        logger.info(f"⬆️ Uploading {file.filename} to Supabase...")

        file_bytes = await file.read()
        original_filename = file.filename or "invoice"
        
        # Check if file is a PDF
        is_pdf = file.content_type == "application/pdf" or original_filename.lower().endswith('.pdf')
        
        if is_pdf:
            logger.info(f"📄 Detected PDF file, converting to image...")
            # Convert PDF to image
            file_bytes = pdf_to_image(file_bytes)
            # Change filename extension to .jpg
            file_path = original_filename.rsplit('.', 1)[0] + ".jpg"
            content_type = "image/jpeg"
        else:
            file_path = original_filename
            content_type = file.content_type or "image/jpeg"
        
        # Upload using REST API directly (more reliable than supabase-py)
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{file_path}"
        
        headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": content_type,
            "x-upsert": "true"  # Overwrite if exists
        }
        
        try:
            logger.info(f"📤 Uploading to: {upload_url}")
            logger.info(f"🔑 Using key ending with: ...{SUPABASE_KEY[-10:]}")
            
            response = requests.post(
                upload_url,
                data=file_bytes,
                headers=headers,
                timeout=30
            )
            
            if response.status_code not in [200, 201]:
                logger.error(f"❌ Upload failed: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Upload failed: {response.text}"
                )
            
            logger.info(f"✅ Upload successful: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Upload request failed: {str(e)}")

        # Build proper public URL
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
        logger.info(f"✅ File available at: {public_url}")

        return {"url": public_url, "converted_from_pdf": is_pdf}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
