import logging
import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from backend.database import get_db
from backend.models.invoice_model import Invoice
from backend.models.item_model import Item
from backend.schemas.invoice_schema import InvoiceCreate
from backend.utils import generate_embedding

router = APIRouter(prefix="/invoices", tags=["Invoices"])
logger = logging.getLogger(__name__)


# Schema for item data
class ItemData(BaseModel):
    description: str = ""
    quantity: float = 1
    unit_price: float = 0
    total: float = 0

# Schema for edited invoice data
class EditedInvoiceData(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    tax_number: str = ""
    cashier: str = ""
    branch: str = ""
    phone: str = ""
    ticket_number: str = ""
    subtotal: str = "0"
    tax: str = "0"
    total_amount: str = "0"
    grand_total: str = "0"
    discounts: str = "0"
    amount_paid: str = "0"
    payment_method: str = ""
    invoice_type: str = "فاتورة شراء"
    category: dict = {"ar": "أخرى", "en": "Other"}
    ai_insight: str = ""
    image_url: str = ""
    items: list[ItemData] = []  # إضافة Items

# ------------------------------------------------------------
# ✅ POST /invoices/save-analyzed → Save edited invoice data
# ------------------------------------------------------------
@router.post("/save-analyzed")
def save_analyzed_invoice(data: EditedInvoiceData, db: Session = Depends(get_db)):
    """
    Save invoice data after user review and editing.
    This is called after VLM analysis and user confirmation.
    """
    try:
        logger.info(f"💾 Saving edited invoice: {data.vendor}")
        
        # Parse date
        def parse_date(value):
            if not value or str(value).lower() in ["not mentioned", "none", "null", ""]:
                logger.warning(f"⚠️ Date value is empty or 'not mentioned': {value}")
                return None
            
            # Log the incoming date value
            logger.info(f"📅 Parsing date: {value} (type: {type(value)})")
            
            # Convert to string if needed
            value_str = str(value).strip()
            
            # List of common date formats
            formats = [
                "%d/%m/%Y",      # 09/10/2025
                "%Y-%m-%d",      # 2025-10-09
                "%m/%d/%Y",      # 10/09/2025
                "%d-%m-%Y",      # 09-10-2025
                "%Y/%m/%d",      # 2025/10/09
                "%d %B %Y",      # 09 October 2025
                "%d %b %Y",      # 09 Oct 2025
                "%B %d, %Y",     # October 09, 2025
                "%b %d, %Y",     # Oct 09, 2025
                "%d.%m.%Y",      # 09.10.2025
            ]
            
            for fmt in formats:
                try:
                    parsed = datetime.strptime(value_str, fmt)
                    logger.info(f"✅ Date parsed successfully using format '{fmt}': {parsed}")
                    return parsed
                except:
                    continue
            
            # Try ISO format
            try:
                parsed = datetime.fromisoformat(value_str)
                logger.info(f"✅ Date parsed successfully using ISO format: {parsed}")
                return parsed
            except:
                pass
            
            # If all parsing attempts fail
            logger.error(f"❌ Failed to parse date: {value}")
            return None
        
        # Convert string numbers to float
        def safe_float(value):
            try:
                if not value or str(value).lower() in ["not mentioned", "none", "null", ""]:
                    return 0.0
                return float(str(value).replace(",", "").strip())
            except:
                return 0.0
        
        parsed_date = parse_date(data.date)
        logger.info(f"📆 Final parsed date for saving: {parsed_date}")
        
        # Create invoice
        invoice = Invoice(
            invoice_number=data.invoice_number or "Not Mentioned",
            invoice_date=parsed_date,
            vendor=data.vendor or "Not Mentioned",
            tax_number=data.tax_number or "Not Mentioned",
            cashier=data.cashier or "Not Mentioned",
            branch=data.branch or "Not Mentioned",
            phone=data.phone or "Not Mentioned",
            ticket_number=data.ticket_number or "Not Mentioned",
            subtotal=str(safe_float(data.subtotal)),
            tax=str(safe_float(data.tax)),
            total_amount=str(safe_float(data.total_amount)),
            grand_total=str(safe_float(data.grand_total)),
            discounts=str(safe_float(data.discounts)),
            amount_paid=str(safe_float(data.amount_paid)),
            payment_method=data.payment_method or "Not Mentioned",
            invoice_type=data.invoice_type,
            category=json.dumps(data.category, ensure_ascii=False),
            ai_insight=data.ai_insight or "Not Mentioned",
            image_url=data.image_url,
        )
        
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        
        # ✅ Save Items if provided
        if data.items and len(data.items) > 0:
            for item_data in data.items:
                # تجاهل Items الفارغة
                if item_data.description.strip():
                    item = Item(
                        invoice_id=invoice.id,
                        description=item_data.description,
                        quantity=int(item_data.quantity),
                        unit_price=float(item_data.unit_price),
                        total=float(item_data.total),
                    )
                    db.add(item)
            db.commit()
            logger.info(f"✅ Saved {len(data.items)} items for invoice {invoice.id}")
        
        # Generate embedding for semantic search
        invoice_text = json.dumps({
            "vendor": data.vendor,
            "category": data.category,
            "invoice_type": data.invoice_type,
            "total_amount": data.total_amount,
            "date": data.date,
        }, ensure_ascii=False)
        
        generate_embedding(invoice.id, invoice_text, db)
        
        logger.info(f"✅ Invoice saved successfully: ID {invoice.id}")
        
        # Return in format expected by InvoiceResultCard
        return {
            "status": "success",
            "invoice_id": invoice.id,
            "category": data.category,
            "invoice_type": data.invoice_type,
            "ai_insight": data.ai_insight,
            "output": {
                "Invoice Number": data.invoice_number,
                "Date": data.date,
                "Vendor": data.vendor,
                "Tax Number": data.tax_number,
                "Cashier": data.cashier,
                "Branch": data.branch,
                "Phone": data.phone,
                "Subtotal": data.subtotal,
                "Tax": data.tax,
                "Total Amount": data.total_amount,
                "Discounts": data.discounts,
                "Payment Method": data.payment_method,
            }
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error saving invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving invoice: {str(e)}")


# ------------------------------------------------------------
# ✅ POST /invoices → Create new invoice
# ------------------------------------------------------------
@router.post("/")
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        last_record = db.query(Invoice).order_by(Invoice.record.desc()).first()
        next_record = 1 if not last_record else (last_record.record or 0) + 1

        invoice = Invoice(
            record=next_record,
            invoice_number=invoice_data.invoice_number,
            invoice_date=invoice_data.invoice_date or datetime.now(),
            vendor=invoice_data.vendor,
            tax_number=invoice_data.tax_number,
            cashier=invoice_data.cashier,
            branch=invoice_data.branch,
            phone=invoice_data.phone,
            subtotal=invoice_data.subtotal,
            tax=invoice_data.tax,
            total_amount=invoice_data.total_amount,
            grand_total=invoice_data.grand_total,
            discounts=invoice_data.discounts,
            payment_method=invoice_data.payment_method,
            amount_paid=invoice_data.amount_paid,
            ticket_number=invoice_data.ticket_number,
            category=invoice_data.category
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return {"status": "success", "data": invoice.to_dict()}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")

# ------------------------------------------------------------
# ✅ GET /invoices → Summary
# ------------------------------------------------------------
@router.get("/")
def get_invoices(db: Session = Depends(get_db)):
    try:
        invoices = db.query(Invoice).all()
        return {
            "status": "success",
            "count": len(invoices),
            "data": [inv.to_dict() for inv in invoices]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving invoices: {str(e)}")

# ------------------------------------------------------------
# ✅ GET /invoices/all → Return only list (for frontend dashboard)
# ------------------------------------------------------------
@router.get("/all")
def get_all_invoices(db: Session = Depends(get_db)):
    try:
        invoices = db.query(Invoice).all()
        result = []
        
        # Get SUPABASE_URL from env for building image URLs
        supabase_url = os.getenv("SUPABASE_URL", "https://pcktfzshbxaljkbedrar.supabase.co")
        
        for inv in invoices:
            inv_dict = inv.to_dict()
            
            # 🔧 Temporary fix: Try to get image_url, fallback to building from invoice number
            if not inv_dict.get("image_url"):
                # Try to build image URL from invoice number or ID
                # Check if invoice_2.jpg or invoice_3.jpg exists
                potential_filename = f"invoice_{inv.id}.jpg"
                inv_dict["image_url"] = f"{supabase_url}/storage/v1/object/public/invoices/{potential_filename}"
                logger.info(f"🔧 Built fallback image URL for invoice {inv.id}: {inv_dict['image_url']}")
            
            result.append(inv_dict)
        
        return result
    except Exception as e:
        logger.error(f"❌ Error retrieving invoices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving invoices: {str(e)}")
