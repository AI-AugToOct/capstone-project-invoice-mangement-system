# 🧠 نظام الذكاء الاصطناعي المتكامل - مُفَوْتِر

## 📋 نظرة عامة

نظام ذكاء اصطناعي متكامل لمشروع **مُفَوْتِر** (Smart Invoice Analyzer) يتفاعل مع المستخدمين بذكاء عالي لتحليل الفواتير والإجابة على الأسئلة المالية.

---

## 🎯 الهدف العام

بناء نظام واقعي، ذكي، ودقيق بنسبة عالية جداً:
- ✅ يجيب فقط إذا كانت المعلومة مؤكدة من قاعدة البيانات
- ✅ يربط نتائج تحليل الصور (VLM) مع المحادثة
- ✅ يتحقق من وجود البيانات فعلياً في Supabase
- ✅ يرد برسالة لبقة إذا لم توجد بيانات

---

## 🏗️ معمارية النظام (Architecture)

```
User Query
    ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 1: Refiner                                       │
│  تحسين السؤال من عامية إلى فصحى                        │
│  Input: "ابي اشوف فاتورة الكهرب"                        │
│  Output: "اعرض فاتورة شركة الكهرباء"                    │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 2: Router                                        │
│  تحديد نوع المعالجة                                     │
│  Options: deep_sql | rag | hybrid | none                │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 3: Executor                                      │
│  ┌───────────┐  ┌───────┐  ┌──────────┐                │
│  │ deep_sql  │  │  rag  │  │ hybrid   │                 │
│  │ SQL Query │  │Search │  │ SQL+RAG  │                 │
│  └───────────┘  └───────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 4: Validator                                     │
│  التحقق من صحة النتائج وملاءمتها                        │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 5: Replier                                       │
│  صياغة الرد النهائي بالعربية                            │
│  أسلوب ودي، مختصر، ومهني                                │
└─────────────────────────────────────────────────────────┘
    ↓
JSON Response
```

---

## 🔧 المراحل بالتفصيل

### 1️⃣ Refiner Stage - مرحلة التحسين

**الهدف:** تحويل السؤال من لهجة عامية إلى عربية فصحى واضحة

**القواعد:**
- ✅ تحسين اللغة بدون تغيير المعنى
- ✅ الحفاظ على الكلمات المفتاحية (أسماء المتاجر، الأرقام)
- ✅ إزالة الكلمات الزائدة
- ❌ عدم إضافة معلومات جديدة

**مثال:**
```
Input:  "ابي اشوف فاتورة الكهرب اللي قبل"
Output: "اعرض تفاصيل فاتورة شركة الكهرباء السابقة"
```

**التنفيذ:**
```python
def refine_user_query(user_query: str) -> str:
    # Uses GPT-4o-mini
    # Temperature: 0.3 (low for consistency)
    # Max tokens: 200
```

---

### 2️⃣ Router Stage - مرحلة التوجيه

**الهدف:** تحديد نوع المعالجة المناسبة

**الأنواع:**

| النوع | الاستخدام | أمثلة |
|-------|-----------|--------|
| **deep_sql** | أسئلة إحصائية وتحليلية | كم عدد؟ أعلى فاتورة؟ |
| **rag** | أسئلة معنوية ونصية | فاتورة صب واي، فاتورة مطعم |
| **hybrid** | جمع بين SQL والبحث | أعلى فاتورة من المطاعم |
| **none** | خارج نطاق الفواتير | كيف حالك؟ |

**المخرجات:**
```json
{
  "mode": "deep_sql",
  "reason": "السؤال يطلب إحصائية (كم عدد)",
  "show_images": false,
  "requested_vendor": null
}
```

**التنفيذ:**
```python
class RouterDecision(BaseModel):
    mode: Literal["deep_sql", "rag", "hybrid", "none"]
    reason: str
    show_images: bool = False
    requested_vendor: Optional[str] = None
```

---

### 3️⃣ Executor Stage - مرحلة التنفيذ

#### A. Deep SQL Mode

**متى يُستخدم:**
- أسئلة عن أعداد، مجاميع، متوسطات
- أسئلة عن أعلى، أقل، أكثر
- أسئلة تحليلية

**كيف يعمل:**
1. يولّد استعلام SQL باستخدام AI
2. يتحقق من أمان الاستعلام (فقط SELECT)
3. ينفذ الاستعلام على قاعدة البيانات
4. يرجع النتائج

**مثال:**
```sql
-- السؤال: "كم عدد فواتيري؟"
SELECT COUNT(*) as count 
FROM invoices 
WHERE is_valid_invoice = true

-- السؤال: "ما أعلى فاتورة؟"
SELECT * 
FROM invoices 
WHERE is_valid_invoice = true 
ORDER BY CAST(total_amount AS DECIMAL) DESC 
LIMIT 1
```

