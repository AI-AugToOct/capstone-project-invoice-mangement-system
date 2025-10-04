# backend/routers/vlm.py
import os
import json
import logging
import time
import requests
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from backend.database import get_db
from backend.models.invoice_model import Invoice
from backend.models.item_model import Item
from backend.utils import generate_embedding

# ================================================================
# ⚙️ Setup
# ================================================================
load_dotenv()
router = APIRouter(prefix="/vlm", tags=["VLM"])
logger = logging.getLogger("backend.vlm")

FRIENDLI_TOKEN = os.getenv("FRIENDLI_TOKEN")
FRIENDLI_URL = "https://api.friendli.ai/dedicated/v1/chat/completions"
FRIENDLI_MODEL_ID = "dep021qh0vlii5d"  # Qwen2.5-VL-32B-Instruct


# ================================================================
# 📦 Request Schema
# ================================================================
class VLMRequest(BaseModel):
    image_url: str
    prompt: str | None = None


# ================================================================
# 🧩 Helper Functions
# ================================================================
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


def parse_date(value):
    """Try to parse multiple date formats safely."""
    if not value or str(value).lower() in ["not mentioned", "none", "null", ""]:
        return None

    formats = [
        "%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value.strip(), fmt)
        except Exception:
            continue
    try:
        return datetime.fromisoformat(value.strip())
    except Exception:
        return None


# ================================================================
# 🏷️ Category Mapping (English → Arabic)
# ================================================================
CATEGORY_MAP = {
    "Cafe": "مقهى",
    "Restaurant": "مطعم",
    "Supermarket": "بقالة / تموينات",
    "Pharmacy": "صيدلية",
    "Clothing": "ملابس",
    "Electronics": "إلكترونيات",
    "Utility": "فاتورة خدمات",
    "Education": "تعليم",
    "Health": "صحة",
    "Transport": "مواصلات",
    "Delivery": "توصيل",
    "Other": "أخرى"
}


def normalize_category(cat):
    """Normalize category name to standardized English + Arabic version."""
    if not cat or str(cat).lower() in ["not mentioned", "none", "null", ""]:
        return {"en": "Other", "ar": CATEGORY_MAP["Other"]}
    for en, ar in CATEGORY_MAP.items():
        if en.lower() in str(cat).lower() or ar in str(cat):
            return {"en": en, "ar": ar}
    return {"en": "Other", "ar": CATEGORY_MAP["Other"]}


# ================================================================
# 🚀 Endpoint: Analyze Invoice
# ================================================================
@router.post("/analyze")
async def analyze_vlm(request: VLMRequest, db: Session = Depends(get_db)):
    """
    Analyze an invoice image using FriendliAI Qwen2.5-VL-32B-Instruct.
    Handles Arabic + English invoices and generates richer insights.
    """
    try:
        start_time = time.time()
        logger.info(f"🔍 Analyzing image: {request.image_url}")

        # ------------------------------------------------------------
        # 🧠 Smart Prompt (Arabic + English + Insight-rich)
        # ------------------------------------------------------------
        if not request.prompt:
            request.prompt = """
You are a multilingual vision-language model trained to analyze invoices.
The invoice image might be **in Arabic, English, or both** — you must read and understand all text accurately.

Your task:
1. Extract **structured invoice data**.
2. Detect **the type of business** (category).
3. Generate a **smart, meaningful insight** about the purchase behavior.

If any field is missing, unreadable, or not found, set it to "Not Mentioned".

Return **only one valid JSON object** with all these exact keys and structure:

{
  "Invoice Number": ...,
  "Date": ...,
  "Vendor": ...,
  "Tax Number": ...,
  "Cashier": ...,
  "Branch": ...,
  "Phone": ...,
  "Items": [
    {"description": ..., "quantity": ..., "unit_price": ..., "total": ...}
  ],
  "Subtotal": ...,
  "Tax": ...,
  "Total Amount": ...,
  "Grand Total (before tax)": ...,
  "Discounts": ...,
  "Payment Method": ...,
  "Amount Paid": ...,
  "Ticket Number": ...,
  "Category": ...,
  "AI_Insight": ...
}

### Rules:
- Output **valid JSON only** (no explanations or markdown).
- The text may be Arabic or English — translate Arabic terms into English for keys but keep vendor names as-is.
- Classify "Category" based on the business type:
  Cafe ☕, Restaurant 🍽️, Supermarket 🛒, Pharmacy 💊, Clothing 👕, Electronics 💻, Utility 💡, Education 🎓, Health 🏥, Transport 🚗, Delivery 📦, or Other.
- The "AI_Insight" must be 2–3 detailed sentences (in English) describing:
  - What type of business it is.
  - The nature of the purchase.
  - Spending behavior (e.g., discount, frequency, amount trend).
  Example:
  "This purchase is from a coffee shop located in Riyadh. The customer spent a moderate amount, similar to previous transactions. Frequent coffee purchases may indicate a daily habit."
- Always ensure numbers (Subtotal, Tax, Total, etc.) exactly match the printed values.
- Do NOT include any markdown or explanations — return clean JSON only.
"""

        # ------------------------------------------------------------
        # 🌐 Send to FriendliAI
        # ------------------------------------------------------------
        headers = {
            "Authorization": f"Bearer {FRIENDLI_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": FRIENDLI_MODEL_ID,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": request.prompt},
                        {"type": "image_url", "image_url": {"url": request.image_url}},
                    ],
                }
            ],
            "max_tokens": 16384,
            "temperature": 0.6,
            "top_p": 0.9,
        }

        response = requests.post(FRIENDLI_URL, headers=headers, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Friendli API error: {response.text}")

        data = response.json()
        raw_output = data["choices"][0]["message"]["content"].strip()

        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").replace("json", "", 1).strip()

        try:
            parsed = json.loads(raw_output)
        except Exception as e:
            logger.error(f"⚠️ JSON parse failed: {e}")
            return {"status": "error", "raw_output": raw_output}

        # ------------------------------------------------------------
        # 🧹 Normalize Data
        # ------------------------------------------------------------
        category_raw = safe_get(parsed, "Category", "category")
        normalized_category = normalize_category(category_raw)
        ai_insight = safe_get(parsed, "AI_Insight", "ai_insight", default="Not Mentioned")
        raw_date = safe_get(parsed, "Date", "date", "placed_at")
        parsed_date = parse_date(raw_date)

        # ------------------------------------------------------------
        # 💾 Save Invoice
        # ------------------------------------------------------------
        invoice = Invoice(
            invoice_number=safe_get(parsed, "Invoice Number", "invoice_number"),
            invoice_date=parsed_date,
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
            category=json.dumps(normalized_category, ensure_ascii=False),
            ai_insight=ai_insight,
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        # ------------------------------------------------------------
        # 🧾 Save Items
        # ------------------------------------------------------------
        items = safe_get(parsed, "Items", "items", default=[])
        if isinstance(items, list):
            for it in items:
                db.add(Item(
                    description=it.get("description", "Unknown Item"),
                    quantity=safe_int(it.get("quantity", 1)),
                    unit_price=safe_float(it.get("unit_price", 0.0)),
                    total=safe_float(it.get("total", 0.0)),
                    invoice_id=invoice.id
                ))
        db.commit()

        # ------------------------------------------------------------
        # 🔢 Generate Embedding
        # ------------------------------------------------------------
        generate_embedding(invoice.id, json.dumps(parsed, ensure_ascii=False), db)

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"✅ Invoice {invoice.id} processed in {elapsed}s")

        # ------------------------------------------------------------
        # 🧾 Final Response
        # ------------------------------------------------------------
        return {
            "status": "success",
            "invoice_id": invoice.id,
            "category": normalized_category,
            "ai_insight": ai_insight,
            "output": parsed,
            "time_taken_seconds": elapsed,
        }

    except Exception as e:
        logger.error(f"❌ VLM analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
