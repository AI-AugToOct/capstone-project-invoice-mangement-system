# backend/utils.py
import json
from sentence_transformers import SentenceTransformer
from backend.models.embedding_model import InvoiceEmbedding


# ✅ Load embedding model once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def generate_embedding(invoice_id: int, invoice_data, db):
    """
    Generate embedding from the FULL invoice data.
    Supports both dict (JSON) and string input.
    """

    # 🧠 If dict → convert to a readable text string
    if isinstance(invoice_data, dict):
        text_parts = []
        for key, value in invoice_data.items():
            if isinstance(value, list):  # e.g. list of items
                items_text = "; ".join(
                    [
                        f"{i.get('description', 'Unknown')} "
                        f"(qty: {i.get('quantity', 1)}, total: {i.get('total', 0)})"
                        for i in value if isinstance(i, dict)
                    ]
                )
                text_parts.append(f"{key}: {items_text}")
            else:
                text_parts.append(f"{key}: {value}")
        full_text = " | ".join(text_parts)

    # 🧾 If it's already a string, just use it directly
    elif isinstance(invoice_data, str):
        full_text = invoice_data

    else:
        # Just make sure we can still embed it
        full_text = json.dumps(invoice_data, ensure_ascii=False)

    # 🔄 Generate vector embedding
    embedding = model.encode(full_text).tolist()

    # 💾 Store in invoice_embeddings table
    emb = InvoiceEmbedding(invoice_id=invoice_id, embedding=embedding)
    db.add(emb)
    db.commit()
    db.refresh(emb)
    return emb.id