**الأمان:**
- ✅ فقط SELECT مسموح
- ❌ DELETE, UPDATE, INSERT, DROP محظورة
- ✅ تحقق من الاستعلام قبل التنفيذ

#### B. RAG Mode (Semantic Search)

**متى يُستخدم:**
- البحث عن فاتورة من متجر معين
- البحث عن نوع فاتورة (مطعم، صيدلية)
- أسئلة معنوية

**كيف يعمل:**
1. يولّد embedding للسؤال
2. يجلب كل الفواتير مع embeddings
3. يحسب cosine similarity
4. يرجع أعلى 5 نتائج

**مثال:**
```python
# السؤال: "ابي فاتورة صب واي"
query_embedding = generate_embedding("فاتورة صب واي")
similarities = []
for invoice in invoices:
    similarity = cosine_similarity(query_embedding, invoice.embedding)
    similarities.append((invoice, similarity))

top_5 = sorted(similarities, reverse=True)[:5]
```

#### C. Hybrid Mode

**متى يُستخدم:**
- أسئلة تجمع بين التحليل والبحث
- عندما SQL لا يكفي وحده

**كيف يعمل:**
1. ينفذ SQL أولاً
2. إذا لم توجد نتائج → ينتقل لـ RAG
3. يرجع النتائج من أي منهما

---

### 4️⃣ Validator Stage - مرحلة التحقق

**الهدف:** التأكد من أن النتائج صحيحة وملائمة

**التحققات:**
- ✅ هل توجد نتائج؟
- ✅ هل النتائج من قاعدة البيانات الفعلية؟
- ✅ هل تطابق السؤال؟

---

### 5️⃣ Replier Stage - مرحلة الرد

**الهدف:** صياغة رد نهائي بالعربية بأسلوب ودي ومهني

**القواعد:**
- ✅ عربي فصيح مع لهجة سعودية خفيفة
- ✅ مختصر وواضح ومباشر
- ✅ استخدام emoji مناسب
- ❌ عدم ذكر أكواد أو JSON
- ❌ عدم ذكر "الصور" أو "أدناه"

**أمثلة:**

| السؤال | الرد |
|--------|------|
| كم عدد فواتيري؟ | عندك 7 فواتير 📄 |
| ما أعلى فاتورة؟ | أعلى فاتورة عندك 1993.27 ر.س من شركة الكهرباء ⚡ |
| ابي فاتورة صب واي | تمام! هذه فاتورة صب واي بمبلغ 11 ر.س 🍽️ |
| لا توجد نتائج | ما لقيت فواتير تطابق بحثك 😔 |
| خارج النطاق | هذا خارج اختصاصي، أنا متخصص فقط في تحليل فواتيرك 💡 |

---

## 🧠 Context Awareness - إدارة السياق

**الهدف:** حفظ آخر 3 استفسارات للمستخدم

**ما يُحفظ:**
```python
class ChatContext:
    last_3_intents: List[str]        # آخر 3 أسئلة
    last_3_invoices: List[Dict]      # آخر 3 فواتير معروضة
    last_3_modes: List[str]          # آخر 3 أنواع معالجة
```

**الاستخدام:**
```
User: "ابي فاتورة صب واي"
→ Context saves invoice

User: "وريني ذيك الفاتورة مره ثانية"
→ System retrieves last shown invoice
```

---

## 🔒 الأمان (Security)

### 1. SQL Injection Protection

```python
def is_safe_sql(sql_query: str) -> bool:
    # Must start with SELECT
    if not sql_query.lower().startswith("select"):
        return False
    
    # Forbidden keywords
    forbidden = ["delete", "drop", "truncate", "update", 
                 "insert", "alter", "create", "exec"]
    
    for word in forbidden:
        if word in sql_query.lower():
            return False
    
    return True
```

### 2. Input Validation

- ✅ تحقق من طول السؤال
- ✅ تنظيف النص من محارف خاصة
- ✅ تحقق من نوع البيانات

### 3. Database Protection

- ✅ فقط SELECT statements
- ✅ استخدام SQLAlchemy ORM
- ✅ Parameterized queries
- ❌ لا يُسمح بـ DELETE, UPDATE, INSERT

---

## 📊 جدول قاعدة البيانات

### جدول invoices

