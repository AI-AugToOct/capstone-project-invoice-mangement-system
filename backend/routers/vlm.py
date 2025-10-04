import os
import json
import logging
import time
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from openai import OpenAI

from backend.database import get_db
from backend.models.invoice_model import Invoice
from backend.models.item_model import Item
from backend.utils import generate_embedding  

load_dotenv()
router = APIRouter(prefix="/vlm", tags=["VLM"])

logger = logging.getLogger("backend.vlm")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

class VLMRequest(BaseModel):
    image_url: str
    prompt: str

# ===== Helpers =====
def safe_get(parsed: dict, *keys, default=None):
   
    for k in keys:
        if isinstance(parsed, dict) and k in parsed:
            return parsed[k]
    return default

def safe_int(value, default=1):
   
    try:
        if value is None:
            return default
        return int(str(value).replace("x", "").strip())
    except Exception:
        return default

def safe_float(value, default=0.0):
   
    try:
        if value is None:
            return default
        return float(str(value).replace(",", "").replace("-", "").strip())
    except Exception:
        return default


@router.post("/analyze")
async def analyze_vlm(request: VLMRequest, db: Session = Depends(get_db)):
    try:
        start_time = time.time()
        logger.info(f"🔍 Analyzing image: {request.image_url}")

        
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": request.prompt},
                    {"type": "image_url", "image_url": {"url": request.image_url}},
                ],
            }],
        )

        raw_output = completion.choices[0].message.content.strip()
        logger.info(f"📝 Raw output: {raw_output}")

      
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`")
            raw_output = raw_output.replace("json", "", 1).strip()

        
        try:
            parsed = json.loads(raw_output)
        except Exception as e:
            logger.error(f"⚠️ Failed to parse JSON: {e}")
            return {
                "status": "error",
                "message": "VLM did not return valid JSON",
                "raw_output": raw_output
            }

        
        invoice = Invoice(
            invoice_number=safe_get(parsed, "Invoice Number", "invoice_number"),
            invoice_date=safe_get(parsed, "Date", "date", "placed_at"),
            vendor=safe_get(parsed, "Vendor", "vendor"),
            tax_number=safe_get(parsed, "Tax Number", "tax_number"),
            cashier=safe_get(parsed, "Cashier", "cashier"),
            branch=safe_get(parsed, "Branch", "branch"),
            phone=safe_get(parsed, "Phone", "phone"),
            subtotal=safe_float(safe_get(parsed, "Subtotal", "sub_total")),
            tax=safe_float(safe_get(parsed, "Tax", "total_taxes")),
            total_amount=safe_float(safe_get(parsed, "Total Amount", "bill_total_value")),
            grand_total=safe_float(safe_get(parsed, "Grand Total (before tax)", "grand_total")),
            discounts=safe_float(safe_get(parsed, "Discounts", "discount")),
            payment_method=safe_get(parsed, "Payment Method", "payment_method", "paid_by"),
            amount_paid=safe_float(safe_get(parsed, "Amount Paid", "amount_paid")),
            ticket_number=safe_get(parsed, "Ticket Number", "ticket_number"),
            category=safe_get(parsed, "Category", "category"),
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        
        items = []

        order_items = safe_get(parsed, "Items", "items", "order", default=[])
        if isinstance(order_items, list):
            for it in order_items:
                items.append({
                    "description": it.get("item") or it.get("description") or "Unknown Item",
                    "quantity": safe_int(it.get("quantity", 1)),
                    "unit_price": safe_float(it.get("unit_price", 0.0)),
                    "total": safe_float(it.get("total", 0.0))
                })

        add_on_items = safe_get(parsed, "add_ons", "Add_ons", "addons", default=[])
        if isinstance(add_on_items, list):
            for it in add_on_items:
                items.append({
                    "description": it.get("item") or "Unknown Item",
                    "quantity": safe_int(it.get("quantity", 1)),
                    "unit_price": 0.0,
                    "total": 0.0
                })

        for item in items:
            db_item = Item(
                description=item["description"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total=item["total"],
                invoice_id=invoice.id
            )
            db.add(db_item)
        db.commit()

    
        text_for_embedding = f"Vendor: {invoice.vendor}, Items: {[i['description'] for i in items]}, Total: {invoice.total_amount}, Date: {invoice.invoice_date}"
        generate_embedding(invoice.id, text_for_embedding, db)

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"✅ VLM + DB + Embedding done in {elapsed} sec")

        return {
            "status": "success",
            "invoice_id": invoice.id,
            "output": parsed,
            "time_taken_seconds": elapsed
        }

    except Exception as e:
        logger.error(f"❌ VLM analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
