from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from openai import OpenAI
import os, json, re, logging
import numpy as np
from datetime import datetime, date
from decimal import Decimal
from backend.database import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "invoices")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
REFINER_MODEL = os.getenv("REFINER_MODEL", "gpt-4o-mini")

logger = logging.getLogger("backend.chat")

# Global context to remember last shown invoice(s) and user intent
last_invoice_context = []
last_user_intent = None
last_query_type = None  # 'max', 'min', 'avg', 'sum', 'list', etc.


def serialize_for_json(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj


def format_invoice_for_frontend(invoice_data: dict) -> dict:
    """Format invoice data for frontend display with guaranteed image_url"""
    formatted = {
        "id": invoice_data.get("id"),
        "vendor": invoice_data.get("vendor") or "متجر غير معروف",
        "invoice_number": invoice_data.get("invoice_number"),
        "invoice_type": invoice_data.get("invoice_type"),
        "date": invoice_data.get("invoice_date") or invoice_data.get("date"),
        "total": str(invoice_data.get("total_amount") or invoice_data.get("total") or "0"),
        "tax": str(invoice_data.get("tax") or "0"),
        "payment_method": invoice_data.get("payment_method"),
        # ✅ Always include image_url, with fallback chain
        "image_url": invoice_data.get("image_url") or invoice_data.get("image") or "",
        "category": invoice_data.get("category")
    }
    
    # Log image URL status for debugging
    if formatted["image_url"]:
        logger.debug(f"🖼️ Invoice {formatted['id']} | Vendor: {formatted['vendor']} | Has Image: ✅")
    else:
        logger.warning(f"⚠️ Invoice {formatted['id']} | Vendor: {formatted['vendor']} | No Image URL")
    
    return formatted


def is_greeting(text: str) -> bool:
    """Check if the user message is a greeting."""
    greetings = [
        "اهلا", "هلا", "السلام عليكم", "مرحبا", "هاي", 
        "hi", "hello", "صباح الخير", "مساء الخير", "السلام",
        "أهلا", "مرحباً", "هلو", "اهلين"
    ]
    text_lower = text.lower().strip()
    return any(greeting in text_lower for greeting in greetings)


def is_irrelevant(text: str) -> bool:
    """Check if the user message is irrelevant to invoices."""
    invoice_keywords = [
        # Arabic keywords
        "فاتورة", "فواتير", "متجر", "مطعم", "مبلغ", "ضريبة", 
        "كهرباء", "مياه", "صيدلية", "مقهى", "شراء", "كم", "عدد",
        "إجمالي", "اجمالي", "مصروفات", "مصروفاتي", "إنفاق", "انفاق",
        "دفعت", "صرفت", "كلفة", "سعر", "تكلفة", "حساب", "حسابات",
        "صورة", "صور", "ابي", "وريني", "اعرض", "ارسل", 
        "كافي", "مقاهي", "مطاعم", "صيدليات", "محل", "محلات",
        "شهر", "اسبوع", "يوم", "سنة", "تاريخ", "اليوم", "امس",
        # English keywords  
        "invoice", "bill", "receipt", "vendor", "store", "amount",
        "tax", "payment", "total", "expense", "spent", "cost", "price"
    ]
    text_lower = text.lower().strip()
    return not any(keyword in text_lower for keyword in invoice_keywords)


def universal_invoice_search(user_query: str, db: Session, limit: int = 5):
    """
    🌐 COMPREHENSIVE Universal Search across ALL invoice and item columns.
    Searches: invoice_number, vendor, subtotal, tax, total_amount, grand_total, 
              discounts, payment_method, amount_paid, category, tax_number, 
              cashier, branch, phone, ticket_number, invoice_type, ai_insight,
              AND item: description, quantity, unit_price, total.
    Returns multiple invoices that match ANY of the criteria.
    """
    conditions = []
    query_lower = user_query.lower()
    safe_query = user_query.replace("'", "''")  # SQL injection protection
    
    logger.info(f"🔍 Starting comprehensive universal search for: '{user_query}'")
    
    # ===== 1️⃣ NUMERIC DETECTION (all numeric columns with ±2 tolerance) =====
    number_match = re.search(r"(\d+(?:\.\d+)?)", user_query)
    if number_match:
        try:
            value = float(number_match.group())
            tolerance = 2  # ±2 for precision
            
            # Search all numeric invoice columns
            numeric_columns = [
                "subtotal", "tax", "total_amount", "grand_total", 
                "discounts", "amount_paid"
            ]
            
            for col in numeric_columns:
                conditions.append(
                    f"(CAST(COALESCE(invoices.{col}, '0') AS FLOAT) BETWEEN {value-tolerance} AND {value+tolerance})"
                )
            
            # Search item-level numeric columns (quantity, unit_price, total)
            conditions.append(
                f"""EXISTS (
                    SELECT 1 FROM items 
                    WHERE items.invoice_id = invoices.id 
                    AND (
                        CAST(items.quantity AS FLOAT) BETWEEN {value-tolerance} AND {value+tolerance}
                        OR CAST(items.unit_price AS FLOAT) BETWEEN {value-tolerance} AND {value+tolerance}
                        OR CAST(items.total AS FLOAT) BETWEEN {value-tolerance} AND {value+tolerance}
                    )
                )"""
            )
            
            logger.info(f"🔢 Numeric search: {value} ± {tolerance}")
        except:
            pass
    
    # ===== 2️⃣ TEXT SEARCH (all text columns from InvoiceCreate) =====
    invoice_text_columns = [
        "invoice_number", "vendor", "payment_method", "invoice_type",
        "tax_number", "cashier", "branch", "phone", "ticket_number", "ai_insight"
    ]
    
    for col in invoice_text_columns:
        conditions.append(
            f"(COALESCE(invoices.{col}, '') ILIKE '%{safe_query}%')"
        )
    
    # Category is special (JSONB)
    conditions.append(
        f"(invoices.category::jsonb->>'ar' ILIKE '%{safe_query}%' OR invoices.category::jsonb->>'en' ILIKE '%{safe_query}%')"
    )
    
    logger.info(f"📝 Text search across {len(invoice_text_columns)+1} invoice columns")
    
    # ===== 3️⃣ ITEM-LEVEL TEXT SEARCH (description) =====
    conditions.append(
        f"""EXISTS (
            SELECT 1 FROM items 
            WHERE items.invoice_id = invoices.id 
            AND items.description ILIKE '%{safe_query}%'
        )"""
    )
    
    logger.info(f"🛒 Item description search enabled")
    
    # ===== 4️⃣ DATE SEARCH (invoice_date patterns) =====
    # Full date format: YYYY-MM-DD
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", user_query)
    if date_match:
        date_str = date_match.group()
        conditions.append(f"CAST(invoices.invoice_date AS DATE) = '{date_str}'")
        logger.info(f"📅 Date filter: {date_str}")
    
    # Month names (Arabic)
    arabic_months = {
        "يناير": "01", "فبراير": "02", "مارس": "03", "ابريل": "04", 
        "أبريل": "04", "مايو": "05", "يونيو": "06", "يوليو": "07", 
        "أغسطس": "08", "سبتمبر": "09", "أكتوبر": "10", "اكتوبر": "10",
        "نوفمبر": "11", "ديسمبر": "12"
    }
    
    for month_ar, month_num in arabic_months.items():
        if month_ar in query_lower:
            conditions.append(f"TO_CHAR(invoices.invoice_date, 'MM') = '{month_num}'")
            logger.info(f"📅 Month filter: {month_ar} ({month_num})")
            break
    
    # ===== 5️⃣ BUILD & EXECUTE QUERY =====
    if not conditions:
        logger.warning("⚠️ No search conditions generated")
        return []
    
    where_clause = " OR ".join(conditions)
    
    query_sql = f"""
    SELECT DISTINCT 
        invoices.id, 
        invoices.invoice_number,
        invoices.vendor, 
        invoices.subtotal,
        invoices.tax,
        invoices.total_amount, 
        invoices.grand_total,
        invoices.discounts,
        invoices.payment_method,
        invoices.amount_paid,
        invoices.category,
        invoices.invoice_date, 
        invoices.invoice_type, 
        invoices.tax_number,
        invoices.cashier,
        invoices.branch,
        invoices.phone,
        invoices.ticket_number,
        invoices.image_url,
        invoices.ai_insight
    FROM invoices
    LEFT JOIN items ON invoices.id = items.invoice_id
    WHERE {where_clause}
    ORDER BY invoices.invoice_date DESC
    LIMIT {limit};
    """
    
    logger.info(f"🔍 Executing SQL: {query_sql[:250]}...")
    
    try:
        rows = db.execute(text(query_sql)).fetchall()
        results = [serialize_for_json(dict(row._mapping)) for row in rows]
        logger.info(f"✅ Universal search found {len(results)} invoice(s)")
        return results
    except Exception as e:
        logger.error(f"❌ Universal search failed: {e}")
        return []


def semantic_search(query: str, db: Session, top_k: int = 5):
    try:
        emb_response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )
        query_embedding = emb_response.data[0].embedding
        
        rows = db.execute(
            text("SELECT invoice_id, embedding FROM invoice_embeddings")
        ).fetchall()
        
        if not rows:
            return []
        
        print(f"📊 Found {len(rows)} embeddings in database")
        
        # Compute cosine similarity for each invoice
        def cosine_similarity(a, b):
            a = np.array(a)
            b = np.array(b)
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        
        ranked = []
        for row in rows:
            try:
                # Parse embedding from database (might be stored as JSON string)
                if isinstance(row.embedding, str):
                    invoice_embedding = json.loads(row.embedding)
                else:
                    invoice_embedding = row.embedding
                
                similarity = cosine_similarity(query_embedding, invoice_embedding)
                ranked.append((row.invoice_id, similarity))
            except Exception as e:
                print(f"⚠️ Error processing embedding for invoice {row.invoice_id}: {e}")
                continue
        
        # Sort by similarity (highest first)
        ranked.sort(key=lambda x: x[1], reverse=True)
        print(f"✅ Ranked {len(ranked)} invoices by similarity")
        
        # Get top_k invoice IDs
        top_ids = [str(r[0]) for r in ranked[:top_k]]
        
        if not top_ids:
            return []
        
        # Fetch full invoice details
        query_sql = f"""
        SELECT id, vendor, total_amount, invoice_date, category, 
               ai_insight, image_url, invoice_type, payment_method, tax
        FROM invoices 
        WHERE id IN ({','.join(top_ids)})
        """
        
        results = db.execute(text(query_sql)).fetchall()
        invoices = [serialize_for_json(dict(row._mapping)) for row in results]
        
        # Add similarity scores
        similarity_map = {r[0]: r[1] for r in ranked[:top_k]}
        for inv in invoices:
            inv['similarity'] = similarity_map.get(inv['id'], 0.0)
        
        print(f"✅ Semantic search returned {len(invoices)} invoices")
        if invoices:
            print(f"📊 Top result: {invoices[0].get('vendor')} (similarity: {invoices[0].get('similarity', 0):.3f})")
        
        return invoices
    
    except Exception as e:
        print(f"❌ Semantic search error: {e}")
        logger.error(f"Semantic search error: {e}")
        return []


