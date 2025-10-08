# مُفَوْتِر - Mufawter
### Smart Invoice Management System | نظام ذكي لإدارة الفواتير

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green)

---

## 🎯 Overview | نظرة عامة

**Mufawter** is an AI-powered invoice management system that automatically extracts, analyzes, and stores invoice data from images or PDFs. The system features a smart Arabic chatbot that can answer natural language queries about your invoices using advanced Text-to-SQL and semantic search capabilities.

**مُفَوْتِر** هو نظام ذكي لإدارة الفواتير يستخدم الذكاء الاصطناعي لاستخراج وتحليل وتخزين بيانات الفواتير من الصور أو ملفات PDF تلقائياً. يتميز النظام بمساعد ذكي يتحدث العربية ويمكنه الإجابة على أسئلتك عن فواتيرك باستخدام تقنيات Text-to-SQL والبحث الدلالي المتقدمة.

---

## ✨ Features | المميزات

### 🤖 AI-Powered Invoice Extraction
- Vision Language Model (Qwen2.5-VL-32B) for automatic data extraction
- Supports images and PDFs
- Extracts vendor, amounts, dates, items, tax, and payment method

### 💬 Intelligent Arabic Chatbot
- Natural language queries in Arabic
- Dynamic Text-to-SQL generation
- Semantic search using OpenAI embeddings
- Context-aware responses

### 📊 Interactive Dashboard
- Real-time spending analytics
- Category breakdown
- Monthly trends
- Top vendors analysis

### 🔍 Advanced Search
- SQL-based precision search
- Semantic similarity search
- Hybrid search combining both methods

### 📱 Modern UI
- Responsive design for all devices
- Dark/Light theme support
- RTL (Arabic) layout
- Beautiful SVG illustrations

---

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL + pgvector** - Database with vector search
- **OpenAI GPT-4o-mini** - LLM for chat and SQL generation
- **OpenAI Embeddings** - Semantic search
- **Friendli AI (Qwen2.5-VL)** - Vision model for invoice extraction

### Infrastructure
- **Supabase** - PostgreSQL hosting & storage
- **Vercel** - Frontend hosting (recommended)
- **Railway** - Backend hosting (recommended)

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install Node.js 18+ and Python 3.12+
node --version  # v18.0.0+
python --version  # Python 3.12+
```

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd capstone-project-invoice-mangement-system
```

### 2. Setup Backend
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create .env file in root
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_BUCKET=invoices
DATABASE_URL=your_postgres_connection_string
OPENAI_API_KEY=your_openai_api_key
FRIENDLI_TOKEN=your_friendli_token
FRIENDLI_URL=https://api.friendli.ai/dedicated/v1/chat/completions
FRIENDLI_MODEL_ID=your_model_id
EMBEDDING_MODEL=text-embedding-3-small
```

### 3. Setup Database
```bash
# Run SQL setup script in your Supabase SQL Editor
# File: database_setup.sql
```

### 4. Setup Frontend
```bash
cd frontend-nextjs
npm install

# Create .env.local
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 5. Run Project
```bash
# From project root
./run.bat  # Windows
# or
./run.sh   # Linux/Mac
```

The backend will start on `http://127.0.0.1:8000`  
The frontend will open automatically on `http://localhost:3000`

---

## 📁 Project Structure

```
capstone-project-invoice-mangement-system/
├── backend/
│   ├── routers/
│   │   ├── chat.py          # Intelligent chatbot endpoint
│   │   ├── vlm.py           # Vision model for invoice extraction
│   │   ├── upload.py        # File upload handler
│   │   ├── invoices.py      # Invoice CRUD operations
│   │   └── dashboard.py     # Analytics endpoints
│   ├── models/
│   │   ├── invoice_model.py
│   │   ├── item_model.py
│   │   └── embedding_model.py
│   ├── schemas/
│   ├── database.py
│   ├── utils.py
│   └── main.py
├── frontend-nextjs/
│   ├── app/
│   │   ├── page.tsx         # Home page
│   │   ├── upload/          # Upload interface
│   │   ├── invoices/        # Invoice list
│   │   ├── dashboard/       # Analytics
│   │   └── chat/            # Chatbot interface
│   ├── components/
│   └── lib/
├── database_setup.sql
├── requirements.txt
├── run.bat
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is part of a capstone project for educational purposes.

---

## 👨‍💻 Developer

Developed as a capstone project demonstrating AI integration in financial document management.

---

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [Supabase Documentation](https://supabase.com/docs)

---

Made with ❤️ using AI and modern web technologies
