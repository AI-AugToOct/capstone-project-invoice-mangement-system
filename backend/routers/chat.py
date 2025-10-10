"""
🧠 مُفَوْتِر | Smart Invoice Analyzer - AI Chat System
═══════════════════════════════════════════════════════════════════════════════

نظام ذكاء اصطناعي متكامل للتفاعل مع المستخدمين وتحليل الفواتير.

المراحل:
1. Refiner Stage    - تحسين السؤال من عامية إلى فصحى
2. Router Stage     - تحديد نوع المعالجة (deep_sql, rag, hybrid, none)
3. Executor Stage   - تنفيذ الاستعلامات والبحث
4. Validator Stage  - التحقق من البيانات الحقيقية
5. Replier Stage    - صياغة الرد النهائي

الأمان:
- فقط استعلامات SELECT مسموحة
- تحقق من كل استعلام SQL قبل التنفيذ
- حماية من SQL Injection

السياق:
- حفظ آخر 3 استفسارات للمستخدم
- ربط مع بيانات الفواتير المحللة من VLM
- دعم الأسئلة التالية (follow-up questions)
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from openai import OpenAI
import os
import json
import re
import logging
import numpy as np
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any, Literal
from backend.database import get_db

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 Configuration & Setup
# ═══════════════════════════════════════════════════════════════════════════════

router = APIRouter(prefix="/chat", tags=["Chat"])
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Models Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Database Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "invoices")

# Logger Setup
logger = logging.getLogger("backend.chat")
logger.setLevel(logging.INFO)

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 Global Context Management
# ═══════════════════════════════════════════════════════════════════════════════

class ChatContext:
    """Global context to remember user's conversation history"""
    
    def __init__(self):
        self.last_3_intents: List[str] = []
        self.last_3_invoices: List[Dict] = []
        self.last_3_modes: List[str] = []
    
    def add_context(self, intent: str, invoices: List[Dict], mode: str):
        """Add new context and maintain only last 3"""
        self.last_3_intents.insert(0, intent)
        self.last_3_invoices.insert(0, invoices)
        self.last_3_modes.insert(0, mode)
        
        # Keep only last 3
        self.last_3_intents = self.last_3_intents[:3]
        self.last_3_invoices = self.last_3_invoices[:3]
        self.last_3_modes = self.last_3_modes[:3]
    
    def get_last_invoices(self) -> List[Dict]:
        """Get last shown invoices"""
        return self.last_3_invoices[0] if self.last_3_invoices else []
    
    def get_last_intent(self) -> Optional[str]:
        """Get last user intent"""
        return self.last_3_intents[0] if self.last_3_intents else None
    
    def clear(self):
        """Clear all context"""
        self.last_3_intents.clear()
        self.last_3_invoices.clear()
        self.last_3_modes.clear()

# Global context instance
context = ChatContext()

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ Utility Functions
# ═══════════════════════════════════════════════════════════════════════════════

def serialize_for_json(obj: Any) -> Any:
    """Convert datetime, Decimal, and other types to JSON-serializable format"""
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
        "image_url": invoice_data.get("image_url") or "",
        "category": invoice_data.get("category"),
        "ai_insight": invoice_data.get("ai_insight"),
    }
    
    if formatted["image_url"]:
        logger.debug(f"🖼️ Invoice {formatted['id']} | Vendor: {formatted['vendor']} | Has Image: ✅")
    else:
        logger.warning(f"⚠️ Invoice {formatted['id']} | Vendor: {formatted['vendor']} | No Image URL")
    
    return formatted


def is_safe_sql(sql_query: str) -> bool:
    """
    Check if SQL query is safe (only SELECT allowed)
    Returns True if safe, False otherwise
    """
    sql_lower = sql_query.lower().strip()
    
    # Must start with SELECT
    if not sql_lower.startswith("select"):
        logger.warning(f"🚫 Unsafe SQL: Does not start with SELECT")
        return False
    
    # Forbidden keywords
    forbidden = ["delete", "drop", "truncate", "update", "insert", "alter", "create", "exec", "execute"]
    for word in forbidden:
        if word in sql_lower:
            logger.warning(f"🚫 Unsafe SQL: Contains forbidden keyword '{word}'")
            return False
    
    logger.info(f"✅ SQL is safe: {sql_query[:100]}...")
    return True


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 STAGE 1: Refiner
# ═══════════════════════════════════════════════════════════════════════════════

