# 📊 Smart Invoice Analyzer — AI-Powered Invoice Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.118-009688?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=for-the-badge&logo=next.js)
![Supabase](https://img.shields.io/badge/Supabase-Cloud-3ECF8E?style=for-the-badge&logo=supabase)
![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Models-yellow?style=for-the-badge)

**مُـفـــــوْتِــــر — يحفظ، يدير، يحلل، ويختصر وقتك**

*An intelligent system that reads invoices (Arabic & English), extracts structured data, and generates AI-powered insights about spending patterns.*

[🚀 Quick Start](#-installation) • [📖 Documentation](docs/) • [🎯 Features](#️-key-features) • [🧠 AI Models](#-ai-models) • [👥 Team](#-team)

</div>

---

## 🚀 Overview

**Smart Invoice Analyzer** is a full-stack AI system that revolutionizes invoice management by combining:

- 🤖 **Vision-Language Models (VLM)** for automatic data extraction
- 🔎 **Semantic Search (RAG)** using embeddings and pgvector
- 💬 **Intelligent Chat** with hybrid AI (SQL + RAG + Retrieval)
- 📊 **Interactive Dashboard** with real-time analytics
- 🌐 **Multilingual Support** for Arabic and English invoices

**Tech Stack:** FastAPI • Next.js • Supabase • HuggingFace • Meta-Llama • Sentence Transformers

---

## ⚙️ Key Features

| Feature | Description |
|---------|-------------|
| 🧾 **Invoice Extraction** | Automatically reads Arabic & English invoices and returns structured JSON |
| 🧠 **AI Insights** | Generates intelligent insights in Arabic about spending behavior |
| 🗂️ **Category Detection** | Classifies invoices by business type (Cafe ☕, Restaurant 🍽️, Pharmacy 💊, etc.) |
| 📋 **Invoice Type Detection** | Identifies invoice types: Purchase, Warranty, Maintenance, Tax |
| ☁️ **Cloud Storage** | Saves invoice images in Supabase Storage (S3-compatible) |
| 🔍 **Semantic Search (RAG)** | Uses pgvector embeddings for intelligent retrieval |
| 💬 **Chat Interface** | Natural-language Q&A: "كم أنفقت على المطاعم؟" |
| 📊 **Dashboard** | Interactive analytics with filters (category, month, payment) |
| 🎨 **Modern UI** | Fully Arabic (RTL) interface with dark mode support |
| 📥 **PDF Export** | Download invoices as PDF documents |

---

## 🧠 AI Models

| Task | Model | Provider | Description |
|------|-------|----------|-------------|
| **Vision-Language Extraction** | `Hugging Face VLM` | Hugging Face Inference API | Reads invoice images in Arabic & English |
| **Embeddings** | `all-MiniLM-L6-v2` | sentence-transformers | 384D vectors for semantic search |
| **Chat / Reasoning** | `Meta-Llama-3-8B-Instruct` | Hugging Face Router (Novita) | Answers invoice queries & generates SQL |
| **Database** | `PostgreSQL + pgvector` | Supabase | Stores invoices & vector embeddings |
| **Storage** | `S3-compatible bucket` | Supabase Storage | Public invoice image storage |

---

## 🔄 System Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    1. User Uploads Invoice                       │
│                   (Image or Camera Capture)                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              2. Upload to Supabase Storage (Cloud)              │
│                     Returns: Public Image URL                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│           3. VLM Analysis (Hugging Face Inference API)          │
│   • OCR: Read Arabic & English text                            │
│   • Extract: Invoice #, Date, Vendor, Items, Totals            │
│   • Classify: Business Category & Invoice Type                 │
│   • Generate: AI Insight in Arabic                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              4. Save to Supabase PostgreSQL Database            │
│   • invoices table (structured data)                           │
│   • items table (line items)                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│           5. Generate Embedding (Sentence Transformers)         │
│   • Convert invoice data to 384D vector                        │
│   • Store in invoice_embeddings table (pgvector)               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   6. User Interactions                          │
│   📊 Dashboard: View analytics, charts, filters                │
│   💬 Chat: Ask questions (SQL / RAG / Retrieval modes)         │
│   📋 Invoices: Browse, filter, download PDFs                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
capstone-project-invoice-mangement-system/
│
├── 📁 backend/                      # FastAPI Backend
│   ├── main.py                      # Application entry point
│   ├── database.py                  # Supabase connection
│   ├── utils.py                     # Embedding generation
│   ├── 📁 routers/                  # API endpoints
│   │   ├── upload.py                # Upload images to Supabase
│   │   ├── vlm.py                   # VLM invoice analysis
│   │   ├── chat.py                  # AI chat (SQL + RAG + Retrieval)
│   │   ├── dashboard.py             # Analytics endpoints
│   │   ├── invoices.py              # CRUD operations
│   │   └── items.py                 # Line items management
│   ├── 📁 models/                   # Database models (SQLAlchemy)
│   │   ├── invoice_model.py
│   │   ├── item_model.py
│   │   └── embedding_model.py
│   └── 📁 schemas/                  # Pydantic validation
│       ├── invoice_schema.py
│       └── item_schema.py
│
├── 📁 frontend-nextjs/              # Next.js Frontend
│   ├── 📁 app/                      # Pages (App Router)
│   │   ├── layout.tsx               # Root layout with Navbar
│   │   ├── page.tsx                 # Home page
│   │   ├── upload/                  # Invoice upload page
│   │   ├── invoices/                # Invoices list page
│   │   ├── dashboard/               # Analytics dashboard
│   │   └── chat/                    # AI chat page
│   ├── 📁 components/               # React components
│   │   ├── Navbar.tsx
│   │   ├── InvoiceResultCard.tsx
│   │   ├── CameraCapture.tsx
│   │   ├── ImageModal.tsx
│   │   ├── ThemeToggle.tsx
│   │   └── ui/                      # shadcn/ui components
│   └── 📁 lib/                      # Utilities
│       ├── utils.ts
│       └── pdfUtils.ts
│
├── 📁 docs/                         # Professional Documentation
│   ├── backend_overview.md          # Backend architecture (12K words)
│   ├── frontend_overview.md         # Frontend structure (10K words)
│   ├── ai_models_overview.md        # AI models deep dive (8K words)
│   ├── ai_deep_dive_questions.md    # Expert Q&A (8K words)
│   ├── api_reference.md             # API documentation (7K words)
│   └── usage_guide.md               # User manual (6K words)
│
├── 📁 visuals/                      # System diagrams
│   └── final_workflow_diagram.md    # 10 Mermaid diagrams
│
├── 📁 models/                       # AI model notebooks
│   ├── final_model.py
│   └── *.ipynb
│
├── 📄 requirements.txt              # Python dependencies (optimized)
├── 📄 .env.example                  # Environment template
├── 📄 database_setup.sql            # Database schema
├── 📄 run.bat                       # Windows run script
├── 📄 run.sh                        # Mac/Linux run script
└── 📄 README.md                     # This file
```

---

## 🛠️ Installation

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **Supabase account** (free tier: [supabase.com](https://supabase.com))
- **Hugging Face API token** (free: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))

---

### Setup Steps

#### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/AI-AugToOct/capstone-project-invoice-mangement-system.git
cd capstone-project-invoice-mangement-system
```

#### 2️⃣ **Create Virtual Environment**

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

#### 3️⃣ **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

#### 4️⃣ **Configure Environment Variables**

```bash
# Copy template
cp .env.example .env

# Edit .env and add your credentials:
# DATABASE_URL=postgresql://user:pass@host.supabase.co:5432/postgres
# SUPABASE_URL=https://[project].supabase.co
# SUPABASE_KEY=your_anon_key
# HF_TOKEN=your_huggingface_token
```

#### 5️⃣ **Setup Database**

In Supabase SQL Editor, run:
```sql
-- See database_setup.sql for complete schema
CREATE EXTENSION IF NOT EXISTS vector;
-- Create tables: invoices, invoice_embeddings, items
```

Create storage bucket:
1. Go to Supabase → Storage
2. Create bucket named `invoices`
3. Make it public

#### 6️⃣ **Setup Frontend**

```bash
cd frontend-nextjs
npm install

# Create .env.local:
# NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
# NEXT_PUBLIC_SUPABASE_URL=https://[project].supabase.co
# NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

#### 7️⃣ **Run the Application**

**Option A: Use Run Scripts**

```bash
# Windows
run.bat

# Mac/Linux
chmod +x run.sh
./run.sh
```

**Option B: Manual Start**

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload
# → http://127.0.0.1:8000

# Terminal 2 - Frontend
cd frontend-nextjs
npm run dev
# → http://localhost:3000
```

#### 8️⃣ **Verify Installation**

- Frontend: http://localhost:3000
- Backend API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000

---

## 🎯 Usage Flow

### Example: Complete Workflow

Let's walk through analyzing a **Starbucks receipt**:

#### 1. **📤 Upload Invoice**
```
User uploads: starbucks_receipt.jpg
→ Saved to Supabase Storage
→ URL: https://[project].supabase.co/storage/v1/object/public/invoices/starbucks_receipt.jpg
```

#### 2. **🤖 AI Extraction (VLM Analysis)**
```json
{
  "Invoice Number": "INV-2024-1234",
  "Date": "2025-10-07",
  "Vendor": "Starbucks",
  "Branch": "Riyadh Tower",
  "Phone": "0112345678",
  "Items": [
    {"description": "Caramel Frappuccino", "quantity": 2, "unit_price": 22.00, "total": 44.00},
    {"description": "Croissant", "quantity": 1, "unit_price": 15.00, "total": 15.00}
  ],
  "Subtotal": "59.00",
  "Tax": "8.85",
  "Total Amount": "67.85",
  "Payment Method": "Visa",
  "Category": "Cafe",
  "Invoice_Type": "فاتورة شراء",
  "Keywords_Detected": ["Purchase", "شراء", "Receipt"],
  "AI_Insight": "هذا الشراء من مقهى ستاربكس في برج الرياض. العميل طلب مشروبين ووجبة خفيفة بمبلغ معتدل. المشتريات المتكررة من المقاهي قد تشير إلى عادة يومية."
}
```

#### 3. **💾 Data Storage**
```sql
-- invoices table
INSERT INTO invoices (vendor, total_amount, category, invoice_type, ...)
VALUES ('Starbucks', '67.85', '{"ar": "مقهى", "en": "Cafe"}', 'فاتورة شراء', ...);

-- items table
INSERT INTO items (invoice_id, description, quantity, unit_price, total)
VALUES (42, 'Caramel Frappuccino', 2, 22.00, 44.00);
```

#### 4. **🔎 Embeddings Generated**
```python
# Text representation:
"Invoice Number: INV-2024-1234 | Vendor: Starbucks | Items: Caramel Frappuccino (qty: 2), Croissant (qty: 1) | Total: 67.85 | Category: Cafe"

# Converted to 384D vector:
[0.123, -0.456, 0.789, ..., 0.234]  # 384 dimensions

# Stored in invoice_embeddings table
```

#### 5. **💬 Chat with AI**
```
User: "كم أنفقت على ستاربكس؟"

AI Mode: SQL (detects aggregation keyword "كم")
SQL: SELECT SUM(CAST(total_amount AS FLOAT)) FROM invoices WHERE vendor LIKE '%Starbucks%'
Result: 245.50

Response: "أنفقت 245.50 ر.س على ستاربكس"
```

```
User: "أرسل لي فواتير ستاربكس"

AI Mode: Retrieval (detects vendor name)
Query: SELECT * FROM invoices WHERE vendor ILIKE '%Starbucks%' LIMIT 5

Response: [Shows 5 invoice cards with images, dates, amounts]
```

#### 6. **📊 Dashboard View**
```
Total Invoices: 156
Total Spending: 12,456.75 ر.س
Average: 79.85 ر.س

Top Vendors:
1. Starbucks - 23 invoices (245.50 ر.س)
2. Dunkin - 18 invoices (189.00 ر.س)
3. Panda - 15 invoices (567.25 ر.س)

Category Distribution (Pie Chart):
- Cafes: 35% (4,359.86 ر.س)
- Restaurants: 40% (4,982.70 ر.س)
- Pharmacies: 15% (1,868.51 ر.س)
- Other: 10% (1,245.68 ر.س)
```

#### 7. **📋 Invoice Management**
- Browse all 156 invoices with thumbnail images
- Filter: Show only "مقهى" → 54 invoices
- Click Starbucks invoice → Full-screen image view
- Download as PDF → `Starbucks_INV-2024-1234.pdf`

---

## 📊 Dashboard Features

### Interactive Analytics

- **📈 Real-time Stats**: Total invoices, spending, averages
- **🥧 Category Pie Chart**: Spending distribution by business type
- **📉 Monthly Area Chart**: Trend analysis over time
- **📊 Payment Bar Chart**: Cash vs Card vs Mobile
- **🔄 Day Radar Chart**: Spending patterns by weekday
- **🏪 Top Vendors**: Most frequent merchants

### Smart Filters

- **Category**: مطعم, مقهى, صيدلية, etc.
- **Month**: يناير, فبراير, مارس, etc.
- **Payment Method**: Cash, Visa, Mada, etc.

All filters update **instantly** - no page reload!

---

## 💬 Chat AI Features

### Hybrid Intelligence (3 Modes)

| Mode | Trigger | Example | Speed |
|------|---------|---------|-------|
| **🧮 SQL Mode** | Aggregation keywords (كم، مجموع) | "كم أنفقت على المطاعم؟" | ⚡ <1s |
| **📄 RAG Mode** | General questions | "ما هي آخر مشترياتي؟" | 🐢 ~3s |
| **🖼️ Retrieval Mode** | Vendor names | "أرسل لي فواتير دانكن" | ⚡ <1s |

### Example Questions

- "كم عدد الفواتير هذا الشهر؟" (How many invoices this month?)
- "ما هو متوسط الفاتورة؟" (What's the average invoice amount?)
- "أرني فواتير ستاربكس" (Show me Starbucks invoices)
- "كم أنفقت في سبتمبر؟" (How much did I spend in September?)

---

## 🔮 Future Enhancements

- [ ] 🧠 Fine-tune VLM on custom invoice dataset for better accuracy
- [ ] 🎨 Enhanced UI with better animations and interactions
- [ ] 💬 Conversation memory for follow-up questions
- [ ] 🔧 Bulk invoice upload (process multiple at once)
- [ ] 📱 Mobile app (iOS & Android)
- [ ] 🌍 Multi-currency support
- [ ] 👥 Multi-user accounts with authentication
- [ ] 📧 Email receipt scanning integration
- [ ] 🔔 Budget alerts and spending limits
- [ ] 📤 Export data as CSV/Excel

---

## 📖 Documentation

Comprehensive documentation (47,000+ words) is available in the `/docs` folder:

| Document | Description | Words |
|----------|-------------|-------|
| [Backend Overview](docs/backend_overview.md) | FastAPI architecture, API routes, database schema | 12,000 |
| [Frontend Overview](docs/frontend_overview.md) | Next.js pages, components, state management | 10,000 |
| [AI Models Overview](docs/ai_models_overview.md) | VLM, LLM, embeddings, RAG pipeline | 8,000 |
| [AI Deep Dive Q&A](docs/ai_deep_dive_questions.md) | 15 expert-level questions & answers | 8,000 |
| [API Reference](docs/api_reference.md) | All endpoints with cURL/Postman examples | 7,000 |
| [Usage Guide](docs/usage_guide.md) | Step-by-step user manual | 6,000 |
| [Visual Diagrams](visuals/final_workflow_diagram.md) | 10 system architecture diagrams | - |

---

---

## 👥 Team

- **Maryam**
- **Lames**
- **Ruwaa**
- **Saif Alotibie**

---

## 🙏 Acknowledgments

- **Hugging Face** - VLM and LLM inference APIs
- **Supabase** - Database and storage infrastructure
- **Vercel** - Next.js framework and deployment
- **shadcn/ui** - Beautiful React components
- **Cairo Font** - Arabic typography
- **Meta AI** - Llama-3 language model
- **Sentence Transformers** - Embedding models

---

<div align="center">

## 🎉 Project Status: Production Ready! 🚀

**مُـفـــــوْتِــــر — يحفظ، يدير، يحلل، ويختصر وقتك**

*Built with ❤️ using FastAPI, Next.js, and AI*

**Cross-Platform** • **Multilingual** • **Production Ready**

[⬆ Back to Top](#-smart-invoice-analyzer--ai-powered-invoice-management-system)

</div>
