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

### Step-by-Step Workflow

1. **📤 Upload Invoice**
   - Drag-and-drop image or capture from camera
   - Image saved to Supabase Storage
   - Returns public URL

2. **🤖 AI Extraction**
   - VLM analyzes image (Arabic + English)
   - Extracts: Invoice #, Date, Vendor, Items, Totals
   - Classifies: Category & Invoice Type
   - Generates: AI Insight in Arabic

3. **💾 Data Storage**
   - Structured data → `invoices` table
   - Line items → `items` table
   - Results displayed in elegant cards

4. **🔎 Embeddings**
   - Convert invoice text to 384D vector
   - Store in `invoice_embeddings` (pgvector)
   - Enable semantic search

5. **💬 Chat Interface**
   - Ask: "كم أنفقت على المطاعم؟" (How much did I spend on restaurants?)
   - AI uses SQL, RAG, or Retrieval mode
   - Returns answer + relevant invoices

6. **📊 Dashboard**
   - View analytics: total spending, top vendors
   - Interactive charts: Pie, Area, Bar, Radar
   - Filter by category, month, payment method
   - Smart insights in Arabic

7. **📋 Manage Invoices**
   - Browse all invoices with images
   - Filter by category or type
   - Download as PDF
   - View full-screen image modal

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

- [ ] 🧠 Fine-tune VLM on custom invoice dataset (+5-7% accuracy)
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

## 🎨 Screenshots

<table>
<tr>
<td width="33%" align="center">
<img src="screenshots/home.png" alt="Home Page" width="100%" />
<b>🏠 Home Page</b><br/>
<i>Modern landing with Arabic UI</i>
</td>
<td width="33%" align="center">
<img src="screenshots/upload.png" alt="Upload" width="100%" />
<b>📤 Upload & Analysis</b><br/>
<i>AI extracts data automatically</i>
</td>
<td width="33%" align="center">
<img src="screenshots/dashboard.png" alt="Dashboard" width="100%" />
<b>📊 Dashboard</b><br/>
<i>Interactive charts & filters</i>
</td>
</tr>
<tr>
<td width="33%" align="center">
<img src="screenshots/invoices.png" alt="Invoices" width="100%" />
<b>📋 Invoices List</b><br/>
<i>Browse with images & filters</i>
</td>
<td width="33%" align="center">
<img src="screenshots/chat.png" alt="Chat" width="100%" />
<b>💬 AI Chat</b><br/>
<i>Natural language Q&A</i>
</td>
<td width="33%" align="center">
<img src="screenshots/dark-mode.png" alt="Dark Mode" width="100%" />
<b>🌙 Dark Mode</b><br/>
<i>Eye-friendly theme</i>
</td>
</tr>
</table>

*Note: Screenshots will be added in future release*

---

## 🔐 Security & Privacy

- ✅ **Environment Variables**: Sensitive keys stored in `.env` (never committed)
- ✅ **Encrypted Connections**: HTTPS/SSL for all API calls
- ✅ **Cloud Storage**: Images stored in your Supabase (you control access)
- ✅ **Row Level Security**: Supabase RLS for multi-user (future)
- ✅ **API Key Rotation**: Rotate keys if exposed

---

## 📈 Performance Metrics

| Operation | Current Performance | Target |
|-----------|---------------------|--------|
| **VLM Analysis** | 3-5 seconds | 2-3 seconds (with caching) |
| **Chat Response (SQL)** | <1 second | <0.5 seconds |
| **Chat Response (RAG)** | 3-4 seconds | 1-2 seconds (better indexing) |
| **Dashboard Load** | <1 second (100 invoices) | <0.3 seconds (caching) |
| **Embedding Generation** | ~100ms per invoice | ~50ms (batch processing) |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

### Coding Standards

- **Backend**: PEP 8 (Python)
- **Frontend**: ESLint + Prettier (TypeScript)
- **Commits**: Conventional Commits format
- **Documentation**: Update docs for new features

---

## 👥 Team

<table>
<tr>
<td align="center">
<img src="https://github.com/maryam.png" width="100px;" alt="Maryam"/><br />
<sub><b>Maryam</b></sub><br />
<i>Backend & AI Integration</i>
</td>
<td align="center">
<img src="https://github.com/lames.png" width="100px;" alt="Lames"/><br />
<sub><b>Lames</b></sub><br />
<i>Frontend Development</i>
</td>
<td align="center">
<img src="https://github.com/ruwaa.png" width="100px;" alt="Ruwaa"/><br />
<sub><b>Ruwaa</b></sub><br />
<i>Database & Architecture</i>
</td>
<td align="center">
<img src="https://github.com/saifalotibie.png" width="100px;" alt="Saif Alotibie"/><br />
<sub><b>Saif Alotibie</b></sub><br />
<i>AI Models & Research</i>
</td>
</tr>
</table>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

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

## 📞 Support & Contact

- **📧 Email**: contact@yourdomain.com
- **🐛 Issues**: [GitHub Issues](https://github.com/AI-AugToOct/capstone-project-invoice-mangement-system/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/AI-AugToOct/capstone-project-invoice-mangement-system/discussions)
- **📖 Documentation**: [/docs folder](docs/)
- **🌐 Live Demo**: Coming soon!

---

## 🌟 Star History

If you find this project helpful, please give it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=AI-AugToOct/capstone-project-invoice-mangement-system&type=Date)](https://star-history.com/#AI-AugToOct/capstone-project-invoice-mangement-system&Date)

---

<div align="center">

## 🎉 Project Status: Production Ready! 🚀

**مُـفـــــوْتِــــر — يحفظ، يدير، يحلل، ويختصر وقتك**

*Built with ❤️ using FastAPI, Next.js, and AI*

**Cross-Platform** • **Multilingual** • **Open Source**

[⬆ Back to Top](#-smart-invoice-analyzer--ai-powered-invoice-management-system)

</div>
