# Backend Architecture Overview

## 🏗️ System Architecture

The **Smart Invoice Analyzer** backend is built using **FastAPI**, a modern Python web framework, integrated with **Supabase** (PostgreSQL + Storage) and AI models from **Hugging Face** and **FriendliAI**.

### Technology Stack

- **Framework**: FastAPI 0.118.0
- **Database**: PostgreSQL (via Supabase) with pgvector extension
- **ORM**: SQLAlchemy 2.0.43
- **Storage**: Supabase Storage (S3-compatible bucket)
- **AI Models**: 
  - Vision-Language Model (VLM) via Hugging Face Inference API
  - LLM: Meta-Llama-3-8B-Instruct (via Novita/Hugging Face Router)
  - Embeddings: sentence-transformers/all-MiniLM-L6-v2
- **Authentication**: Environment-based API keys

---

## 📂 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py             # Database connection and session management
├── utils.py                # Utility functions (embedding generation)
├── models/                 # SQLAlchemy ORM models
│   ├── invoice_model.py    # Invoice table schema
│   ├── embedding_model.py  # Vector embeddings table
│   └── item_model.py       # Line items table
├── routers/                # API route handlers
│   ├── upload.py           # File upload to Supabase Storage
│   ├── vlm.py              # Invoice analysis using VLM
│   ├── chat.py             # AI chat with hybrid intelligence
│   ├── dashboard.py        # Statistics and analytics
│   └── invoices.py         # Invoice CRUD operations
└── schemas/                # Pydantic validation schemas
    ├── invoice_schema.py
    └── item_schema.py
```

---

## 🗄️ Database Schema

### Tables

#### 1. **invoices**
Primary table storing analyzed invoice data.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `record` | INTEGER | Sequential record number |
| `invoice_number` | STRING | Invoice identifier from document |
| `invoice_date` | DATETIME | Date of invoice |
| `vendor` | STRING | Store/merchant name |
| `tax_number` | STRING | Tax registration number |
| `cashier` | STRING | Cashier name |
| `branch` | STRING | Branch location |
| `phone` | STRING | Contact phone |
| `subtotal` | STRING | Amount before tax |
| `tax` | STRING | Tax amount |
| `total_amount` | STRING | Total including tax |
| `grand_total` | STRING | Final amount |
| `discounts` | STRING | Discount amount |
| `payment_method` | STRING | Payment type (Cash/Card/etc) |
| `amount_paid` | STRING | Amount paid |
| `ticket_number` | STRING | Transaction ticket number |
| `category` | STRING | Business category (JSON: {ar, en}) |
| `ai_insight` | STRING | AI-generated Arabic insight |
| `invoice_type` | STRING | Invoice type in Arabic (فاتورة شراء, etc) |
| `image_url` | STRING | Supabase Storage URL |
| `created_at` | DATETIME | Timestamp |

#### 2. **invoice_embeddings**
Vector embeddings for semantic search (RAG).

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `invoice_id` | INTEGER | Foreign key to invoices |
| `embedding` | VECTOR(384) | 384-dimensional vector |

#### 3. **items**
Line items from invoices.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `invoice_id` | INTEGER | Foreign key to invoices |
| `description` | STRING | Item description |
| `quantity` | FLOAT | Quantity |
| `unit_price` | FLOAT | Price per unit |
| `total` | FLOAT | Line total |

---

## 🔌 API Routes

### 1. Upload Endpoint (`/upload`)

**Route**: `POST /upload/`

**Purpose**: Upload invoice image to Supabase Storage.

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/upload/ \
  -F "file=@invoice.jpg"
```

**Response**:
```json
{
  "url": "https://[project].supabase.co/storage/v1/object/public/invoices/invoice.jpg"
}
```

**Process**:
1. Receives uploaded file
2. Stores in Supabase bucket `invoices`
3. Generates public URL
4. Returns URL for frontend

---

### 2. VLM Analysis Endpoint (`/vlm`)

**Route**: `POST /vlm/analyze`

**Purpose**: Analyze invoice image using Vision-Language Model.

**Request**:
```json
{
  "image_url": "https://[...]/invoice.jpg",
  "prompt": "Optional custom prompt"
}
```

