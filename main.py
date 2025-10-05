import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import models
from database import SessionLocal, engine

# Pydantic models for API requests/responses
class InvoiceCreate(BaseModel):
    invoice_number: str
    vendor: str
    subtotal: str = "0.00"
    tax: str = "0.00"
    total_amount: str = "0.00"
    grand_total: str = "0.00"
    discounts: str = "0.00"
    payment_method: str = "Cash"
    amount_paid: str = "0.00"
    category: str = "General"
    invoice_date: Optional[datetime] = None
    tax_number: Optional[str] = None
    cashier: Optional[str] = None
    branch: Optional[str] = None
    phone: Optional[str] = None
    ticket_number: Optional[str] = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables (if not exist)
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")
except Exception as e:
    logger.error(f"Error creating tables: {e}")

app = FastAPI()

# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()


@app.get("/")
def root():
    logger.info("Root endpoint called.")
    return {"msg": "Hello from FastAPI + Supabase"}


@app.post("/invoices/")
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        # Get the next record number
        last_record = db.query(models.Invoice).order_by(models.Invoice.record.desc()).first()
        next_record = (last_record.record + 1) if last_record else 1
        
        # Create new invoice
        invoice = models.Invoice(
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
        logger.info(f"Invoice created: {invoice.id} - {invoice.vendor}")
        return {"status": "success", "data": invoice.to_dict()}
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")


@app.get("/invoices/")
def get_invoices(db: Session = Depends(get_db)):
    try:
        invoices = db.query(models.Invoice).all()
        logger.info(f"Retrieved {len(invoices)} invoices.")
        return {
            "status": "success", 
            "count": len(invoices), 
            "data": [invoice.to_dict() for invoice in invoices]
        }
    except Exception as e:
        logger.error(f"Error retrieving invoices: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving invoices.")