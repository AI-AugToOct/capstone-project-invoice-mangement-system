from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    qty = Column(Integer)
    price = Column(Float)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
