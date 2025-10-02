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
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
