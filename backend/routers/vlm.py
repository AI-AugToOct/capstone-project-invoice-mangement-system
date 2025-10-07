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
أنت نموذج ذكاء اصطناعي متعدد اللغات مدرب على تحليل الفواتير.
الفاتورة قد تكون بالعربية، الإنجليزية، أو كليهما - يجب أن تقرأ وتفهم جميع النصوص بدقة.

مهمتك:
1. استخراج بيانات الفاتورة المنظمة.
2. تحديد نوع النشاط التجاري (التصنيف).
3. **كشف نوع الفاتورة (Invoice Type)** بناءً على الكلمات المفتاحية والمؤشرات البصرية.
4. استخراج الكلمات المفتاحية (بالعربية والإنجليزية) التي تساعد في تحديد نوع الفاتورة.
5. إنشاء رؤية ذكية ومفيدة باللغة العربية عن سلوك الشراء.

⚠️ مهم جداً: يجب أن يكون حقل "AI_Insight" باللغة العربية فقط ويصف الشراء بشكل مفيد للمستخدم.

إذا كان أي حقل مفقود أو غير قابل للقراءة، اكتبه كـ "Not Mentioned".

أرجع **فقط** كائن JSON واحد صحيح بهذه المفاتيح والبنية بالضبط:

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
  "Keywords_Detected": [...],
  "Invoice_Type": "...",
  "AI_Insight": "..." (يجب أن يكون بالعربية)
}

### القواعد:

**1. تحديد نوع الفاتورة (Invoice_Type):**
ابحث عن الكلمات المفتاحية التالية في الفاتورة (بالعربية أو الإنجليزية):

- **فاتورة شراء**: إذا وجدت كلمات مثل:
  - شراء، Purchase, Buy, Sale, Receipt, Bill, Tax Invoice (for purchases)
  
- **فاتورة ضمان**: إذا وجدت كلمات مثل:
  - ضمان، Warranty, Guarantee, Coverage, Protection Plan, Extended Warranty
  
- **فاتورة صيانة**: إذا وجدت كلمات مثل:
  - صيانة، Maintenance, Service, Repair, Fixing, Servicing, Check-up
  
- **فاتورة ضريبية**: إذا وجدت كلمات مثل:
  - فاتورة ضريبية، Tax Invoice, VAT Invoice, الرقم الضريبي (مع عدم وجود مشتريات واضحة)
  
- **أخرى**: إذا لم تجد أي من الكلمات السابقة أو كان نوع الفاتورة غير واضح

**قواعد مهمة لتحديد النوع:**
- اختر النوع الأكثر تحديداً إذا ظهرت مؤشرات متعددة
- إذا كانت فاتورة تحتوي على "Tax Invoice" لكن بها مشتريات واضحة → اختر "فاتورة شراء"
- إذا كانت فاتورة صيانة وضمان معاً → اختر "فاتورة صيانة" (الأكثر تحديداً)
- لا تخمن عشوائياً - إذا لم تكن متأكداً → اختر "أخرى"

⚠️ **مهم جداً:** يجب أن يكون "Invoice_Type" باللغة العربية فقط (مثال: "فاتورة شراء" وليس "Purchase Invoice")

**2. الكلمات المفتاحية (Keywords_Detected):**
استخرج قائمة بالكلمات المفتاحية التي وجدتها في الفاتورة والتي ساعدت في تحديد نوع الفاتورة.
مثال: ["شراء", "Purchase", "فاتورة ضريبية", "Tax Invoice"]

**3. تصنيف النشاط التجاري (Category):**
صنّف "Category" بناءً على نوع النشاط التجاري:
  Cafe ☕, Restaurant 🍽️, Supermarket 🛒, Pharmacy 💊, Clothing 👕, Electronics 💻, Utility 💡, Education 🎓, Health 🏥, Transport 🚗, Delivery 📦, أو Other.

**4. الرؤية الذكية (AI_Insight):**
يجب أن يكون "AI_Insight" من 2-3 جمل تفصيلية **بالعربية فقط** تصف:
  - نوع النشاط التجاري.
  - طبيعة المشتريات.
  - سلوك الإنفاق (مثل: خصم، تكرار، اتجاه المبلغ).
  مثال:
  "هذا الشراء من مطعم Keeta في كانتون. العميل طلب وجبتين بمبلغ معتدل. المشتريات المتكررة من المطاعم قد تشير إلى عادة يومية."

**5. دقة البيانات:**
- تأكد دائماً أن الأرقام (Subtotal, Tax, Total, إلخ) تطابق القيم المطبوعة بالضبط.
- أرجع **JSON صحيح فقط** (بدون شروحات أو markdown).
- النص قد يكون بالعربية أو الإنجليزية - ترجم المصطلحات العربية للمفاتيح لكن احتفظ بأسماء المتاجر كما هي.
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
        
        # 🔍 Extract Invoice Type and Keywords from VLM response
        invoice_type_from_vlm = safe_get(parsed, "Invoice_Type", "invoice_type", default="Other")
        keywords_detected = safe_get(parsed, "Keywords_Detected", "keywords_detected", default=[])
        
        # Log detected keywords for debugging
        logger.info(f"🔑 Keywords detected: {keywords_detected}")
        logger.info(f"📋 Invoice type from VLM: {invoice_type_from_vlm}")

        # ------------------------------------------------------------
        # 💾 Save Invoice
        # ------------------------------------------------------------
        # 🧾 Use invoice_type from VLM if available, otherwise fallback to category
        invoice_type_ar = invoice_type_from_vlm if invoice_type_from_vlm != "Other" else normalized_category.get("ar", "شراء")
        
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
            invoice_type=invoice_type_ar,  # نوع الفاتورة بالعربية
            image_url=request.image_url,  # حفظ رابط الصورة من Supabase
        )
        
        logger.info(f"🧾 Stored invoice_type: {invoice_type_ar}")
        logger.info(f"🖼️ Stored image_url: {request.image_url}")

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
