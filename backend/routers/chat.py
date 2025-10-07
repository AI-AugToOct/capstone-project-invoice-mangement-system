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
from backend.models.invoice_model import Invoice
from sqlalchemy import or_

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
            logger.info("🧮 SQL Mode - Aggregation detected")

            completion = llm_client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "أنت مساعد ذكي متخصص في تحويل الأسئلة العربية المتعلقة بالفواتير إلى استعلامات SQL صحيحة.\n\n"
                            "قاعدة البيانات تحتوي على الجداول التالية:\n\n"
                            "1. جدول invoices:\n"
                            "   - id, record, invoice_number, invoice_date, vendor, tax_number, cashier, branch, phone\n"
                            "   - subtotal, tax, total_amount, grand_total, discounts, payment_method, amount_paid\n"
                            "   - ticket_number, category, created_at, ai_insight\n\n"
                            "2. جدول items:\n"
                            "   - id, invoice_id, description, quantity, unit_price, total\n\n"
                            "3. جدول invoice_embeddings:\n"
                            "   - id, invoice_id, embedding\n\n"
                            "قواعد مهمة:\n"
                            "- أعد فقط استعلام SQL واحد نظيف بدون شرح\n"
                            "- استخدم CAST للتحويلات الرقمية\n"
                            "- total_amount و subtotal و tax نوعها TEXT - استخدم CAST(column AS FLOAT)\n"
                            "- category نوعها JSON - استخدم json_extract إذا احتجت\n"
                            "- لا تضع ملاحظات أو تعليقات في الاستعلام"
                        ),
                    },
                    {"role": "user", "content": request.question},
                ],
            )

            sql_query = completion.choices[0].message.content.strip()
            sql_query = fix_sql_casts(sql_query)
            logger.info(f"📝 Generated SQL:\n{sql_query}")

            try:
                results = db.execute(text(sql_query)).fetchall()
                
                # Format Arabic response
                if results and len(results) == 1 and len(results[0]) == 1:
                    val = results[0][0]
                    # Format number with Arabic context
                    if isinstance(val, (int, float)):
                        return {"answer": f"النتيجة: **{val:,.2f}** {'ريال' if 'مبلغ' in request.question or 'إنفاق' in request.question or 'إجمالي' in request.question else ''}"}
                    return {"answer": f"النتيجة: **{val}**"}
                elif not results:
                    return {"answer": "لم أجد أي بيانات تطابق سؤالك."}
                else:
                    # Multiple results - format nicely
                    formatted_results = []
                    for row in results[:10]:  # Limit to 10 results
                        formatted_results.append(" | ".join([str(r) for r in row]))
                    
                    result_text = "\n".join(formatted_results)
                    return {"answer": f"النتائج ({len(results)} سجل):\n\n{result_text}"}
                    
            except Exception as sql_err:
                logger.error(f"❌ SQL execution failed: {sql_err}")
                return {
                    "answer": f"عذراً، حدث خطأ في تنفيذ الاستعلام.\n\nالاستعلام: {sql_query}\n\nالخطأ: {str(sql_err)}"
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

        # 🔎 Mode 2 — Direct Retrieval (Vendor/Type Search)
        # Check if question is asking for specific vendor or invoice type
        retrieval_keywords = ['فاتورة', 'فواتير', 'أرني', 'أرسل', 'اعرض', 'وين']
        is_retrieval = any(keyword in request.question for keyword in retrieval_keywords)
        
        if is_retrieval:
            logger.info("🖼️ Retrieval Mode - Looking for specific invoices")
            
            # استخراج كلمات مفتاحية من السؤال
            keywords = request.question.lower().split()
            direct_results = []
            
            for keyword in keywords:
                if len(keyword) > 2:  # تجاهل الكلمات القصيرة جداً
                    found = db.query(Invoice).filter(
                        or_(
                            Invoice.vendor.ilike(f"%{keyword}%"),
                            Invoice.invoice_type.ilike(f"%{keyword}%")
                        )
                    ).limit(5).all()
                    
                    if found:
                        direct_results.extend(found)
                        break  # وجدنا نتائج، نوقف البحث
            
            # إذا وجدنا نتائج مباشرة، نستخدمها
            if direct_results:
                logger.info(f"🎯 Found {len(direct_results)} invoices")
                
                # تحويل النتائج لـ JSON مع كل المعلومات
                invoices_data = []
                context_lines = []
                
                # Get SUPABASE_URL for building image URLs
                supabase_url = os.getenv("SUPABASE_URL", "https://pcktfzshbxaljkbedrar.supabase.co")
                
                for inv in direct_results[:5]:  # نأخذ أول 5 فواتير
                    date_str = str(inv.invoice_date.strftime("%Y-%m-%d")) if inv.invoice_date else "غير محدد"
                    
                    # Use stored image_url or fallback
                    image_url = inv.image_url or f"{supabase_url}/storage/v1/object/public/invoices/invoice_{inv.id}.jpg"
                    
                    invoices_data.append({
                        "id": inv.id,
                        "vendor": inv.vendor or "غير معروف",
                        "invoice_number": inv.invoice_number or "غير محدد",
                        "invoice_type": inv.invoice_type or "غير محدد",
                        "date": date_str,
                        "total": str(inv.total_amount) if inv.total_amount else "0.00",
                        "tax": str(inv.tax) if inv.tax else "0.00",
                        "payment_method": inv.payment_method or "غير محدد",
                        "image_url": image_url,
                        "category": inv.category or "{}",
                    })
                    
                    context_lines.append(
                        f"فاتورة رقم {inv.id} من {inv.vendor or 'غير معروف'} بتاريخ {date_str} بمبلغ {inv.total_amount or 0.0} ريال"
                    )
                
                context_text = "\n".join(context_lines)
                
                # 💬 Generate final natural language answer in Arabic
                completion = llm_client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "أنت مساعد ذكي يجيب على الأسئلة المتعلقة بالفواتير بالعربية.\n"
                                "استخدم البيانات المقدمة للإجابة بشكل واضح وطبيعي.\n"
                                "اذكر عدد الفواتير والمبالغ والتفاصيل المهمة."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"سؤال المستخدم: {request.question}\n\nالفواتير المتاحة:\n{context_text}"
                        }
                    ],
                )
                
                ai_answer = completion.choices[0].message.content.strip()
                return {
                    "answer": ai_answer,
                    "invoices": invoices_data  # إرجاع الفواتير مع كل المعلومات
                }
        
        # 🔍 Mode 3 — RAG (Semantic Search for general questions)
        logger.info("📄 RAG Mode - Semantic search with embeddings")
        
        query = text("""
            SELECT i.id, i.vendor, i.subtotal, i.total_amount, i.invoice_date, i.category,
                   e.embedding <-> CAST(:vec AS vector) AS distance
            FROM invoices i
            JOIN invoice_embeddings e ON i.id = e.invoice_id
            ORDER BY distance ASC
            LIMIT :top_k;
        """)
        results = db.execute(query, {"vec": vector, "top_k": request.top_k}).fetchall()

        if not results:
            return {"answer": "لم أتمكن من العثور على أي فواتير متعلقة بسؤالك. جرب إعادة صياغة السؤال أو اسأل عن متجر محدد."}

        # تحويل النتائج بالعربية
        context_lines = []
        for r in results:
            date_str = r.invoice_date.strftime("%Y-%m-%d") if r.invoice_date else "غير محدد"
            vendor = r.vendor or "غير معروف"
            total = float(r.total_amount) if r.total_amount else 0.0
            
            context_lines.append(
                f"فاتورة رقم {r.id} من {vendor} بتاريخ {date_str} بمبلغ {total:.2f} ريال"
            )

        context_text = "\n".join(context_lines)

        # 💬 Generate final natural language answer in Arabic
        completion = llm_client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت مساعد ذكي متخصص في تحليل الفواتير وإدارتها.\n"
                        "استخدم البيانات المقدمة للإجابة بشكل واضح ومفيد بالعربية.\n"
                        "كن دقيقاً في الأرقام واذكر التفاصيل المهمة.\n"
                        "إذا لم تكن المعلومات كافية، اذكر ذلك بوضوح."
                    )
                },
                {
                    "role": "user",
                    "content": f"سؤال المستخدم: {request.question}\n\nالفواتير الأكثر صلة:\n{context_text}"
                }
            ],
        )

        ai_answer = completion.choices[0].message.content.strip()
        return {"answer": ai_answer}

    except Exception as e:
        logger.error(f"❌ Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
