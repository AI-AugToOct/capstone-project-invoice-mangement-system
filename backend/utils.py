from openai import OpenAI
import os
import json
from backend.models.embedding_model import InvoiceEmbedding

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(invoice_id: int, invoice_data, db):
    """
    Generate embedding for the invoice using OpenAI text-embedding-3-small.
    Handles both dict and string input.
    """

    if isinstance(invoice_data, dict):
        text_parts = []
        for key, value in invoice_data.items():
            if isinstance(value, list):
                items_text = "; ".join(
                    [
                        f"{i.get('description', 'Unknown')} (qty: {i.get('quantity', 1)}, total: {i.get('total', 0)})"
                        for i in value if isinstance(i, dict)
                    ]
                )
                text_parts.append(f"{key}: {items_text}")
            else:
                text_parts.append(f"{key}: {value}")
        full_text = " | ".join(text_parts)
    elif isinstance(invoice_data, str):
        full_text = invoice_data
    else:
        full_text = json.dumps(invoice_data, ensure_ascii=False)

    # Generate embedding from OpenAI
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=full_text
    )

    embedding = response.data[0].embedding

    # Save embedding to database
    emb = InvoiceEmbedding(invoice_id=invoice_id, embedding=embedding)
    db.add(emb)
    db.commit()
    db.refresh(emb)
    return emb.id