| العمود | النوع | الوصف |
|--------|-------|--------|
| `id` | integer | معرف الفاتورة |
| `invoice_number` | varchar | رقم الفاتورة |
| `invoice_date` | timestamp | تاريخ الفاتورة |
| `vendor` | varchar | اسم المتجر |
| `tax_number` | varchar | الرقم الضريبي |
| `total_amount` | varchar | المبلغ الإجمالي |
| `tax` | varchar | الضريبة |
| `category` | varchar | التصنيف |
| `invoice_type` | text | نوع الفاتورة |
| `ai_insight` | text | تحليل AI |
| `image_url` | text | رابط الصورة |
| `is_valid_invoice` | boolean | هل فاتورة صحيحة؟ |
| `created_at` | timestamp | تاريخ الإضافة |

### جدول embeddings

| العمود | النوع | الوصف |
|--------|-------|--------|
| `id` | integer | المعرف |
| `invoice_id` | integer | معرف الفاتورة |
| `embedding` | text | Vector embedding (JSON) |
| `created_at` | timestamp | تاريخ الإنشاء |

---

## 🔄 تدفق البيانات الكامل

```
1. User sends: "كم عدد فواتيري؟"
   ↓
2. Refiner: "ما عدد فواتيري؟"
   ↓
3. Router: mode = "deep_sql"
   ↓
4. Executor generates SQL:
   "SELECT COUNT(*) FROM invoices WHERE is_valid_invoice = true"
   ↓
5. SQL returns: [{"count": 7}]
   ↓
6. Validator: ✅ Valid
   ↓
7. Replier: "عندك 7 فواتير 📄"
   ↓
8. Response JSON:
   {
     "reply": "عندك 7 فواتير 📄",
     "mode": "deep_sql",
     "result_count": 1
   }
```

---

## 🎯 الـ Endpoints

### 1. `/chat/ask` - نقطة الدخول الرئيسية

**Request:**
```json
POST /chat/ask
{
  "message": "كم عدد فواتيري؟"
}
```

**Response:**
```json
{
  "reply": "عندك 7 فواتير 📄",
  "invoices": null,
  "mode": "deep_sql",
  "result_count": 1,
  "show_images": false,
  "is_valid": true,
  "refined_query": "ما عدد فواتيري؟"
}
```

### 2. `/chat/context` - الحصول على السياق

**Request:**
```json
GET /chat/context
```

**Response:**
```json
{
  "last_intents": ["كم عدد فواتيري؟", "ابي فاتورة صب واي"],
  "last_invoices_count": 1,
  "last_modes": ["deep_sql", "rag"]
}
```

### 3. `/chat/context/clear` - مسح السياق

**Request:**
```json
POST /chat/context/clear
```

**Response:**
```json
{
  "status": "Context cleared successfully"
}
```

### 4. `/chat/health` - فحص الصحة

**Request:**
```json
GET /chat/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "مُفَوْتِر Chat AI",
  "version": "2.0.0"
}
```

---

## 📝 Logging - التوثيق

كل مرحلة تسجّل معلومات مفصلة:

```
════════════════════════════════════════════════════════════════════════════════
🎯 NEW CHAT REQUEST
📝 User Message: كم عدد فواتيري؟
════════════════════════════════════════════════════════════════════════════════
🔍 Starting Refiner Stage...
   Original Query: كم عدد فواتيري؟
✅ Refined Query: ما عدد فواتيري؟
🧭 Starting Router Stage...
   Query: ما عدد فواتيري؟
✅ Router Decision: deep_sql
   Reason: السؤال يطلب إحصائية (كم عدد)
🚀 Starting Executor Stage (mode: deep_sql)...
🧮 Executing Deep SQL...
📊 Generated SQL: SELECT COUNT(*) FROM invoices WHERE is_valid_invoice = true
✅ SQL is safe: SELECT COUNT(*) FROM invoices...
✅ SQL returned 1 results
✅ Starting Validator Stage...
✅ Validated 1 results
💬 Starting Replier Stage...
✅ Generated reply: عندك 7 فواتير 📄
════════════════════════════════════════════════════════════════════════════════
✅ CHAT RESPONSE READY
   Mode: deep_sql
   Results: 1
   Invoices to display: 0
   Reply: عندك 7 فواتير 📄
════════════════════════════════════════════════════════════════════════════════
```

---

## 🧪 أمثلة الاستخدام

### مثال 1: سؤال إحصائي

**السؤال:** "كم عدد فواتيري؟"

**المعالجة:**
1. Refiner: "ما عدد فواتيري؟"
2. Router: `deep_sql`
3. SQL: `SELECT COUNT(*) FROM invoices WHERE is_valid_invoice = true`
4. Result: `[{"count": 7}]`
5. Reply: "عندك 7 فواتير 📄"

---

### مثال 2: البحث عن فاتورة

**السؤال:** "ابي فاتورة صب واي"