**Response**:
```json
{
  "status": "success",
  "invoice_id": 42,
  "output": {
    "Invoice Number": "INV-12345",
    "Date": "2025-10-07",
    "Vendor": "Coffee Shop",
    "Total Amount": "25.50",
    "Category": "Cafe",
    "Keywords_Detected": ["Purchase", "شراء"],
    "Invoice_Type": "فاتورة شراء",
    "AI_Insight": "هذا الشراء من مقهى..."
  },
  "category": {"ar": "مقهى", "en": "Cafe"},
  "ai_insight": "هذا الشراء من مقهى...",
  "invoice_type": "فاتورة شراء",
  "image_url": "https://[...]/invoice.jpg"
}
```

**Process Flow**:
1. Receives image URL and optional prompt
2. Calls Hugging Face VLM API with structured prompt
3. Parses JSON response from model
4. Extracts fields: invoice number, vendor, date, items, totals, category, type, keywords
5. Generates AI insight in Arabic
6. Saves invoice to database
7. Generates embedding for RAG
8. Returns structured data to frontend

**AI Prompt Structure**:
- Multilingual support (Arabic + English)
- JSON schema enforcement
- Keyword detection for invoice type classification
- Business category detection
- Smart insight generation

---

### 3. Chat Endpoint (`/chat`)

**Route**: `POST /chat/ask`

**Purpose**: Answer natural language questions about invoices using hybrid AI.

**Request**:
```json
{
  "question": "كم أنفقت على المطاعم؟",
  "top_k": 3
}
```

**Response**:
```json
{
  "answer": "أنفقت إجمالي 345.50 ر.س على المطاعم",
  "mode": "sql",
  "invoices": [
    {
      "vendor": "مطعم الذوق",
      "total": "125.00",
      "date": "2025-10-05",
      "image_url": "https://[...]/invoice_5.jpg",
      "invoice_type": "فاتورة شراء"
    }
  ]
}
```

**Hybrid Intelligence Modes**:

#### **Mode 1: SQL (Aggregation)**
- Triggered by: كم، مجموع، إجمالي، count, total, sum
- Process:
  1. Converts question to SQL using LLM
  2. Executes query on database
  3. Formats results in Arabic
  
#### **Mode 2: RAG (Semantic Search)**
- Triggered by: General questions about invoice content
- Process:
  1. Generates question embedding
  2. Performs cosine similarity search in pgvector
  3. Retrieves top-k relevant invoices
  4. Uses LLM to generate contextual answer

#### **Mode 3: Retrieval (Direct Search)**
- Triggered by: Vendor names or invoice types
- Process:
  1. Extracts keywords (vendor/type)
  2. Performs database ILIKE search
  3. Returns matching invoices with images
  4. Formats response with invoice cards

---

### 4. Dashboard Endpoint (`/dashboard`)

**Route**: `GET /dashboard/stats`

**Purpose**: Aggregate statistics for dashboard visualization.

**Response**:
```json
{
  "total_invoices": 156,
  "total_spent": 12456.75,
  "top_vendors": [
    {"vendor": "Starbucks", "count": 23},
    {"vendor": "Dunkin", "count": 18}
  ]
}
```

**Calculations**:
- Total invoices: `COUNT(*)`
- Total spent: `SUM(CAST(total_amount AS FLOAT))`
- Top vendors: `GROUP BY vendor ORDER BY COUNT DESC LIMIT 5`

---

### 5. Invoices Endpoint (`/invoices`)

**Route**: `GET /invoices/all`

**Purpose**: Retrieve all invoices with metadata.

**Response**:
```json
[
  {
    "id": 1,
    "vendor": "Coffee Shop",
    "invoice_number": "INV-001",
    "total_amount": "25.50",
    "invoice_date": "2025-10-07T10:30:00",
    "image_url": "https://[...]/invoice_1.jpg",
    "invoice_type": "فاتورة شراء",
    "category": "{\"ar\": \"مقهى\", \"en\": \"Cafe\"}",
    "ai_insight": "هذا الشراء من مقهى..."
  }
]
```

---

## 🧠 AI Model Integration

### 1. Vision-Language Model (VLM)

**Model**: Accessed via Hugging Face Inference API

**Purpose**: Extract structured data from invoice images

**Input**: Image URL + Structured prompt

**Output**: JSON with invoice fields

**Capabilities**:
- OCR for Arabic and English text
- Multilingual understanding
- Structured data extraction
- Business category classification
- Invoice type detection
- Smart insight generation

### 2. Large Language Model (LLM)

**Model**: `meta-llama/Meta-Llama-3-8B-Instruct`

**Provider**: Novita via Hugging Face Router

**Purpose**: 
- Convert natural language to SQL
- Generate contextual answers
- Format responses in Arabic

### 3. Embedding Model

**Model**: `sentence-transformers/all-MiniLM-L6-v2`

**Dimensions**: 384

