import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models.invoice_model import Invoice
from backend.schemas.invoice_schema import InvoiceCreate

router = APIRouter(prefix="/invoices", tags=["Invoices"])
logger = logging.getLogger(__name__)

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
        return [inv.to_dict() for inv in invoices]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving invoices: {str(e)}")
