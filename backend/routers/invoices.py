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


# Schema for edited invoice data
class EditedInvoiceData(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    tax_number: str = ""
    cashier: str = ""
    branch: str = ""
    phone: str = ""
    subtotal: str = "0"
    tax: str = "0"
    total_amount: str = "0"
    discounts: str = "0"
    payment_method: str = ""
    invoice_type: str = "فاتورة شراء"
    category: dict = {"ar": "أخرى", "en": "Other"}
    ai_insight: str = ""
    image_url: str = ""

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
                return None
            formats = ["%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"]
            for fmt in formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except:
                    continue
            try:
                return datetime.fromisoformat(value.strip())
            except:
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
        
        # Create invoice
        invoice = Invoice(
            invoice_number=data.invoice_number or "Not Mentioned",
            invoice_date=parsed_date,
            vendor=data.vendor or "Not Mentioned",
            tax_number=data.tax_number or "Not Mentioned",
            cashier=data.cashier or "Not Mentioned",
            branch=data.branch or "Not Mentioned",
            phone=data.phone or "Not Mentioned",
            subtotal=safe_float(data.subtotal),
            tax=safe_float(data.tax),
            total_amount=safe_float(data.total_amount),
            discounts=safe_float(data.discounts),
            payment_method=data.payment_method or "Not Mentioned",
            invoice_type=data.invoice_type,
            category=json.dumps(data.category, ensure_ascii=False),
            ai_insight=data.ai_insight or "Not Mentioned",
            image_url=data.image_url,
        )
        
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        
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
