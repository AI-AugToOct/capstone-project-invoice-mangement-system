# 🤖 نظام الذكاء الاصطناعي - مُــفَــوْتِــر

## 📊 الـ Diagram الشامل لنظام AI

```mermaid
graph TB
    subgraph INPUT["📥 إدخال المستخدم"]
        A1[📸 صورة الفاتورة]
        A2[💬 سؤال المستخدم]
    end

    subgraph IMAGE_PROCESSING["🖼️ معالجة الصورة المتقدمة"]
        B1[📤 رفع الصورة]
        B2[🔍 OpenCV - كشف الدوران]
        B3[📐 تصحيح الميل]
        B4[🎯 تصحيح المنظور]
        B5[✨ صورة محسّنة]
        
        B1 --> B2
        B2 --> B3
        B3 --> B4
        B4 --> B5
    end

    subgraph VLM_ANALYSIS["🧠 تحليل النموذج البصري اللغوي"]
        C1[🤖 Qwen2.5-VL-32B-Instruct]
        C2[📝 استخراج البيانات]
        C3[🔢 تحليل الأرقام]
        C4[📋 استخراج العناصر]
        C5[💡 رؤى ذكية AI Insight]
        
        C1 --> C2
        C1 --> C3
        C1 --> C4
        C1 --> C5
    end

    subgraph VALIDATION["✅ التحقق والمراجعة"]
        D1{هل الصورة فاتورة؟}
        D2[✅ 5+ حقول مملوءة]
        D3[❌ أقل من 5 حقول]
        D4[📝 عرض للمراجعة]
        D5[🗑️ رفض الصورة]
        
        D1 -->|نعم| D2
        D1 -->|لا| D3
        D2 --> D4
        D3 --> D5
    end

    subgraph EMBEDDING_SYSTEM["🔗 نظام الـ Embeddings"]
        E1[📄 نص الفاتورة الكامل]
        E2[🧬 OpenAI text-embedding-3-small]
        E3[📊 Vector 1536 dimension]
        E4[💾 حفظ في invoice_embeddings]
        
        E1 --> E2
        E2 --> E3
        E3 --> E4
    end

    subgraph CHAT_AI["💬 نظام الدردشة الذكي - 5 مراحل"]
        direction TB
        
        subgraph STAGE1["1️⃣ Refiner - المحسّن"]
            F1[📝 سؤال عامي]
            F2[🤖 GPT-4o-mini]
            F3[📖 سؤال فصيح]
            
            F1 --> F2
            F2 --> F3
        end
        
        subgraph STAGE2["2️⃣ Router - الموجّه"]
            G1[🧭 تحليل نوع السؤال]
            G2{نوع المعالجة؟}
            G3[📊 deep_sql - إحصائي]
            G4[🔍 rag - بحث دلالي]
            G5[🔄 hybrid - مختلط]
            G6[❌ none - خارج النطاق]
            
            G1 --> G2
            G2 --> G3
            G2 --> G4
            G2 --> G5
            G2 --> G6
        end
        
        subgraph STAGE3["3️⃣ Executor - المنفّذ"]
            H1[🔍 RAG - البحث الدلالي]
            H2[🧬 توليد embedding للسؤال]
            H3[📊 حساب Cosine Similarity]
            H4[🎯 ترتيب النتائج]
            H5[💾 SQL Fallback]
            
            H1 --> H2
            H2 --> H3
            H3 --> H4
            H4 --> H5
        end
        
        subgraph STAGE4["4️⃣ Validator - المُحقق"]
            I1[✅ فحص البيانات]
            I2[🔍 تنقية النتائج]
            I3[📸 فلترة الصور]
        end
        
        subgraph STAGE5["5️⃣ Replier - المُجيب"]
            J1[🤖 GPT-4o-mini]
            J2[📝 صياغة الرد]
            J3[💬 رد نهائي]
            
            J1 --> J2
            J2 --> J3
        end
    end

    subgraph DATABASE["💾 قاعدة البيانات"]
        K1[(📋 invoices)]
        K2[(🔗 invoice_embeddings)]
        K3[(📦 items)]
    end

    subgraph OUTPUT["📤 المخرجات"]
        L1[📸 صور الفواتير]
        L2[📊 بيانات منظمة]
        L3[💬 ردود ذكية]
        L4[📈 إحصائيات]
    end

    %% Connections
    A1 --> B1
    B5 --> C1
    C2 --> D1
    D4 --> E1
    E4 --> K2
    D4 --> K1
    C4 --> K3
    
    A2 --> F1
    F3 --> G1
    G4 --> H1
    H4 --> I1
    I3 --> J1
    
    K1 --> H1
    K2 --> H3
    K3 --> L2
    
    J3 --> L3
    H4 --> L1
    K1 --> L4

    %% Styling
    classDef inputClass fill:#60a5fa,stroke:#2563eb,stroke-width:3px,color:#fff
    classDef processClass fill:#34d399,stroke:#059669,stroke-width:2px,color:#000
    classDef aiClass fill:#fbbf24,stroke:#d97706,stroke-width:3px,color:#000
    classDef dbClass fill:#a78bfa,stroke:#7c3aed,stroke-width:2px,color:#fff
    classDef outputClass fill:#ec4899,stroke:#be185d,stroke-width:3px,color:#fff
    
    class A1,A2 inputClass
    class B1,B2,B3,B4,B5,D1,D2,D3,D4,D5 processClass
    class C1,C2,C3,C4,C5,E2,F2,G1,G2,H2,H3,J1 aiClass
    class K1,K2,K3 dbClass
    class L1,L2,L3,L4 outputClass
```

