from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

    class Config:
        orm_mode = True