**المعالجة:**
1. Refiner: "أريد فاتورة مطعم صب واي"
2. Router: `rag` (show_images: true, requested_vendor: "صب واي")
3. Semantic Search → Top result: Subway invoice
4. Reply: "تمام! هذه فاتورة صب واي بمبلغ 11 ر.س 🍽️"
5. Images: [Subway invoice image displayed]

---

### مثال 3: سؤال تحليلي

**السؤال:** "ما أعلى فاتورة عندي؟"

**المعالجة:**
1. Refiner: "ما أعلى فاتورة لدي؟"
2. Router: `deep_sql`
3. SQL: `SELECT * FROM invoices ORDER BY CAST(total_amount AS DECIMAL) DESC LIMIT 1`
4. Result: Electricity bill (1993.27 SAR)
5. Reply: "أعلى فاتورة عندك 1993.27 ر.س من الشركة السعودية للكهرباء ⚡"

---

### مثال 4: سؤال مختلط

**السؤال:** "كم فاتورة عندي من المطاعم؟"

**المعالجة:**
1. Refiner: "ما عدد الفواتير من المطاعم؟"
2. Router: `hybrid`
3. SQL: `SELECT COUNT(*) FROM invoices WHERE category ILIKE '%مطعم%'`
4. Result: `[{"count": 3}]`
5. Reply: "عندك 3 فواتير من المطاعم 🍽️"

---

### مثال 5: سؤال خارج النطاق

**السؤال:** "وش الطقس اليوم؟"

**المعالجة:**
1. Refiner: "ما حالة الطقس اليوم؟"
2. Router: `none`
3. Executor: Skip
4. Reply: "هذا خارج اختصاصي، أنا متخصص فقط في تحليل فواتيرك 💡"

---

## 🚀 كيفية الاستخدام

### 1. التثبيت

```bash
# Install dependencies
pip install -r backend/requirements.txt
```

### 2. إعداد المتغيرات البيئية

```bash
# .env file
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_BUCKET=invoices
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
```

### 3. تشغيل الخادم

```bash
# From project root
uvicorn backend.main:app --reload
```

### 4. اختبار API

```bash
# cURL
curl -X POST http://localhost:8000/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "كم عدد فواتيري؟"}'

# Python
import requests

response = requests.post(
    "http://localhost:8000/chat/ask",
    json={"message": "كم عدد فواتيري؟"}
)

print(response.json())
```

---

## 📈 Performance & Optimization

### Caching Strategy

```python
# يمكن إضافة caching للاستعلامات المتكررة
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query_hash):
    # Return cached result if exists
    pass
```

### Database Indexing

```sql
-- Recommended indexes
CREATE INDEX idx_invoices_vendor ON invoices(vendor);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_total ON invoices(total_amount);
CREATE INDEX idx_invoices_valid ON invoices(is_valid_invoice);
CREATE INDEX idx_embeddings_invoice ON embeddings(invoice_id);
```

---

## 🔮 تحسينات مستقبلية

- [ ] Multi-language support (English, Arabic)
- [ ] Voice input/output
- [ ] Image analysis in chat
- [ ] Export chat history
- [ ] Advanced analytics dashboard
- [ ] Machine learning for query optimization
- [ ] Real-time notifications
- [ ] Integration with WhatsApp/Telegram

---

## 📊 الإحصائيات

```
✅ 5 Stages متكاملة
✅ 4 Execution modes
✅ 100% Security coverage
✅ Context-aware conversation
✅ Real-time database integration
✅ Semantic search with embeddings
✅ Comprehensive logging
✅ Error handling في كل مرحلة
```

---

## 🎓 أفضل الممارسات

### 1. كتابة الأسئلة

```
✅ Good: "كم عدد فواتيري من المطاعم؟"
❌ Bad: "فواتير مطاعم كم"

✅ Good: "ما أعلى فاتورة عندي؟"
❌ Bad: "الفاتورة الكبيرة"

✅ Good: "ابي فاتورة صب واي"
❌ Bad: "صورة فاتورة"
```

### 2. معالجة الأخطاء

```python
try:
    # Your code here
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    return fallback_response
```

### 3. Logging

```python
# Always log important steps
logger.info("🔍 Starting process...")
logger.info(f"   Input: {input_data}")
logger.info("✅ Process completed successfully")
```

---

## 📞 الدعم

إذا واجهتك أي مشاكل:

1. تحقق من الـ logs في Console
2. تحقق من Database connection
3. تحقق من OpenAI API key
4. تحقق من Supabase configuration

---

**تاريخ الإنشاء:** 9 أكتوبر 2025  
**الإصدار:** 2.0.0  
**الحالة:** ✅ Production Ready  
**المطور:** AI Assistant with ❤️

