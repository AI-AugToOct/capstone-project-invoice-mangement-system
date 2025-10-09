# 🧾 مُـــفـــــوْتِــــر - Smart Invoice Analyzer

<div align="center">

![مُـــفـــــوْتِــــر](https://img.shields.io/badge/مُـــفـــــوْتِــــر-Smart%20Invoice%20Analyzer-8dbcc7?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**نظام ذكي عربي متكامل لإدارة وتحليل الفواتير بالذكاء الاصطناعي**

[🌐 Live Demo](https://capstone-project-invoice-mangement-system-poa4ldjjv.vercel.app) | [📖 Documentation](#-المميزات) | [🚀 Quick Start](#-التشغيل-السريع)

</div>

---

## 📋 **جدول المحتويات**

- [نظرة عامة](#-نظرة-عامة)
- [المميزات](#-المميزات)
- [التقنيات المستخدمة](#-التقنيات-المستخدمة)
- [البنية المعمارية](#-البنية-المعمارية)
- [التشغيل السريع](#-التشغيل-السريع)
- [Deployment](#-deployment)
- [API Documentation](#-api-endpoints)
- [المساهمة](#-المساهمة)
- [الترخيص](#-الترخيص)

---

## 🎯 **نظرة عامة**

**مُـــفـــــوْتِــــر** هو نظام متكامل يجمع بين قوة الذكاء الاصطناعي وسهولة الاستخدام لإدارة فواتيرك بطريقة ذكية وفعالة. يدعم النظام اللغة العربية بشكل كامل مع واجهة مستخدم حديثة ومتجاوبة.

### ✨ **ماذا يفعل؟**

```mermaid
graph LR
    A[📸 رفع الفاتورة] --> B[🤖 تحليل بالذكاء الاصطناعي]
    B --> C[📊 استخراج البيانات]
    C --> D[💾 حفظ تلقائي]
    D --> E[📈 تحليلات و رؤى]
    E --> F[💬 مساعد ذكي]
```

---

## 🚀 **المميزات**

### 📤 **رفع وتحليل ذكي**
- ✅ رفع صور أو ملفات PDF
- ✅ التقاط مباشر بالكاميرا (موبايل)
- ✅ تحليل فوري باستخدام Vision Language Model
- ✅ استخراج تلقائي للبيانات (اسم المورد، التاريخ، الإجمالي، الضريبة)
- ✅ تحويل PDF إلى صور تلقائياً

### 📊 **لوحة تحكم تفاعلية**
- 📈 إحصائيات شاملة (إجمالي الفواتير، المصروفات، الضرائب)
- 📉 رسوم بيانية تفاعلية (Recharts)
- 🗂️ تصنيف حسب الفئات وطرق الدفع
- 📅 فلترة حسب التاريخ والشهر
- 🎨 Dark Mode / Light Mode

### 💬 **مساعد ذكي عربي**
- 🤖 محادثة بالعربية باستخدام Friendli AI
- 🔍 استعلامات ذكية عن الفواتير
- 📋 إجابات فورية مع بيانات دقيقة
- 🧠 RAG (Retrieval Augmented Generation) مع PostgreSQL + pgvector

### 🗃️ **إدارة متقدمة**
- 📋 عرض جميع الفواتير في جدول قابل للبحث
- 🔎 بحث متقدم وفلترة
- 📥 تصدير كـ PDF
- 🗑️ حذف آمن
- 🖼️ عرض الصور الأصلية

### 🌐 **واجهة مستخدم حديثة**
- 🎨 تصميم عربي أنيق مع Tailwind CSS
- 📱 Responsive 100% (Desktop, Tablet, Mobile)
- 🌓 Dark/Light Mode
- ⚡ Animations سلسة مع Framer Motion
- ♿ Accessible (WCAG AA)

---

## 🛠️ **التقنيات المستخدمة**

### **Frontend** (Next.js 14)

```
📦 Frontend Stack
├── ⚛️  Next.js 14.2.33 (App Router)
├── 🎨 Tailwind CSS 3.4.1
├── 🧩 shadcn/ui (Radix UI)
├── ✨ Framer Motion 11.5.6
├── 📊 Recharts 2.12.7
├── 🖼️  next/image (Optimized)
└── 🌐 TypeScript 5
```

### **Backend** (FastAPI)

```
🔧 Backend Stack
├── ⚡ FastAPI 0.115.0
├── 🔄 Uvicorn 0.32.0 (ASGI Server)
├── 🗄️  PostgreSQL + Supabase
├── 🧠 pgvector (Vector DB للـ RAG)
├── 📊 SQLAlchemy 2.0.36 (ORM)
├── 🔐 Psycopg2 (PostgreSQL Adapter)
└── 🐍 Python 3.12
```

### **AI & ML**

```
🤖 AI Stack
├── 🎯 Friendli AI (Vision + Chat)
├── 🧠 OpenAI GPT-4 Vision (Alternative)
├── 📝 OpenAI Embeddings (text-embedding-3-small)
├── 🖼️  PyMuPDF 1.24.14 (PDF Processing)
└── 📊 NumPy 2.1.3
```

### **Infrastructure**

```
☁️  Cloud & DevOps
├── 🚂 Railway (Backend Hosting)
├── ▲  Vercel (Frontend Hosting)
├── 🗄️  Supabase (Database + Storage)
├── 🐳 Docker + Docker Compose
└── 📦 GitHub Actions (CI/CD)
```

---

## 🏗️ **البنية المعمارية**

### **System Architecture**

```mermaid
graph TB
    subgraph "Frontend - Next.js"
        A[React Components]
        B[Tailwind UI]
        C[API Client]
    end
    
    subgraph "Backend - FastAPI"
        D[REST API]
        E[Business Logic]
        F[Database ORM]
    end
    
    subgraph "AI Services"
        G[Friendli AI]
        H[OpenAI]
        I[pgvector RAG]
    end
    
    subgraph "Data Layer"
        J[(PostgreSQL)]
        K[Supabase Storage]
    end
    
    A --> C
    C --> D
    D --> E
    E --> F
    E --> G
    E --> H
    E --> I
    F --> J
    D --> K
    I --> J
```

### **API Flow**

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AI
    participant DB
    
    User->>Frontend: رفع فاتورة
    Frontend->>Backend: POST /upload
    Backend->>Supabase: حفظ الصورة
    Backend->>AI: تحليل VLM
    AI-->>Backend: استخراج البيانات
    Backend->>DB: حفظ في PostgreSQL
    Backend-->>Frontend: إرجاع النتيجة
    Frontend-->>User: عرض البيانات
```

---

## 🚀 **التشغيل السريع**

### **المتطلبات الأساسية**

- 🐍 Python 3.12+
- 📦 Node.js 18+
- 🐳 Docker (اختياري)

### **1️⃣ Clone المشروع**

```bash
git clone https://github.com/AI-AugToOct/capstone-project-invoice-mangement-system.git
cd capstone-project-invoice-mangement-system
```

### **2️⃣ إعداد البيئة**

#### **Backend:**

```bash
# إنشاء Virtual Environment
python -m venv venv

# التفعيل (Windows)
venv\Scripts\activate

# التفعيل (Linux/Mac)
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt
```

#### **Frontend:**

```bash
cd frontend-nextjs
npm install
```

### **3️⃣ إعداد Environment Variables**

#### **Backend (`.env`):**

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_BUCKET=invoices

# Database
DATABASE_URL=postgresql://user:password@host:5432/db

# OpenAI
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small

# Friendli AI
FRIENDLI_TOKEN=flp_...
FRIENDLI_URL=https://api.friendli.ai/dedicated/v1/chat/completions
FRIENDLI_MODEL_ID=your_model_id

# App
ENVIRONMENT=development
PORT=8000
```

#### **Frontend (`frontend-nextjs/.env.local`):**

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

### **4️⃣ تشغيل المشروع**

#### **Windows:**
```bash
.\run.bat
```

#### **Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

#### **Docker:**
```bash
docker-compose up --build
```

### **5️⃣ فتح التطبيق**

- 🌐 **Frontend:** http://localhost:3000
- ⚡ **Backend API:** http://localhost:8000
- 📚 **API Docs:** http://localhost:8000/docs

---

## ☁️ **Deployment**

### **Backend → Railway**

1. **إنشاء مشروع جديد على Railway**
2. **ربط GitHub Repository**
3. **إضافة Environment Variables**
4. **Deploy تلقائي!**

**Railway Config (`railway.json`):**
```json
{
  "build": {
    "builder": "dockerfile",
    "dockerfilePath": "Dockerfile.backend"
  }
}
```

### **Frontend → Vercel**

1. **Import من GitHub**
2. **Root Directory:** `frontend-nextjs`
3. **Framework Preset:** Next.js
4. **إضافة Environment Variables**
5. **Deploy!**

**Vercel Config:**
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

---

## 📡 **API Endpoints**

### **Upload**
```http
POST /upload/
Content-Type: multipart/form-data

Response: {
  "url": "https://storage.supabase.co/...",
  "converted_from_pdf": false
}
```

### **VLM Analysis**
```http
POST /vlm/analyze
Content-Type: application/json

{
  "image_url": "https://..."
}

Response: {
  "vendor": "متجر الإلكترونيات",
  "invoice_number": "INV-2024-001",
  "invoice_date": "2024-03-15",
  "total_amount": "1250.00",
  "tax": "187.50",
  "payment_method": "بطاقة ائتمان",
  "category": "إلكترونيات"
}
```

### **Chat**
```http
POST /chat/ask
Content-Type: application/json

{
  "question": "كم إجمالي مصروفاتي هذا الشهر؟"
}

Response: {
  "reply": "إجمالي مصروفاتك لهذا الشهر هو 4,250 ريال سعودي.",
  "invoices": [...]
}
```

### **Dashboard**
```http
GET /dashboard/stats

Response: {
  "total_invoices": 45,
  "total_spent": "15420.50",
  "total_tax": "2313.08",
  "this_month_spent": "4250.00",
  "by_category": {...},
  "by_month": {...}
}
```

### **Invoices**
```http
GET /invoices/all
GET /invoices/{id}
DELETE /invoices/{id}
```

---

## 📁 **هيكل المشروع**

```
capstone-project-invoice-mangement-system/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Entry Point
│   ├── database.py            # DB Configuration
│   ├── models/                # SQLAlchemy Models
│   ├── routers/               # API Routes
│   ├── schemas/               # Pydantic Schemas
│   └── requirements.txt       # Python Dependencies
│
├── frontend-nextjs/           # Next.js Frontend
│   ├── app/                   # App Router
│   │   ├── page.tsx          # Home Page
│   │   ├── upload/           # Upload Page
│   │   ├── dashboard/        # Dashboard
│   │   ├── invoices/         # Invoices List
│   │   └── chat/             # Chat Assistant
│   ├── components/           # React Components
│   ├── lib/                  # Utilities
│   └── public/               # Static Assets
│
├── Dockerfile.backend        # Backend Docker
├── Dockerfile.frontend       # Frontend Docker
├── docker-compose.yml        # Multi-container Setup
├── railway.json             # Railway Config
└── README.md               # This file
```

---

## 🤝 **المساهمة**

المساهمات مرحب بها دائماً! إذا كنت تريد المساهمة:

1. Fork المشروع
2. أنشئ Branch جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى Branch (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

---

## 🐛 **مشاكل معروفة**

- ⚠️ Friendli AI قد يحتاج إلى deployment نشط
- 📱 Safari على iOS: بعض الـ CSS animations قد تكون بطيئة
- 🔄 Real-time updates: ستتم إضافتها قريباً

---

## 📈 **خارطة الطريق**

- [ ] إضافة Real-time notifications
- [ ] دعم Excel Export
- [ ] Mobile App (React Native)
- [ ] تقارير شهرية تلقائية
- [ ] تكامل مع أنظمة محاسبية
- [ ] OCR محسّن للغة العربية

---

## 📄 **الترخيص**

هذا المشروع مرخص تحت **MIT License** - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👨‍💻 **الفريق**

<div align="center">

**تم التطوير بواسطة فريق AI-AugToOct**

[![GitHub](https://img.shields.io/badge/GitHub-AI--AugToOct-181717?style=for-the-badge&logo=github)](https://github.com/AI-AugToOct)

</div>

---

## 📞 **التواصل**

- 📧 **Email:** support@mufawter.com
- 🌐 **Website:** [mufawter.com](https://capstone-project-invoice-mangement-system-poa4ldjjv.vercel.app)
- 💬 **Issues:** [GitHub Issues](https://github.com/AI-AugToOct/capstone-project-invoice-mangement-system/issues)

---

<div align="center">

**⭐ إذا أعجبك المشروع، لا تنسى إعطاءه نجمة! ⭐**

Made with ❤️ in Saudi Arabia 🇸🇦

</div>