def refine_user_query(user_query: str) -> str:
    """
    🔍 Refiner Stage:
    تحسين وصياغة سؤال المستخدم من عامية إلى فصحى واضحة
    
    Args:
        user_query: السؤال الأصلي من المستخدم
    
    Returns:
        السؤال المحسّن بالفصحى
    """
    logger.info("🔍 Starting Refiner Stage...")
    logger.info(f"   Original Query: {user_query}")
    
    try:
        refiner_prompt = f"""
أنت خبير في تحسين الأسئلة العربية.

**مهمتك:**
حوّل السؤال التالي من اللهجة العامية (السعودية/الخليجية) إلى لغة عربية فصحى واضحة ومفهومة.

**قواعد صارمة:**
1. لا تغيّر نية المستخدم أو معنى السؤال
2. لا تضف معلومات جديدة
3. فقط نظّف اللهجة وحسّن الصياغة
4. **احتفظ بالكلمات المفتاحية كما هي EXACTLY** (أسماء المتاجر بالإنجليزية أو العربية، الأرقام، التواريخ)
   - مثال: "Keeta" → أبقِها "Keeta" (لا تغيرها)
   - مثال: "كتا" → أبقِها "كتا"
5. **إذا كان اسم المتجر طويل، استخرج الاسم الأساسي فقط**
   - مثال: "شركة جيرة لتقديم المشروبات - فرع الأكاديمية" → "فاتورة جيرة"
   - مثال: "مؤسسة صب واي للأغذية" → "فاتورة صب واي"
   - مثال: "Keeta Restaurant" → "فاتورة Keeta"
6. أخرج النص المحسّن فقط، بدون شرح أو تعليق

**السؤال الأصلي:**
"{user_query}"

**السؤال المحسّن:**
"""
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "أنت خبير في تحسين الأسئلة العربية. تحوّل اللهجة العامية إلى فصحى بدون تغيير المعنى."},
                {"role": "user", "content": refiner_prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        refined_query = response.choices[0].message.content.strip()
        
        # Remove any quotes or extra formatting
        refined_query = refined_query.strip('"').strip("'").strip()
        
        logger.info(f"✅ Refined Query: {refined_query}")
        return refined_query
        
    except Exception as e:
        logger.error(f"❌ Refiner Stage failed: {e}")
        # If refiner fails, return original query
        return user_query

# ═══════════════════════════════════════════════════════════════════════════════
# 🧭 STAGE 2: Router
# ═══════════════════════════════════════════════════════════════════════════════

class RouterDecision(BaseModel):
    """Router decision model"""
    mode: Literal["deep_sql", "rag", "hybrid", "none"]
    reason: str
    show_images: bool = False
    requested_vendor: Optional[str] = None


def route_query(refined_query: str) -> RouterDecision:
    """
    🧭 Router Stage:
    تحديد نوع المعالجة المطلوبة بناءً على نوع السؤال
    
    Args:
        refined_query: السؤال المحسّن من Refiner
    
    Returns:
        RouterDecision object with mode and reason
    """
    logger.info("🧭 Starting Router Stage...")
    logger.info(f"   Query: {refined_query}")
    
    try:
        router_prompt = f"""
أنت خبير في تصنيف الأسئلة المتعلقة بالفواتير.

**مهمتك:**
حدد نوع المعالجة المناسبة للسؤال التالي:

**أنواع المعالجة:**

1. **deep_sql** - للأسئلة التحليلية والإحصائية:
   - كم عدد؟ كم إجمالي؟ كم مجموع؟
   - أعلى، أقل، أكثر، أقل
   - متوسط، معدل
   - مثال: "كم عدد فواتيري؟" "ما أعلى فاتورة؟"

2. **rag** - للأسئلة المعنوية والنصية:
   - البحث عن فاتورة من متجر معين
   - فاتورة بنوع معين (مطعم، صيدلية، كافيه)
   - طلبات الصور (صورة فاتورة، ورّني صورة، أريد الصورة، invoice image)
   - مثال: "ابي فاتورة صب واي" "وريني فاتورة المطعم" "صورة فاتورة كتا"

3. **hybrid** - للجمع بين SQL والبحث الدلالي:
   - أسئلة تجمع بين التحليل والبحث النصي
   - مثال: "أعلى فاتورة من المطاعم" "كم فاتورة عندي من الصيدليات"

4. **none** - للأسئلة خارج نطاق الفواتير:
   - أسئلة عامة غير متعلقة بالفواتير
   - مثال: "وش الطقس اليوم؟" "كيف حالك؟"

**إضافي:**
- **show_images**: اجعلها true في هذه الحالات:
  * صورة أو صور (image/images) 
  * ورّني، شوفني، أريد أن أرى، ابي
  * فاتورة من متجر محدد (مثلاً: "فاتورة كتا" "فاتورة صب واي" "فاتورة مطعم")
  * أي سؤال عن فاتورة معينة (اسم متجر، نوع متجر، فرع)
  * **افتراضياً اجعلها true إلا للأسئلة الإحصائية فقط** (كم عدد، كم مجموع)
- **requested_vendor**: استخرج اسم المتجر الأساسي فقط:
  * إذا كان الاسم طويل (مثل: "شركة جيرة لتقديم المشروبات - فرع الأكاديمية") → أكتب "جيرة"
  * إذا كان بسيط (مثل: "كتا") → أكتب "كتا"
  * أمثلة: كتا، صب واي، جرير، بنده، جيرة، الدانوب، etc.

**السؤال:**
"{refined_query}"

**أخرج JSON فقط بهذا الشكل:**
{{
  "mode": "deep_sql" أو "rag" أو "hybrid" أو "none",
  "reason": "شرح قصير للسبب",
  "show_images": true أو false,
  "requested_vendor": "اسم المتجر" أو null
}}
"""
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "أنت خبير في تصنيف الأسئلة. أخرج JSON فقط."},
                {"role": "user", "content": router_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        router_output = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', router_output, re.DOTALL)
        if json_match:
            router_json = json.loads(json_match.group())
        else:
            router_json = json.loads(router_output)
        
        decision = RouterDecision(
            mode=router_json.get("mode", "none"),
            reason=router_json.get("reason", ""),
            show_images=router_json.get("show_images", False),
            requested_vendor=router_json.get("requested_vendor")
        )
        
        logger.info(f"✅ Router Decision: {decision.mode}")
        logger.info(f"   Reason: {decision.reason}")
        logger.info(f"   Show Images: {decision.show_images}")
        if decision.requested_vendor:
            logger.info(f"   Requested Vendor: {decision.requested_vendor}")
        
        return decision
        
    except Exception as e:
        logger.error(f"❌ Router Stage failed: {e}")
        # Default to hybrid mode if router fails
        return RouterDecision(
            mode="hybrid",
            reason=f"Router failed, defaulting to hybrid: {str(e)}"
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 🧮 STAGE 3: Executor
# ═══════════════════════════════════════════════════════════════════════════════

def execute_deep_sql(refined_query: str, db: Session) -> List[Dict]:
    """
    🧮 Execute deep SQL query for analytical questions
    
    Args:
        refined_query: السؤال المحسّن
        db: Database session
    
    Returns:
        List of results from database
    """
    logger.info("🧮 Executing Deep SQL...")
    
    try:
        # Generate SQL query using AI
        sql_prompt = f"""
أنت خبير في كتابة استعلامات SQL لقاعدة بيانات الفواتير.

**جدول الفواتير (invoices):**
- id (integer)
- invoice_number (varchar)
- invoice_date (timestamp)
- vendor (varchar) - اسم المتجر
- tax_number (varchar)
- cashier (varchar)
- branch (varchar)
- phone (varchar)
- subtotal (varchar)
- tax (varchar)
- total_amount (varchar) - المبلغ الإجمالي
- discounts (varchar)
- payment_method (varchar)
- category (varchar)
- invoice_type (text)
- ai_insight (text)
- image_url (text)
- is_valid_invoice (boolean)
- created_at (timestamp)

**السؤال:**
"{refined_query}"

**قواعد صارمة:**
1. استعلام SELECT فقط (ممنوع DELETE, UPDATE, INSERT)
2. استخدم أسماء الأعمدة الصحيحة من القائمة أعلاه
3. total_amount هو varchar، استخدم CAST لتحويله لرقم إذا لزم
4. للبحث عن نص، استخدم ILIKE مع %
5. أخرج SQL فقط، بدون شرح

**مثال:**
سؤال: "كم عدد فواتيري؟"
SQL: SELECT COUNT(*) as count FROM invoices WHERE is_valid_invoice = true

سؤال: "ما أعلى فاتورة؟"
SQL: SELECT * FROM invoices WHERE is_valid_invoice = true ORDER BY CAST(total_amount AS DECIMAL) DESC LIMIT 1

**SQL Query:**
"""
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
                messages=[
                {"role": "system", "content": "أنت خبير SQL. أخرج SQL فقط."},
                {"role": "user", "content": sql_prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Clean SQL query
        sql_query = sql_query.strip('```sql').strip('```').strip()
        
        logger.info(f"📊 Generated SQL: {sql_query}")
        
        # Safety check
        if not is_safe_sql(sql_query):
            logger.error("🚫 Unsafe SQL query rejected")
            return []
        
        # Execute SQL
        rows = db.execute(text(sql_query)).fetchall()
        results = [serialize_for_json(dict(row._mapping)) for row in rows]
        
        logger.info(f"✅ SQL returned {len(results)} results")
        return results
        
    except Exception as e:
        logger.error(f"❌ Deep SQL execution failed: {e}")
        return []


def execute_rag(refined_query: str, db: Session, top_k: int = 5) -> List[Dict]:
    """
    🔍 Execute RAG (Retrieval-Augmented Generation) using embeddings
    
    Args:
        refined_query: السؤال المحسّن
        db: Database session
        top_k: Number of top results to return
    
    Returns:
        List of semantically similar invoices
    """
    logger.info("🔍 Executing RAG (Semantic Search with embeddings)...")
    
    try:
        # Generate embedding for user query
        embedding_response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=refined_query
        )
        
        query_embedding = np.array(embedding_response.data[0].embedding)
        logger.info(f"✅ Generated query embedding (dim: {len(query_embedding)})")
        
        # Get all invoices with embeddings - CORRECT TABLE NAME!
        sql = text("""
            SELECT i.*, e.embedding
            FROM invoices i
            LEFT JOIN invoice_embeddings e ON i.id = e.invoice_id
            WHERE i.is_valid_invoice = true
            AND e.embedding IS NOT NULL
            AND i.image_url IS NOT NULL
        """)
        
        rows = db.execute(sql).fetchall()
        logger.info(f"📊 Found {len(rows)} invoices with embeddings")
        
        if not rows:
            logger.warning("⚠️ No invoices with embeddings found")
            return []
        
        # Calculate similarities using pgvector
        similarities = []
        for row in rows:
            row_dict = dict(row._mapping)
            
            # Parse embedding (pgvector returns it as a list)
            embedding_data = row_dict.get('embedding')
            if not embedding_data:
                continue
            
            try:
                # Convert to numpy array if it's a list
                if isinstance(embedding_data, list):
                    invoice_embedding = np.array(embedding_data)
                elif isinstance(embedding_data, str):
                    invoice_embedding = np.array(json.loads(embedding_data))
                else:
                    invoice_embedding = np.array(embedding_data)
                
                similarity = cosine_similarity(query_embedding, invoice_embedding)
                
                similarities.append({
                    'invoice': row_dict,
                    'similarity': float(similarity)
                })
            except Exception as e:
                logger.debug(f"Failed to process embedding for invoice {row_dict.get('id')}: {e}")
                continue
        
        # Sort by similarity and get top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_results = similarities[:top_k]
        
        results = [item['invoice'] for item in top_results]
        
        logger.info(f"✅ RAG returned {len(results)} results")
        for i, item in enumerate(top_results[:3], 1):
            logger.info(f"   {i}. {item['invoice'].get('vendor', 'Unknown')} (similarity: {item['similarity']:.3f})")
        
        return results
    
    except Exception as e:
        logger.error(f"❌ RAG execution failed: {e}")
        
        # Rollback the failed transaction first
        try:
            db.rollback()
            logger.info("🔄 Transaction rolled back after RAG failure")
        except Exception as rollback_error:
            logger.warning(f"⚠️ Rollback warning: {rollback_error}")
        
        # Fallback: Super flexible SQL search (NO embeddings table)
        try:
            logger.info("🔄 Falling back to Basic SQL search (no embeddings)...")
            
            # Clean keywords - remove ALL Arabic filter words
            keywords = (refined_query
                       .replace("فاتورة", "")
                       .replace("صورة", "")
                       .replace("ابي", "")
                       .replace("وريني", "")
                       .replace("مطعم", "")
                       .replace("متجر", "")
                       .replace("من", "")
                       .replace("في", "")
                       .replace("أريد", "")
                       .replace("كم", "")
                       .replace("أنفقت", "")
                       .replace("على", "")
                       .replace("؟", "")
                       .strip())
            
            logger.info(f"🔍 Original query: '{refined_query}'")
            logger.info(f"🔍 Extracted keywords: '{keywords}'")
            
            # If still empty after cleaning, try to get ALL invoices with images
            if not keywords or len(keywords) < 2:
                logger.warning("⚠️ No valid keywords, returning ALL recent invoices with images...")
                sql_fallback = text("""
                    SELECT *
                    FROM invoices
                    WHERE is_valid_invoice = true
                    AND image_url IS NOT NULL
                    ORDER BY created_at DESC
                    LIMIT :limit
                """)
                
                rows = db.execute(sql_fallback, {"limit": top_k}).fetchall()
            else:
                # Search in basic invoice fields only (NO embeddings)
                sql_fallback = text("""
                    SELECT *
                    FROM invoices
                    WHERE is_valid_invoice = true
                    AND image_url IS NOT NULL
                    AND (
                        LOWER(vendor) LIKE LOWER(:keyword_pattern)
                        OR LOWER(category::text) LIKE LOWER(:keyword_pattern)
                        OR LOWER(invoice_type) LIKE LOWER(:keyword_pattern)
                        OR LOWER(branch) LIKE LOWER(:keyword_pattern)
                        OR LOWER(invoice_number) LIKE LOWER(:keyword_pattern)
                    )
                    ORDER BY 
                        CASE 
                            WHEN LOWER(vendor) LIKE LOWER(:keyword_start) THEN 1
                            WHEN LOWER(vendor) LIKE LOWER(:keyword_pattern) THEN 2
                            ELSE 3
                        END,
                        created_at DESC
                    LIMIT :limit
                """)
                
                rows = db.execute(
                    sql_fallback, 
                    {
                        "keyword_pattern": f"%{keywords}%",
                        "keyword_start": f"{keywords}%",
                        "limit": top_k * 2  # Get more results for better matching
                    }
                ).fetchall()
            
            results = [serialize_for_json(dict(row._mapping)) for row in rows]
            logger.info(f"✅ SQL Fallback returned {len(results)} results")
            
            if results:
                logger.info("📋 Top results:")
                for i, item in enumerate(results[:5], 1):
                    vendor = item.get('vendor', 'Unknown')
                    has_image = bool(item.get('image_url'))
                    logger.info(f"   {i}. {vendor} (image: {has_image})")
            else:
                logger.warning(f"⚠️ No results found for keywords: '{keywords}'")
            
            return results[:top_k]  # Return only top_k results
            
        except Exception as fallback_error:
            logger.error(f"❌ SQL Fallback failed: {fallback_error}")
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
        
        return []


def execute_hybrid(refined_query: str, db: Session) -> List[Dict]:
    """
    🔄 Execute hybrid approach: SQL first, then RAG
    
    Args:
        refined_query: السؤال المحسّن
        db: Database session
    
    Returns:
        Combined results from SQL and RAG
    """
    logger.info("🔄 Executing Hybrid (SQL + RAG)...")
    
    try:
        # Try SQL first
        sql_results = execute_deep_sql(refined_query, db)
        
        if sql_results and len(sql_results) > 0:
            logger.info(f"✅ SQL found {len(sql_results)} results, using SQL results")
            return sql_results
        
        # Fallback to RAG if SQL returns nothing
        logger.info("⚠️ SQL returned no results, falling back to RAG...")
        rag_results = execute_rag(refined_query, db)
        
        logger.info(f"✅ Hybrid returned {len(rag_results)} results (from RAG)")
        return rag_results
        
    except Exception as e:
        logger.error(f"❌ Hybrid execution failed: {e}")
        return []


def execute_query(refined_query: str, decision: RouterDecision, db: Session) -> List[Dict]:
    """
    🚀 Main executor - ALWAYS uses RAG/Embeddings with SQL fallback
    
    Args:
        refined_query: السؤال المحسّن
        decision: Router decision
        db: Database session
    
    Returns:
        List of results
    """
    logger.info(f"🚀 Starting RAG Executor (embeddings-based search)...")
    
    if decision.mode == "none":
        logger.info("ℹ️ Query is out of scope (mode: none)")
        return []
    
    # ALWAYS use RAG (embeddings + SQL fallback)
    return execute_rag(refined_query, db)

# ═══════════════════════════════════════════════════════════════════════════════
# ✅ STAGE 4: Validator
# ═══════════════════════════════════════════════════════════════════════════════

def validate_results(results: List[Dict], refined_query: str) -> bool:
    """
    ✅ Validate that results actually match the query
    
    Args:
        results: Results from executor
        refined_query: السؤال المحسّن
    
    Returns:
        True if results are valid and relevant, False otherwise
    """
    logger.info("✅ Starting Validator Stage...")
    
    if not results or len(results) == 0:
        logger.warning("⚠️ No results to validate")
        return False
    
    logger.info(f"✅ Validated {len(results)} results")
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# 💬 STAGE 5: Replier
# ═══════════════════════════════════════════════════════════════════════════════

def generate_reply(refined_query: str, results: List[Dict], decision: RouterDecision) -> str:
    """
    💬 Generate final reply in Arabic with friendly tone
    
    Args:
        refined_query: السؤال المحسّن
        results: Results from executor
        decision: Router decision
    
    Returns:
        Final reply string in Arabic
    """
    logger.info("💬 Starting Replier Stage...")
    
    try:
        # Handle out of scope
        if decision.mode == "none":
            logger.info("ℹ️ Query out of scope, returning generic reply")
            return "هذا خارج اختصاصي، أنا متخصص فقط في تحليل فواتيرك 💡"
        
        # Handle no results
        if not results or len(results) == 0:
            logger.info("ℹ️ No results found")
            return "ما لقيت فواتير تطابق بحثك 😔"
        
        # Generate reply based on results
        reply_prompt = f"""
أنت مساعد ذكي في نظام مُفَوْتِر لإدارة الفواتير.

**سؤال المستخدم:**
"{refined_query}"

**البيانات المسترجعة:**
{json.dumps(serialize_for_json(results[:3]), ensure_ascii=False, indent=2)}

**قواعد الرد (التزم بها بدقة):**

1. **للأسئلة الإحصائية (كم عدد، كم إجمالي):**
   - رد مختصر جداً: "عندك X فواتير 📄"
   - لا تذكر أي تفاصيل فواتير!

2. **للأسئلة عن فاتورة محددة أو طلب صورة:**
   - رد بسيط: "لقيت فاتورة [المتجر] 🧾"
   - إذا كانت هناك صور: "هذي صورة الفاتورة 📸"
   - أو: "تمام! هذه فاتورة [المتجر] بمبلغ [X] ﷼"

3. **للأسئلة التحليلية (أعلى، أقل):**
   - "أعلى فاتورة عندك [X] ﷼ من [المتجر] 💰"

4. **إذا لا توجد نتائج:**
   - "ما لقيت فواتير بهذا الوصف 😔"

**أسلوب الرد:**
- عربي فصيح مع لهجة سعودية خفيفة
- مختصر وواضح ومباشر
- استخدم emoji مناسب
- الصور تظهر تلقائياً، لا داعي لتفصيل

**الرد:**
"""
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
                messages=[
                {
                    "role": "system",
                    "content": """أنت مساعد ذكي في نظام مُفَوْتِر.
أسلوبك: عربي فصيح مع لهجة سعودية خفيفة، مختصر وواضح.
لا تذكر أكواد أو JSON، فقط ردود طبيعية."""
                },
                {"role": "user", "content": reply_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        final_reply = response.choices[0].message.content.strip()
        
        logger.info(f"✅ Generated reply: {final_reply[:100]}...")
        return final_reply
        
    except Exception as e:
        logger.error(f"❌ Replier Stage failed: {e}")
        return "عذراً، حدث خطأ في صياغة الرد 😔"

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 Main Endpoint
# ═══════════════════════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str


@router.post("/ask")
async def chat_ask(request: ChatRequest, db: Session = Depends(get_db)):
    """
    🎯 Main Chat Endpoint
    
    Process user query through all stages:
    1. Refiner  - تحسين السؤال
    2. Router   - تحديد نوع المعالجة
    3. Executor - تنفيذ الاستعلام
    4. Validator - التحقق من النتائج
    5. Replier  - صياغة الرد
    
    Args:
        request: ChatRequest with user message
        db: Database session
    
    Returns:
        JSON response with reply and data
    """
    logger.info("="*80)
    logger.info("🎯 NEW CHAT REQUEST")
    logger.info(f"📝 User Message: {request.message}")
    logger.info("="*80)
    
    try:
        user_query = request.message.strip()
        
        # ════════════════════════════════════════════════════════════════════
        # Stage 1: Refiner
        # ════════════════════════════════════════════════════════════════════
        refined_query = refine_user_query(user_query)
        
        # ════════════════════════════════════════════════════════════════════
        # Stage 2: Router
        # ════════════════════════════════════════════════════════════════════
        decision = route_query(refined_query)
        
        # ════════════════════════════════════════════════════════════════════
        # Stage 3: Executor
        # ════════════════════════════════════════════════════════════════════
        results = execute_query(refined_query, decision, db)
        
        # ════════════════════════════════════════════════════════════════════
        # Stage 4: Validator
        # ════════════════════════════════════════════════════════════════════
        is_valid = validate_results(results, refined_query)
        
        # ════════════════════════════════════════════════════════════════════
        # Stage 5: Replier
        # ════════════════════════════════════════════════════════════════════
        final_reply = generate_reply(refined_query, results, decision)
        
        # ════════════════════════════════════════════════════════════════════
        # Format invoices for frontend
        # ════════════════════════════════════════════════════════════════════
        invoices_for_display = []
        if decision.show_images and results:
            for item in results:
                formatted = format_invoice_for_frontend(item)
                
                # Filter by requested vendor if specified
                if decision.requested_vendor:
                    item_vendor = (item.get("vendor") or "").lower()
                    vendor_filter = decision.requested_vendor.lower()
                    
                    if vendor_filter not in item_vendor:
                        continue
                
                if formatted.get("id") and formatted.get("vendor"):
                    invoices_for_display.append(formatted)
            
        # ════════════════════════════════════════════════════════════════════
        # Save to context
        # ════════════════════════════════════════════════════════════════════
        if invoices_for_display:
            context.add_context(
                intent=user_query,
                invoices=invoices_for_display[:3],
                mode=decision.mode
            )
            logger.info(f"💾 Saved {len(invoices_for_display[:3])} invoices to context")
        
        # ════════════════════════════════════════════════════════════════════
        # Final Response
        # ════════════════════════════════════════════════════════════════════
        logger.info("="*80)
        logger.info(f"✅ CHAT RESPONSE READY")
        logger.info(f"   Mode: {decision.mode}")
        logger.info(f"   Results: {len(results)}")
        logger.info(f"   Invoices to display: {len(invoices_for_display)}")
        logger.info(f"   Reply: {final_reply[:100]}...")
        logger.info("="*80)

        return {
            "reply": final_reply,
            "invoices": invoices_for_display if invoices_for_display else None,
            "mode": decision.mode,
            "result_count": len(results),
            "show_images": decision.show_images,
            "is_valid": is_valid,
            "refined_query": refined_query
        }

    except Exception as e:
        logger.error("="*80)
        logger.error(f"❌ CHAT ERROR: {e}")
        logger.error("="*80)
        
        return {
            "reply": "عذراً، حدث خطأ أثناء معالجة طلبك 😔 الرجاء المحاولة مرة أخرى.",
            "error": str(e),
            "mode": "error",
            "result_count": 0
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 Additional Helper Endpoints
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/context")
async def get_context():
    """Get current conversation context"""
    return {
        "last_intents": context.last_3_intents,
        "last_invoices_count": len(context.get_last_invoices()),
        "last_modes": context.last_3_modes
    }


@router.post("/context/clear")
async def clear_context():
    """Clear conversation context"""
    context.clear()
    logger.info("🗑️ Context cleared")
    return {"status": "Context cleared successfully"}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "مُفَوْتِر Chat AI",
        "version": "2.0.0"
        }
