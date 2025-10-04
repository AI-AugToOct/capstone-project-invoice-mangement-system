from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total = Column(Float)