**Purpose**: Generate vector embeddings for semantic search

**Process**:
```python
def generate_embedding(invoice_id, invoice_data, db):
    # Convert invoice dict to text
    full_text = " | ".join([f"{k}: {v}" for k, v in invoice_data.items()])
    
    # Generate normalized embedding
    embedding = model.encode(full_text, normalize_embeddings=True).tolist()
    
    # Store in database
    emb = InvoiceEmbedding(invoice_id=invoice_id, embedding=embedding)
    db.add(emb)
    db.commit()
```

---

## 🔄 Request-Response Workflow

### Example: Complete Invoice Upload & Analysis

```
1. Frontend sends image → POST /upload/
   ↓
2. Backend uploads to Supabase Storage
   ↓
3. Returns public URL
   ↓
4. Frontend sends URL → POST /vlm/analyze
   ↓
5. Backend calls VLM API
   ↓
6. VLM processes image + prompt
   ↓
7. Returns structured JSON
   ↓
8. Backend parses and saves to PostgreSQL
   ↓
9. Generates embedding for RAG
   ↓
10. Returns formatted result to frontend
```

---

## 🔐 Environment Variables

Required in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# Supabase
SUPABASE_URL=https://[project].supabase.co
SUPABASE_KEY=your_anon_key

# AI Models
HF_TOKEN=your_huggingface_token
FRIENDLI_TOKEN=your_friendli_token (optional)
```

---

## 🚀 Deployment Considerations

### Cross-Platform Compatibility

**Windows**:
- Uses PowerShell for scripts
- Path separators handled automatically by Python

**macOS/Linux**:
- Uses bash for scripts
- Native Unix path handling

### Performance Optimizations

1. **Connection Pooling**: SQLAlchemy manages DB connections
2. **Async Operations**: FastAPI async endpoints for I/O operations
3. **Model Caching**: Embedding model loaded once at startup
4. **Vector Search**: Optimized with pgvector indexes

### Error Handling

- Comprehensive try-catch blocks
- Detailed logging with `logging` module
- HTTP status codes: 200 (success), 400 (bad request), 500 (server error)
- User-friendly error messages in Arabic

---

## 📊 Backend Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routers Layer                                            │  │
│  │  • /upload  • /vlm  • /chat  • /dashboard  • /invoices   │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Business Logic & AI Integration                          │  │
│  │  • VLM Analysis  • Embedding Generation  • SQL Builder    │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Data Layer (SQLAlchemy ORM)                              │  │
│  │  • Invoice Model  • Embedding Model  • Items Model        │  │
│  └───────────────────────┬──────────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        │                                      │
        ↓                                      ↓
┌─────────────────┐                  ┌─────────────────────┐
│  Supabase DB    │                  │  Hugging Face API   │
│  (PostgreSQL    │                  │  • VLM              │
│   + pgvector)   │                  │  • LLM              │
│                 │                  │  • Embeddings       │
│  • invoices     │                  └─────────────────────┘
│  • embeddings   │
│  • items        │                  ┌─────────────────────┐
└─────────────────┘                  │  Supabase Storage   │
                                     │  (S3 Bucket)        │
                                     │  • Invoice Images   │
                                     └─────────────────────┘
```

---

## 🔍 Key Features

1. **Multilingual Support**: Handles Arabic and English seamlessly
2. **Hybrid AI Intelligence**: Combines SQL, RAG, and direct retrieval
3. **Vector Search**: Semantic search using pgvector
4. **Real-time Analysis**: Fast VLM inference via Hugging Face
5. **Scalable Architecture**: Modular design for easy extension
6. **Comprehensive Logging**: Detailed logs for debugging
7. **Type Safety**: Pydantic schemas for request/response validation

---

## 📝 Example API Calls

### Using cURL

```bash
# Upload invoice
curl -X POST http://127.0.0.1:8000/upload/ \
  -F "file=@invoice.jpg"

# Analyze invoice
curl -X POST http://127.0.0.1:8000/vlm/analyze \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://[...]/invoice.jpg"}'

# Ask question
curl -X POST http://127.0.0.1:8000/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "كم أنفقت هذا الشهر؟"}'

# Get dashboard stats
curl http://127.0.0.1:8000/dashboard/stats

# Get all invoices
curl http://127.0.0.1:8000/invoices/all
```

---

## 🛠️ Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run migrations** (if needed):
   ```bash
   python backend/run_migration.py
   ```

4. **Start server**:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access API docs**:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

---

**Last Updated**: October 7, 2025  
**Version**: 1.0.0

