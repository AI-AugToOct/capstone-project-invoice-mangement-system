# backend/models/embedding_model.py
from sqlalchemy import Column, Integer, ForeignKey
from backend.database import Base
from pgvector.sqlalchemy import Vector  

class InvoiceEmbedding(Base):
    __tablename__ = "invoice_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"))
    embedding = Column(Vector(384))  # 
