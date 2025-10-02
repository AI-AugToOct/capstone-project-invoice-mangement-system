from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    record = Column(Integer, index=True)
    invoice_number = Column(String, index=True)
    invoice_date = Column(DateTime)
    vendor = Column(String, index=True)
    tax_number = Column(String)
    cashier = Column(String)
    branch = Column(String)
    phone = Column(String)
    subtotal = Column(String)
    tax = Column(String)
    total_amount = Column(String)
    grand_total = Column(String)
    discounts = Column(String)
    payment_method = Column(String)
    amount_paid = Column(String)
    ticket_number = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "record": self.record,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date.isoformat() if self.invoice_date else None,
            "vendor": self.vendor,
            "tax_number": self.tax_number,
            "cashier": self.cashier,
            "branch": self.branch,
            "phone": self.phone,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total_amount": self.total_amount,
            "grand_total": self.grand_total,
            "discounts": self.discounts,
            "payment_method": self.payment_method,
            "amount_paid": self.amount_paid,
            "ticket_number": self.ticket_number,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
