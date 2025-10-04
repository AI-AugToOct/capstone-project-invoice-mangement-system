import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from sqlalchemy import text
from openai import OpenAI

from backend.database import get_db

# --------------------------
# Setup
# --------------------------
load_dotenv()
router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger("backend.chat")

HF_TOKEN = os.getenv("HF_TOKEN")

# HuggingFace Inference Client
hf_client = InferenceClient(api_key=HF_TOKEN)


llm_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# --------------------------
# Request Schema
# --------------------------
class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


# --------------------------
# Endpoint
# --------------------------
@router.post("/ask")
async def ask_chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 1) Generate embedding for user question  (positional only)
        emb = hf_client.feature_extraction(
            [request.question],  # 
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector = [float(x) for x in emb[0]]  

       
        query = text("""
            SELECT i.id, i.vendor, i.subtotal, i.total_amount, i.invoice_date,
                   e.embedding <-> CAST(:vec AS vector) AS distance
            FROM invoices i
            JOIN invoice_embeddings e ON i.id = e.invoice_id
            ORDER BY distance ASC
            LIMIT :top_k;
        """)

        results = db.execute(query, {"vec": vector, "top_k": request.top_k}).fetchall()

        if not results:
            return {"answer": "I couldn’t find any invoices related to your question."}

        
        context_lines = []
        for r in results:
            date_str = str(r.invoice_date) if r.invoice_date else "Not Mentioned"
            context_lines.append(
                f"Invoice {r.id} from {r.vendor or 'Unknown'} on {date_str} → Total {r.total_amount or 0.0} SAR"
            )

        context_text = "\n".join(context_lines)

     
        completion = llm_client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that answers questions about invoices. "
                               "Use the provided invoice data to answer clearly and naturally."
                },
                {
                    "role": "user",
                    "content": f"User question: {request.question}\n\nHere are the most relevant invoices:\n{context_text}"
                }
            ],
        )

        ai_answer = completion.choices[0].message.content.strip()

        return {"answer": ai_answer}

    except Exception as e:
        logger.error(f"❌ Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