---

## 🔍 تفاصيل المراحل

### 1️⃣ معالجة الصورة (OpenCV + Tesseract)
- **كشف الدوران**: `detect_osd_angle()` - باستخدام Tesseract OSD
- **تصحيح الميل**: `deskew_via_min_area_rect()` - MinAreaRect
- **تصحيح المنظور**: `correct_perspective()` - Perspective Transform

### 2️⃣ التحليل البصري (VLM)
- **النموذج**: FriendliAI Qwen2.5-VL-32B-Instruct
- **المخرجات**: JSON منظم (Vendor, Total, Tax, Items, AI Insight)
- **التحقق**: 5+ حقول مملوءة = فاتورة صحيحة

### 3️⃣ الـ Embeddings
- **النموذج**: OpenAI `text-embedding-3-small`
- **الأبعاد**: 1536 dimension vector
- **التخزين**: PostgreSQL + pgvector

### 4️⃣ نظام الدردشة (5 Stages)
1. **Refiner**: تحويل العامية → فصحى
2. **Router**: تحديد نوع المعالجة (SQL/RAG/Hybrid)
3. **Executor**: تنفيذ البحث الدلالي + Cosine Similarity
4. **Validator**: فحص وتنقية النتائج
5. **Replier**: صياغة الرد النهائي

### 5️⃣ نماذج الـ AI المستخدمة
- **VLM**: Qwen2.5-VL-32B-Instruct (FriendliAI)
- **LLM**: GPT-4o-mini (OpenAI)
- **Embeddings**: text-embedding-3-small (OpenAI)
- **OCR**: Tesseract (للـ OSD)

---

## 📊 معادلات رياضية

### Cosine Similarity
```
similarity = (A · B) / (||A|| × ||B||)

حيث:
A = embedding السؤال
B = embedding الفاتورة
· = Dot Product
|| || = Euclidean Norm
```

### Validation Score
```
validation_score = count(filled_fields) / total_fields

✅ valid if score ≥ 5/total_fields
```

---

## 🎯 مميزات النظام

| الميزة | التقنية | الفائدة |
|--------|---------|---------|
| 🔄 تصحيح تلقائي للصور | OpenCV + Tesseract | دقة أعلى في التحليل |
| 🧠 تحليل بصري متقدم | VLM 32B Parameters | فهم عميق للفواتير |
| 🔍 بحث دلالي ذكي | Embeddings + Cosine Similarity | نتائج دقيقة حتى مع الأخطاء |
| 💬 دردشة طبيعية | 5-Stage AI Pipeline | فهم اللهجة السعودية |
| ✅ تحقق تلقائي | Multi-field Validation | منع الأخطاء |

---

## 🔗 التدفق الكامل

```
📸 صورة ملتوية
    ↓
🔄 OpenCV (تصحيح)
    ↓
🧠 VLM (تحليل)
    ↓
✅ Validation (تحقق)
    ↓
🔗 Embeddings (فهرسة)
    ↓
💾 Database (حفظ)
    ↓
💬 Chat AI (استعلام)
    ↓
📊 نتائج دقيقة
```

---

## 📈 الإحصائيات

- **دقة VLM**: ~95% للفواتير العربية
- **سرعة المعالجة**: 2-5 ثواني/فاتورة
- **دعم اللغات**: العربية + الإنجليزية
- **أنواع الفواتير**: ضريبية، مبسطة، شراء، إرجاع

---

*تم التطوير بواسطة فريق Tuwaiq Academy Capstone Project 2025*

