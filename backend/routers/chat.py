# backend/routers/chat.py
import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from openai import OpenAI
from backend.database import get_db

# ================================================================
# ⚙️ Setup
# ================================================================
load_dotenv()
router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger("backend.chat")

HF_TOKEN = os.getenv("HF_TOKEN")

# Clients
hf_client = InferenceClient(api_key=HF_TOKEN)
llm_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# Local embedding model (fallback)
local_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# ================================================================
# 🧠 Helper Classes & Functions
# ================================================================
class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


def is_aggregation_question(question: str) -> bool:
    """Detects if the question involves aggregation (sum, count, etc.)"""
    keywords = ["sum", "total", "average", "count", "how many", "كم", "مجموع", "إجمالي"]
    q_lower = question.lower()
    return any(k in q_lower for k in keywords)


def fix_sql_casts(sql_query: str) -> str:
    """Casts numeric columns to FLOAT for math operations"""
    numeric_fields = [
        "subtotal", "tax", "total_amount", "grand_total",
        "discounts", "amount_paid"
    ]
    for col in numeric_fields:
        sql_query = sql_query.replace(col, f"CAST({col} AS FLOAT)")
    return sql_query


# ================================================================
# 💬 Endpoint: /chat/ask
# ================================================================
@router.post("/ask")
async def ask_chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 🧮 Mode 1 — Aggregation / SQL
        if is_aggregation_question(request.question):
            logger.info("🧮 Detected aggregation question, switching to SQL mode")

            completion = llm_client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant that translates natural language invoice "
                            "questions into SQL queries. "
                            "The database has three tables:\n"
                            "- invoices(id, vendor, subtotal, tax, total_amount, category, invoice_date, ...)\n"
                            "- items(id, invoice_id, description, quantity, unit_price, total)\n"
                            "- invoice_embeddings(id, invoice_id, embedding)\n\n"
                            "ONLY return the SQL query. Do not explain anything else."
                        ),
                    },
                    {"role": "user", "content": request.question},
                ],
            )

            sql_query = completion.choices[0].message.content.strip()
            sql_query = fix_sql_casts(sql_query)
            logger.info(f"Generated SQL:\n{sql_query}")

            try:
                results = db.execute(text(sql_query)).fetchall()
                if results and len(results) == 1 and len(results[0]) == 1:
                    val = results[0][0]
                    return {"answer": f"The result is **{val}**."}
                elif not results:
                    return {"answer": "No data found for your query."}
                else:
                    return {"answer": f"Here are the results:\n{results}"}
            except Exception as sql_err:
                logger.error(f"❌ SQL execution failed: {sql_err}")
                return {
                    "answer": f"Sorry, I could not run the generated SQL.\nQuery:\n{sql_query}",
                    "error": str(sql_err),
                }

        # 🔍 Mode 2 — Semantic / RAG
        try:
            response = hf_client.post(
                path="https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
                json={"inputs": [request.question]},
            )
            emb = response.json()
            vector = [float(x) for x in emb[0]]
            logger.info("✅ Got embedding from Hugging Face API")

        except Exception as api_err:
            logger.warning(f"⚠️ HF API failed, using local embedding: {api_err}")
            vector = local_model.encode([request.question])[0].tolist()

        # 🔎 Search similar invoices
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

        # 💬 Generate final natural language answer
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
