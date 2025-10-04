# backend/utils.py
import os
from sentence_transformers import SentenceTransformer
from backend.models.embedding_model import InvoiceEmbedding


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding(invoice_id: int, text: str, db):
   
    embedding = model.encode(text).tolist()

    
    emb = InvoiceEmbedding(invoice_id=invoice_id, embedding=embedding)
    db.add(emb)
    db.commit()
    db.refresh(emb)
    return emb.id