@router.post("/ask")
async def chat_agent(request: dict, db: Session = Depends(get_db)):
    """
    Multi-stage intelligent assistant for مُفَوْتِر:
    - Stage 1: Intent detection & SQL generation
    - Stage 2: SQL execution
    - Stage 3: Semantic search fallback (if needed)
    - Stage 4: Natural Arabic response generation
    """
    try:
        user_query = request.get("question") or request.get("query", "")
        user_query = user_query.strip()
        
        if not user_query:
            return {"reply": "اكتب سؤالك أولاً 😊"}
        
        original_query = user_query
        logger.info(f"📥 Original query: {original_query}")
        
        # Check for greetings
        if is_greeting(user_query):
            logger.info("Detected greeting - returning welcome message")
            return {
                "reply": "هلا والله 👋! جاهز أساعدك تحلل فواتيرك؟ 💼",
                "invoices": None,
                "search_type": "none"
            }
        
        # Check for irrelevant questions
        if is_irrelevant(user_query):
            logger.info("Detected irrelevant query - returning guidance message")
            return {
                "reply": "أنا متخصص فقط في فواتيرك 💡 — جرب تسألني عن فاتورة أو متجر!",
                "invoices": None,
                "search_type": "none"
            }
        
        # Check if user is asking to show/send the last invoice (context-aware follow-up)
        global last_invoice_context, last_user_intent, last_query_type
        if re.search(r"(صورتها|صورته|وريني|ارسلها|ارسله|ابي اشوفها|ابي اشوفه|اعرضها|اعرضه|شفها|شفه)", user_query, re.IGNORECASE):
            if last_invoice_context and len(last_invoice_context) > 0:
                logger.info(f"Context-aware follow-up detected | Last intent: {last_user_intent} | Query type: {last_query_type}")
                
                # Generate contextual reply based on last query type
                if last_query_type == "max":
                    reply = "تمام! هذه صورة أغلى فاتورة عندك 👇"
                elif last_query_type == "min":
                    reply = "تمام! هذه صورة أرخص فاتورة عندك 👇"
                elif last_query_type == "avg":
                    reply = "هذه واحدة من الفواتير القريبة من المتوسط 👇"
                else:
                    reply = "تمام! هذه صورة آخر فاتورة بحثت عنها 👇"
                
                logger.info(f"Returning {len(last_invoice_context)} invoice(s) from context")
                return {
                    "reply": reply,
                    "invoices": last_invoice_context,
                    "search_type": "context"
                }
            else:
                logger.info("User requested last invoice but no context available")
                return {
                    "reply": "ما عندي فاتورة سابقة أقدر أرسلها 😅 — جرب تسأل عن فاتورة معينة أول!",
                    "invoices": None,
                    "search_type": "none"
                }
        
        # ============================================================
        # 🧠 STAGE 1: Query Refinement Phase
        # ============================================================
        try:
            logger.info("🔄 Starting query refinement phase...")
            
            refinement_prompt = f"""
أنت نموذج متخصص في تحسين وإعادة صياغة الأسئلة العربية لنظام تحليل الفواتير.
المستخدم قد يكتب رسائل غير مكتملة، عامية، أو غامضة.
أعد صياغة رسالة المستخدم إلى سؤال عربي واضح ودقيق يحافظ على نفس النية،
مناسب للاستعلام من قاعدة البيانات والتحليل الذكي.

📝 **قواعد الصياغة:**
1. احتفظ بالنية الأصلية تماماً
2. حوّل العامية إلى فصحى واضحة
3. أضف السياق المفقود إذا كان واضحاً من السؤال
4. إذا ذكر "ذيك" أو "تلك" → افترض أنه يقصد "أعلى" أو "آخر"
5. إذا كان السؤال واضحاً أصلاً، أعده كما هو أو بتحسين طفيف

✅ **أمثلة:**
- "ارسل لي ذيك الفاتورة" → "أرسل لي صورة أعلى فاتورة مدفوعة في النظام"
- "كم فاتورة عندي؟" → "كم عدد الفواتير المسجلة لدي؟"
- "فاتورة مطعم" → "اعرض تفاصيل فاتورة المطعم"
- "ابغى فواتير شهر اكتوبر" → "اعرض كل الفواتير بتاريخ أكتوبر 2025"
- "كم دفعت الشهر هذا؟" → "ما هو إجمالي المبالغ المدفوعة في فواتير هذا الشهر؟"
- "فاتورة الكهرباء" → "اعرض تفاصيل فاتورة شركة الكهرباء"
- "ابي صورة فاتورة المطعم الشهير" → "أرسل لي صورة فاتورة المطعم الشهير"

**أخرج النص العربي المُحسّن فقط، لا شيء آخر.**

---
الرسالة الأصلية من المستخدم:
{user_query}
"""

            refine_response = client.chat.completions.create(
                model=REFINER_MODEL,
                messages=[
                    {"role": "system", "content": "أنت نموذج لغوي عربي متخصص في إعادة صياغة الاستفسارات بدقة عالية لتحسين فهم الأنظمة الذكية."},
                    {"role": "user", "content": refinement_prompt}
                ],
                temperature=0.2,
                max_tokens=150
            )

            refined_query = refine_response.choices[0].message.content.strip()
            
            # Clean up any extra quotes or formatting
            refined_query = refined_query.strip('"').strip("'").strip()
            
            logger.info(f"✨ Refined query: {refined_query}")
            
            # Replace user_query with refined version
            user_query = refined_query

        except Exception as e:
            logger.error(f"❌ Query refinement failed: {e}")
            logger.info(f"⚠️ Falling back to original query: {original_query}")
            # Fallback to original text if refinement fails
            user_query = original_query
        
        # ============================================================
        # 🧮 SMART MATH DETECTION: Detect statistical/comparative intent
        # ============================================================
        math_intent_detected = False
        sql_override = None
        numeric_operation = None
        
        # Check for MAX (highest/most expensive)
        if any(word in user_query for word in ["أغلى", "أعلى", "أكبر", "اغلى", "اعلى", "اكبر", "الأعلى", "الأغلى"]):
            logger.info("🔢 Math intent detected: MAX (highest invoice)")
            sql_override = "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method, invoice_number FROM invoices ORDER BY CAST(total_amount AS FLOAT) DESC LIMIT 1"
            numeric_operation = "max"
            math_intent_detected = True
            last_query_type = "max"
        
        # Check for MIN (lowest/cheapest)
        elif any(word in user_query for word in ["أرخص", "أقل", "أصغر", "ارخص", "اقل", "اصغر", "الأقل", "الأرخص"]):
            logger.info("🔢 Math intent detected: MIN (lowest invoice)")
            sql_override = "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method, invoice_number FROM invoices ORDER BY CAST(total_amount AS FLOAT) ASC LIMIT 1"
            numeric_operation = "min"
            math_intent_detected = True
            last_query_type = "min"
        
        # Check for AVG (average)
        elif any(word in user_query for word in ["متوسط", "معدل", "المتوسط", "المعدل"]):
            logger.info("🔢 Math intent detected: AVG (average)")
            sql_override = "SELECT AVG(CAST(total_amount AS FLOAT)) as average FROM invoices"
            numeric_operation = "avg"
            math_intent_detected = True
            last_query_type = "avg"
        
        # Check for SUM (total)
        elif any(word in user_query for word in ["إجمالي", "مجموع", "كم صرفت", "كم دفعت", "اجمالي", "المجموع", "الإجمالي"]):
            logger.info("🔢 Math intent detected: SUM (total)")
            sql_override = "SELECT SUM(CAST(total_amount AS FLOAT)) as total FROM invoices"
            numeric_operation = "sum"
            math_intent_detected = True
            last_query_type = "sum"
        
        # If math intent detected, execute SQL directly and return
        if math_intent_detected and sql_override:
            logger.info(f"⚡ Executing math-optimized SQL: {sql_override[:80]}...")
            
            try:
                result = db.execute(text(sql_override)).fetchall()
                
                if numeric_operation in ["avg", "sum"]:
                    # For aggregate functions, return numeric result only
                    if result and len(result) > 0:
                        value = result[0][0]
                        if value is not None:
                            value = float(value)
                            
                            if numeric_operation == "avg":
                                reply = f"متوسط مبالغ فواتيرك هو {value:.2f} ر.س تقريبًا 💡"
                            else:  # sum
                                reply = f"إجمالي مصروفاتك هو {value:.2f} ر.س 💵"
                            
                            logger.info(f"✅ Math result: {value:.2f}")
                            return {
                                "reply": reply,
                                "invoices": None,
                                "search_type": "math",
                                "numeric_result": value,
                                "operation": numeric_operation
                            }
                    
                    # Fallback if no data
                    return {
                        "reply": "ما عندك فواتير حالياً لحساب المتوسط أو الإجمالي 😔",
                        "invoices": None,
                        "search_type": "none"
                    }
                
                elif numeric_operation in ["max", "min"]:
                    # For MAX/MIN, return the full invoice
                    if result and len(result) > 0:
                        invoice_data = dict(result[0]._mapping)
                        invoice_data = serialize_for_json(invoice_data)
                        
                        # Format for frontend
                        formatted_invoice = format_invoice_for_frontend(invoice_data)
                        
                        # Store in context for follow-up
                        last_invoice_context = [formatted_invoice]
                        last_user_intent = user_query
                        
                        # Generate friendly reply
                        vendor = invoice_data.get("vendor", "غير معروف")
                        amount = float(invoice_data.get("total_amount", 0))
                        
                        if numeric_operation == "max":
                            reply = f"أعلى فاتورة عندك {amount:.2f} ر.س من {vendor} 💰"
                        else:  # min
                            reply = f"أقل فاتورة عندك {amount:.2f} ر.س من {vendor} 📄"
                        
                        logger.info(f"✅ Math result: {amount:.2f} from {vendor}")
                        return {
                            "reply": reply,
                            "invoices": [formatted_invoice],
                            "search_type": "math",
                            "numeric_result": amount,
                            "operation": numeric_operation
                        }
                    
                    # Fallback if no data
                    return {
                        "reply": "ما عندك فواتير حالياً 😔",
                        "invoices": None,
                        "search_type": "none"
                    }
            
            except Exception as e:
                logger.error(f"❌ Math SQL execution failed: {e}")
                # Continue to normal flow
        
        # ============================================================
        # 🔎 UNIVERSAL SMART SEARCH: Multi-column intelligent matching
        # ============================================================
        # Try universal search for queries mentioning specific data
        should_try_universal = any([
            re.search(r"\d+", user_query),  # Contains numbers
            re.search(r"[A-Za-z]{3,}", user_query),  # Contains English text (vendor names)
            any(word in user_query for word in ["فاتورة", "محل", "مطعم", "مقهى", "شركة", "صيدلية"]),
            any(word in user_query for word in ["ضريبية", "شراء", "نقد", "بطاقة", "فيزا"])
        ])
        
        if should_try_universal and not math_intent_detected:
            logger.info("🔍 Attempting universal smart search...")
            universal_results = universal_invoice_search(user_query, db, limit=5)
            
            if universal_results and len(universal_results) > 0:
                logger.info(f"✅ Universal search returned {len(universal_results)} result(s)")
                
                # Store in context
                last_user_intent = user_query
                last_query_type = "universal"
                
                # ✅ Format ALL invoices for display (ensures image_url is included)
                invoices_for_display = []
                for item in universal_results:
                    formatted = format_invoice_for_frontend(item)
                    if formatted.get("id") and formatted.get("vendor"):
                        invoices_for_display.append(formatted)
                
                last_invoice_context = invoices_for_display[:3]
                
                # Log image URL status for all returned invoices
                logger.info(f"📸 Image URL status:")
                for inv in invoices_for_display:
                    img_status = "✅ HAS IMAGE" if inv.get("image_url") else "❌ NO IMAGE"
                    logger.info(f"   Invoice {inv['id']} ({inv['vendor']}): {img_status}")
                
                # Generate friendly reply based on result count
                if len(invoices_for_display) == 1:
                    vendor = invoices_for_display[0].get("vendor", "غير معروف")
                    amount = invoices_for_display[0].get("total", "0")
                    reply = f"لقيت فاتورة من {vendor} بمبلغ {amount} ر.س 📄"
                elif len(invoices_for_display) <= 3:
                    vendors = [inv.get("vendor", "غير معروف") for inv in invoices_for_display[:3]]
                    reply = f"لقيت {len(invoices_for_display)} فواتير: {', '.join(vendors[:2])}{'...' if len(vendors) > 2 else ''} 💼"
                else:
                    reply = f"لقيت {len(invoices_for_display)} فواتير تطابق طلبك 👇 هذي أبرزها:"
                
                logger.info(f"💾 Saved {len(invoices_for_display)} invoice(s) to context from universal search")
                
                # ✅ ALWAYS return invoices with image URLs
                return {
                    "reply": reply,
                    "invoices": invoices_for_display,  # Already formatted with image_url
                    "search_type": "universal",
                    "result_count": len(invoices_for_display)
                }
        
        plan_prompt = f"""
        استخرج نية المستخدم وحدد إن كان يحتاج SQL أو بحث دلالي.
        
        سؤال المستخدم:
        "{user_query}"
        
        📋 قواعد التحليل الدقيقة:
        
        🎯 **البحث الدقيق (استخدم الأعمدة المناسبة فقط):**
        - **نوع الفاتورة**: invoice_type ILIKE '%keyword%'
          مثال: "فاتورة ضريبية" → WHERE invoice_type ILIKE '%ضريبية%'
        
        - **المتجر**: vendor ILIKE '%keyword%'
          مثال: "فاتورة المياه" → WHERE vendor ILIKE '%مياه%'
        
        - **التصنيف**: category::jsonb->>'ar' ILIKE '%keyword%' OR category::jsonb->>'en' ILIKE '%keyword%'
          أمثلة:
          • "فواتير المطاعم" → WHERE (category::jsonb->>'ar' ILIKE '%مطعم%' OR category::jsonb->>'en' ILIKE '%Restaurant%')
          • "فواتير المقاهي" → WHERE (category::jsonb->>'ar' ILIKE '%مقهى%' OR category::jsonb->>'en' ILIKE '%Cafe%')
          • "الصيدليات" → WHERE (category::jsonb->>'ar' ILIKE '%صيدلية%' OR category::jsonb->>'en' ILIKE '%Pharmacy%')
        
        - **المبلغ**: CAST(total_amount AS FLOAT) BETWEEN value-5 AND value+5
          مثال: "فاتورة بـ 100 ريال" → WHERE CAST(total_amount AS FLOAT) BETWEEN 95 AND 105
        
        - **التاريخ**: invoice_date
          مثال: "فواتير هذا الشهر" → WHERE invoice_date >= '2025-10-01'
        
        - **أعلى/أقل/أكبر/أصغر**: استخدم ORDER BY + LIMIT
          أمثلة:
          • "أعلى فاتورة" أو "أكبر فاتورة" → ORDER BY total_amount DESC LIMIT 1
          • "أقل فاتورة" أو "أصغر فاتورة" → ORDER BY total_amount ASC LIMIT 1
          • "أغلى 3 فواتير" → ORDER BY total_amount DESC LIMIT 3
          • "أرخص فاتورة" → ORDER BY total_amount ASC LIMIT 1
        
        ⚠️ **ممنوع:**
        - لا تستخدم `ai_insight` في البحث الأساسي (فقط كـ fallback)
        - لا تخلط أنواع مختلفة إلا إذا طلب المستخدم صراحة
        - لا تستخدم OR بين أعمدة مختلفة بدون سبب
        
        🔄 **Fallback (إذا لم توجد نتائج دقيقة):**
        - استخدم: WHERE ai_insight ILIKE '%keyword%' LIMIT 3
        - وضح في explanation أنك استخدمت بحث تقريبي
        
        🖼️ **قاعدة الصور المهمة جداً:**
        المستخدم يطلب صور إذا استخدم **أي** من الكلمات التالية:
          • "صورة" أو "صور" → show_images: true
          • "ابي" مع ذكر فواتير/متجر → show_images: true
          • "وريني" أو "شف" أو "اشوف" → show_images: true
          • "ارسل" أو "أرسلي" أو "اعرض" → show_images: true
          • "فاتورة" أو "فواتير" + اسم متجر → show_images: true
        - إذا السؤال احصائي (كم، عدد، مجموع) **فقط** → show_images: false
        
        🗄️ الجداول المتاحة:
        - invoices(id, invoice_number, vendor, invoice_date, total_amount, tax, payment_method, category, ai_insight, invoice_type, image_url, created_at)
        - items(id, invoice_id, description, quantity, unit_price, total)
        - invoice_embeddings(invoice_id, embedding)
        
        ⚠️ قيود الأمان والأداء:
        - **فقط SELECT** (ممنوع DELETE/UPDATE/DROP)
        - **استخدم LIMIT دائماً:**
          • إذا طلب عرض/صورة → LIMIT 3
          • إذا طلب إحصائية (COUNT/SUM) → بدون LIMIT
          • إذا طلب "كل الفواتير" → LIMIT 10 maximum
        - إذا السؤال عن مبلغ → CAST(total_amount AS FLOAT) BETWEEN value-5 AND value+5
        - استخدم COALESCE للقيم الفارغة
        - اجلب الأعمدة المطلوبة فقط: id, vendor, total_amount, invoice_date, invoice_type, image_url
        
        📦 أخرج JSON بهذا الشكل بالضبط:
        {{
          "needs_sql": true/false,
          "sql": "SELECT ... FROM ... WHERE ...",
          "explanation": "شرح بسيط لنية البحث",
          "fallback_semantic": true/false,
          "search_type": "sql" أو "semantic" أو "hybrid",
          "show_images": true/false,
          "requested_vendor": "اسم المتجر إذا طلب صورة متجر محدد"
        }}
        
        **أمثلة دقيقة:**
        
        1. "كم فاتورة عندي؟"
        → {{"needs_sql": true, "sql": "SELECT COUNT(*) as count FROM invoices;", "show_images": false}}
        
        2. "ابي صورة فاتورة محل شاهي"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method, invoice_number FROM invoices WHERE vendor ILIKE '%شاي%' OR vendor ILIKE '%شاهي%' LIMIT 5;", "show_images": true, "requested_vendor": "شاهي"}}
        
        2b. "ابي صورة فاتورة كهرب"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method, invoice_number FROM invoices WHERE vendor ILIKE '%كهرب%' OR vendor ILIKE '%كهرباء%' LIMIT 5;", "show_images": true, "requested_vendor": "كهرباء"}}
        
        3. "ابي فاتورة الكافي"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method FROM invoices WHERE (category::jsonb->>'ar' ILIKE '%مقهى%' OR category::jsonb->>'en' ILIKE '%Cafe%') LIMIT 5;", "show_images": true}}
        
        4. "وريني فاتورة Keeta"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method FROM invoices WHERE vendor ILIKE '%Keeta%' LIMIT 3;", "show_images": true, "requested_vendor": "Keeta"}}
        
        5. "كم دفعت في المطاعم؟"
        → {{"needs_sql": true, "sql": "SELECT SUM(CAST(total_amount AS FLOAT)) as total FROM invoices WHERE category::jsonb->>'ar' ILIKE '%مطعم%' OR category::jsonb->>'en' ILIKE '%Restaurant%';", "show_images": false}}
        
        6. "فواتير المقاهي"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method FROM invoices WHERE (category::jsonb->>'ar' ILIKE '%مقهى%' OR category::jsonb->>'en' ILIKE '%Cafe%') LIMIT 5;", "show_images": false}}
        
        7. "ابي صور فواتير المقاهي"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method FROM invoices WHERE (category::jsonb->>'ar' ILIKE '%مقهى%' OR category::jsonb->>'en' ILIKE '%Cafe%') LIMIT 10;", "show_images": true}}
        
        8. "ما أعلى فاتورة دفعتها؟"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method, invoice_number FROM invoices ORDER BY CAST(total_amount AS FLOAT) DESC LIMIT 1;", "show_images": false}}
        
        9. "أقل 3 فواتير عندي"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url FROM invoices ORDER BY CAST(total_amount AS FLOAT) ASC LIMIT 3;", "show_images": false}}
        
        10. "كم عدد فواتيري"
        → {{"needs_sql": true, "sql": "SELECT COUNT(*) as count FROM invoices;", "show_images": false}}
        
        11. "ابي صورة فاتورة المطعم الشهير"
        → {{"needs_sql": true, "sql": "SELECT id, vendor, total_amount, invoice_date, invoice_type, image_url, tax, payment_method FROM invoices WHERE vendor ILIKE '%شهير%' LIMIT 1;", "show_images": true, "requested_vendor": "شهير"}}
        
        **مهم جداً:**
        - لاحظ الفرق: "المقاهي" → "مقهى" في البحث (صيغة المفرد)
        - المطاعم → مطعم، الصيدليات → صيدلية
        - استخدم ILIKE (case-insensitive) دائماً
        - استخدم صيغة المفرد في البحث داخل category
        - **مهم:** category مخزون كـ TEXT لازم تحوله: category::jsonb->>'ar'
        - لا تنسى ::jsonb قبل ->> وإلا SQL ما راح يشتغل!
        - لا تكتب أي شيء غير JSON!
        """

        plan_response = client.chat.completions.create(
            model="gpt-4o-mini",
                messages=[
                {"role": "system", "content": """أنت مدير متقدم للفواتير (Advanced Invoice Manager) مع صلاحيات كاملة على قاعدة البيانات.

🎯 **دورك:**
- لديك وصول كامل لكل الفواتير والبيانات المالية
- تستطيع تحليل وإحصاء وعرض أي معلومة عن الفواتير
- تفهم الأسئلة الإحصائية والتحليلية (كم، إجمالي، عدد، متوسط)
- تجمع بين Text-to-SQL و RAG للإجابة الدقيقة

قواعد حاسمة:
1. **الصور:** إذا المستخدم ذكر: "صورة", "صور", "ابي", "وريني", "اعرض", "ارسل", "شف", "اشوف" + أي ذكر للفاتورة/متجر
   → show_images: true
2. **requested_vendor:** حدد **بالضبط** اسم المتجر/الشركة من السؤال:
   - "فاتورة كهرب" → requested_vendor: "كهرباء"
   - "فاتورة مياه" → requested_vendor: "مياه"
   - "محل شاهي" → requested_vendor: "شاي"
   - "المطعم الشهير" → requested_vendor: "شهير"
   - "فاتورة Keeta" → requested_vendor: "Keeta"
3. **العدد والإحصائيات:** إذا قال "كم عدد", "كم فاتورة"
   → استخدم COUNT(*) فقط، لا تجلب تفاصيل الفواتير!
4. **الترتيب والمقارنة:** إذا قال "أعلى", "أقل", "أكبر", "أصغر", "أغلى", "أرخص"
   → استخدم ORDER BY CAST(total_amount AS FLOAT) DESC/ASC + LIMIT
5. إذا قال "المقاهي" → ابحث عن "مقهى" في category (صيغة مفرد)
6. **category** لازم cast: category::jsonb->>'ar' ILIKE '%مقهى%'
7. **دائماً** اجلب image_url في SELECT (إلا لو استخدمت COUNT)
8. أرجع JSON فقط."""},
                {"role": "user", "content": plan_prompt}
            ],
            temperature=0.1,
            max_tokens=700
        )

        plan_text = plan_response.choices[0].message.content
        
        try:
            plan_json = json.loads(re.search(r"\{.*\}", plan_text, re.S).group())
        except Exception as e:
            plan_json = {
                "needs_sql": False, 
                "sql": None, 
                "explanation": plan_text,
                "fallback_semantic": True,
                "search_type": "semantic",
                "show_images": False
            }

        sql_result = None
        semantic_result = None
        sql_text = plan_json.get("sql")
        used_semantic = False
        
        if plan_json.get("needs_sql") and sql_text:
            if not sql_text.lower().strip().startswith("select"):
                return {"reply": "⚠️ المساعد لا ينفذ إلا أوامر القراءة الآمنة فقط."}
            
            try:
                rows = db.execute(text(sql_text)).fetchall()
                sql_result = [serialize_for_json(dict(row._mapping)) for row in rows]
            except Exception as e:
                logger.error(f"SQL execution error: {e}")
                sql_result = []
        
        should_use_semantic = (
            (sql_result is not None and len(sql_result) == 0) or
            plan_json.get("fallback_semantic") or
            plan_json.get("search_type") in ["semantic", "hybrid"]
        )
        
        if should_use_semantic:
            semantic_result = semantic_search(user_query, db, top_k=5)
            used_semantic = True
        
        final_data = sql_result if sql_result else semantic_result
        
        reply_prompt = f"""
        🎯 سؤال المستخدم:
        "{user_query}"
        
        📊 البيانات المسترجعة:
        {json.dumps(serialize_for_json(final_data), ensure_ascii=False, indent=2) if final_data else "لا توجد نتائج"}
        
        🔍 طريقة البحث المستخدمة:
        {"SQL Query" if sql_result else "Semantic Search (بحث دلالي)" if used_semantic else "لا يوجد"}
        
        📝 **قواعد الرد (CRITICAL - اتبعها بدقة):**
        
        🔢 **إذا السؤال احصائي (كم عدد، كم إجمالي، كم مجموع):**
        ✅ **رد مختصر جداً - رقم فقط:**
           - "عندك [count] فواتير 📄"
           - "المجموع [total] ر.س 💰"
           - "3 فواتير من المطاعم 🍽️"
        ❌ **ممنوع نهائياً:**
           - **لا تسرد أي تفاصيل فواتير!**
           - **لا تذكر متاجر أو مبالغ أو تواريخ!**
           - **فقط الرقم المطلوب!**
        
        🖼️ **إذا السؤال عن صورة أو فاتورة محددة:**
        ✅ **رد بسيط:**
           - "تمام! هذه صورة فاتورة [المتجر] 👇"
           - "لقيت فاتورة [المتجر] بمبلغ [X] ر.س 📄"
        ❌ **ممنوع:**
           - **لا تقول "الصور أدناه" أو "📷" - الصور تظهر تلقائياً!**
           - **لا تذكر فواتير من متاجر مختلفة!**
        
        📊 **إذا السؤال تحليلي (أعلى، أقل، أكثر):**
        ✅ **رد واضح:**
           - "أعلى فاتورة عندك [مبلغ] ر.س من [متجر] 💰"
           - "أقل فاتورة [مبلغ] ر.س من [متجر] 📄"
        
        ❌ **لا توجد نتائج:**
           - "ما لقيت فواتير [النوع] حالياً 😔"
        
        🚫 **ممنوع تماماً:**
        - سرد فواتير عشوائية أو غير مطابقة
        - ذكر تفاصيل لما السؤال يكون عن عدد/إجمالي فقط
        - كتابة فقرات طويلة
        - ذكر "الصور" أو "أدناه" أو "في الصور"
        
        ✅ **أمثلة مثالية:**
        
        سؤال: "كم عدد فواتيري؟"
        رد: "عندك 7 فواتير 📄"
        
        سؤال: "ابي صورة فاتورة المطعم الشهير"
        رد: "تمام! هذه فاتورة المطعم الشهير بمبلغ 150 ر.س 🍽️"
        
        سؤال: "ما أعلى فاتورة عندي؟"
        رد: "أعلى فاتورة عندك 1993.27 ر.س من الشركة السعودية للكهرباء ⚡"
        
        اكتب الرد الآن بالعربية فقط، مختصر وواضح:
        """

        reply_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """أنت مدير متقدم للفواتير في نظام مُفَوْتِر.

🎯 صلاحياتك:
- لديك وصول كامل على قاعدة بيانات الفواتير
- تستطيع تحليل المصروفات والإحصائيات
- تفهم الأسئلة المالية والتحليلية بعمق
- تجيب بدقة عن الإجماليات والأعداد والمتوسطات

💬 أسلوبك:
- عربي فصيح مع لهجة سعودية خفيفة
- مختصر وواضح ومباشر
- لا تكتب أكواد أو JSON
- استخدم الأرقام والإحصائيات بدقة"""},
                {"role": "user", "content": reply_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        final_reply = reply_response.choices[0].message.content.strip()
        
        invoices_for_display = []
        show_images = plan_json.get("show_images", False)
        requested_vendor = (plan_json.get("requested_vendor") or "").strip()
        
        if show_images and final_data:
            logger.info(f"Image display requested | Vendor filter: '{requested_vendor}' | Results: {len(final_data)}")
            
            for item in final_data:
                formatted = format_invoice_for_frontend(item)
                
                # If specific vendor requested, apply strict filtering
                if requested_vendor:
                    item_vendor = (item.get("vendor") or "").lower()
                    vendor_filter = requested_vendor.lower()
                    
                    # Check if vendor matches the filter
                    if vendor_filter not in item_vendor:
                        logger.debug(f"Filtered out: {item_vendor} (doesn't match {vendor_filter})")
                        continue
                
                if formatted.get("id") and formatted.get("vendor"):
                    invoices_for_display.append(formatted)
            
            logger.info(f"✅ Final invoices to display: {len(invoices_for_display)}")
            
            # ✅ Log image URL status for all displayed invoices
            if invoices_for_display:
                logger.info(f"📸 Image URL status for displayed invoices:")
                for inv in invoices_for_display:
                    img_status = "✅" if inv.get("image_url") else "❌"
                    logger.info(f"   {img_status} Invoice {inv['id']} ({inv['vendor']}): {inv.get('image_url', 'NO IMAGE')}")
        
        # Save the last shown invoice(s) and user intent for follow-up requests
        if invoices_for_display and len(invoices_for_display) > 0:
            # Store up to 3 most recent invoices
            last_invoice_context = invoices_for_display[:3]
            last_user_intent = user_query
            if not last_query_type:  # Only set if not already set by math detection
                last_query_type = "list"
            logger.info(f"💾 Saved {len(last_invoice_context)} invoice(s) to context | Intent: '{user_query[:50]}...'")
        elif final_data and len(final_data) > 0 and not show_images:
            # Even if not showing images, save the data for potential follow-up
            last_invoice_context = [format_invoice_for_frontend(final_data[0])]
            last_user_intent = user_query
            if not last_query_type:
                last_query_type = "list"
            logger.info(f"💾 Saved 1 invoice to context (from query result)")

        return {
            "reply": final_reply,
            "invoices": invoices_for_display if invoices_for_display else None,
            "plan": plan_json,
            "executed_sql": sql_text if sql_result else None,
            "used_semantic": used_semantic,
            "result_count": len(final_data) if final_data else 0,
            "search_type": plan_json.get("search_type", "unknown"),
            "show_images": show_images
        }

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {
            "reply": "عذراً، حدث خطأ أثناء معالجة طلبك 😔 الرجاء المحاولة مرة أخرى.",
            "error": str(e)
        }
