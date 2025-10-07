# API Reference

## 📡 Base URL

```
http://127.0.0.1:8000
```

For production, replace with your deployed backend URL.

---

## 🔐 Authentication

Currently, the API uses environment-based authentication for external services (Hugging Face, Supabase). No user authentication is required for endpoints.

---

## 📋 Endpoints Overview

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/upload/` | POST | Upload invoice image |
| `/vlm/analyze` | POST | Analyze invoice with VLM |
| `/chat/ask` | POST | Ask question about invoices |
| `/dashboard/stats` | GET | Get dashboard statistics |
| `/dashboard/ping` | GET | Dashboard health check |
| `/invoices/all` | GET | Get all invoices |

---

## 🔹 1. Root Endpoint

### `GET /`

Health check endpoint.

#### Response
```json
{
  "message": "Hello from FastAPI + Supabase + HuggingFace VLM 🚀"
}
```

#### Status Codes
- `200 OK`: Server is running

#### Example (cURL)
```bash
curl http://127.0.0.1:8000/
```

#### Example (Postman)
```
GET http://127.0.0.1:8000/
```

---

## 🔹 2. Upload Invoice

### `POST /upload/`

Upload an invoice image to Supabase Storage.

#### Request

**Content-Type**: `multipart/form-data`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Invoice image (JPG, PNG) |

#### Response
```json
{
  "url": "https://[project].supabase.co/storage/v1/object/public/invoices/invoice_123.jpg"
}
```

#### Status Codes
- `200 OK`: Upload successful
- `400 Bad Request`: Invalid file or upload failed
- `500 Internal Server Error`: Server error

#### Example (cURL)
```bash
curl -X POST http://127.0.0.1:8000/upload/ \
  -F "file=@/path/to/invoice.jpg"
```

#### Example (Postman)
1. Method: `POST`
2. URL: `http://127.0.0.1:8000/upload/`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select image file

#### Example (Python)
```python
import requests

url = "http://127.0.0.1:8000/upload/"
files = {"file": open("invoice.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

#### Example (JavaScript)
```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);

const response = await fetch("http://127.0.0.1:8000/upload/", {
  method: "POST",
  body: formData,
});

const data = await response.json();
console.log(data.url);
```

---

## 🔹 3. Analyze Invoice

### `POST /vlm/analyze`

Analyze an invoice image using Vision-Language Model.

#### Request

**Content-Type**: `application/json`

**Body**:
```json
{
  "image_url": "https://[...]/invoice.jpg",
  "prompt": "Optional custom prompt (default VLM prompt used if omitted)"
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | Yes | Public URL of invoice image |
| `prompt` | string | No | Custom analysis prompt |

#### Response
```json
{
  "status": "success",
  "invoice_id": 42,
  "output": {
    "Invoice Number": "INV-12345",
    "Date": "2025-10-07",
    "Vendor": "Coffee Shop",
    "Tax Number": "123456789",
    "Cashier": "John Doe",
    "Branch": "Downtown",
    "Phone": "0551234567",
    "Items": [
      {
        "description": "Cappuccino",
        "quantity": 2,
        "unit_price": 15.00,
        "total": 30.00
      }
    ],
    "Subtotal": "30.00",
    "Tax": "4.50",
    "Total Amount": "34.50",
    "Grand Total (before tax)": "30.00",
    "Discounts": "0.00",
    "Payment Method": "Visa",
    "Amount Paid": "34.50",
    "Ticket Number": "T-9876",
    "Category": "Cafe",
    "Keywords_Detected": ["شراء", "Purchase", "قهوة"],
    "Invoice_Type": "فاتورة شراء",
    "AI_Insight": "هذا الشراء من مقهى Coffee Shop. العميل طلب مشروبين بمبلغ معتدل. المشتريات المتكررة من المقاهي قد تشير إلى عادة يومية."
  },
  "category": {
    "ar": "مقهى",
    "en": "Cafe"
  },
  "ai_insight": "هذا الشراء من مقهى Coffee Shop...",
  "invoice_type": "فاتورة شراء",
  "image_url": "https://[...]/invoice.jpg"
}
```

#### Status Codes
- `200 OK`: Analysis successful
- `400 Bad Request`: Invalid request
- `500 Internal Server Error`: VLM or database error

#### Example (cURL)
```bash
curl -X POST http://127.0.0.1:8000/vlm/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://[project].supabase.co/storage/v1/object/public/invoices/invoice_123.jpg"
  }'
```

#### Example (Postman)
1. Method: `POST`
2. URL: `http://127.0.0.1:8000/vlm/analyze`
3. Headers: `Content-Type: application/json`
4. Body → raw (JSON):
```json
{
  "image_url": "https://[...]/invoice.jpg"
}
```

#### Example (Python)
```python
import requests

url = "http://127.0.0.1:8000/vlm/analyze"
payload = {
    "image_url": "https://[...]/invoice.jpg"
}
response = requests.post(url, json=payload)
print(response.json())
```

#### Example (JavaScript)
```javascript
const response = await fetch("http://127.0.0.1:8000/vlm/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    image_url: "https://[...]/invoice.jpg"
  }),
});

const result = await response.json();
console.log(result);
```

---

## 🔹 4. Chat with AI

### `POST /chat/ask`

Ask a natural language question about invoices.

#### Request

**Content-Type**: `application/json`

**Body**:
```json
{
  "question": "كم أنفقت على المطاعم هذا الشهر؟",
  "top_k": 3
}
```

**Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `question` | string | Yes | - | Natural language question (Arabic/English) |
| `top_k` | integer | No | 3 | Number of results for RAG mode |

#### Response

**SQL Mode** (aggregation questions):
```json
{
  "answer": "أنفقت 345.50 ر.س على المطاعم هذا الشهر",
  "mode": "sql",
  "sql_query": "SELECT SUM(CAST(total_amount AS FLOAT)) FROM invoices WHERE...",
  "invoices": []
}
```

**RAG Mode** (semantic search):
```json
{
  "answer": "بناءً على فواتيرك، آخر مشترياتك من المقاهي كانت من Starbucks وDunkin",
  "mode": "rag",
  "invoices": [
    {
      "id": 5,
      "vendor": "Starbucks",
      "total": "45.00",
      "date": "2025-10-07",
      "image_url": "https://[...]/invoice_5.jpg",
      "invoice_type": "فاتورة شراء"
    }
  ]
}
```

**Retrieval Mode** (direct search):
```json
{
  "answer": "تم العثور على 3 فواتير من دانكن",
  "mode": "retrieval",
  "invoices": [
    {
      "id": 10,
      "vendor": "Dunkin",
      "invoice_number": "INV-5432",
      "total": "35.25",
      "date": "2025-09-30",
      "payment_method": "Visa",
      "image_url": "https://[...]/invoice_10.jpg",
      "invoice_type": "فاتورة شراء",
      "ai_insight": "شراء من دانكن دونتس..."
    }
  ]
}
```

#### Status Codes
- `200 OK`: Query successful
- `400 Bad Request`: Invalid question
- `500 Internal Server Error`: Database or AI error

#### Example (cURL)
```bash
curl -X POST http://127.0.0.1:8000/chat/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "كم أنفقت على المطاعم؟",
    "top_k": 5
  }'
```

#### Example (Postman)
1. Method: `POST`
2. URL: `http://127.0.0.1:8000/chat/ask`
3. Headers: `Content-Type: application/json`
4. Body → raw (JSON):
```json
{
  "question": "أرسل لي فواتير دانكن",
  "top_k": 3
}
```

#### Example (Python)
```python
import requests

url = "http://127.0.0.1:8000/chat/ask"
payload = {
    "question": "كم عدد الفواتير هذا الشهر؟",
    "top_k": 5
}
response = requests.post(url, json=payload)
print(response.json())
```

#### Example (JavaScript)
```javascript
const response = await fetch("http://127.0.0.1:8000/chat/ask", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    question: "ما هي آخر فاتورة اشتريتها؟",
    top_k: 3
  }),
});

const data = await response.json();
console.log(data);
```

---

## 🔹 5. Dashboard Statistics

### `GET /dashboard/stats`

Get aggregated statistics for dashboard.

#### Response
```json
{
  "total_invoices": 156,
  "total_spent": 12456.75,
  "top_vendors": [
    {
      "vendor": "Starbucks",
      "count": 23
    },
    {
      "vendor": "Dunkin",
      "count": 18
    },
    {
      "vendor": "Panda",
      "count": 15
    }
  ]
}
```

#### Status Codes
- `200 OK`: Success
- `500 Internal Server Error`: Database error

#### Example (cURL)
```bash
curl http://127.0.0.1:8000/dashboard/stats
```

#### Example (Postman)
```
GET http://127.0.0.1:8000/dashboard/stats
```

#### Example (Python)
```python
import requests

url = "http://127.0.0.1:8000/dashboard/stats"
response = requests.get(url)
print(response.json())
```

#### Example (JavaScript)
```javascript
const response = await fetch("http://127.0.0.1:8000/dashboard/stats");
const data = await response.json();
console.log(data);
```

---

## 🔹 6. Dashboard Health Check

### `GET /dashboard/ping`

Check dashboard endpoint availability.

#### Response
```json
{
  "message": "✅ Dashboard endpoint is live!"
}
```

#### Status Codes
- `200 OK`: Endpoint is live

#### Example (cURL)
```bash
curl http://127.0.0.1:8000/dashboard/ping
```

---

## 🔹 7. Get All Invoices

### `GET /invoices/all`

Retrieve all invoices with full metadata.

#### Response
```json
[
  {
    "id": 1,
    "record": 1,
    "invoice_number": "INV-12345",
    "invoice_date": "2025-10-07T10:30:00",
    "vendor": "Starbucks",
    "tax_number": "123456789",
    "cashier": "John Doe",
    "branch": "Downtown",
    "phone": "0551234567",
    "subtotal": "30.00",
    "tax": "4.50",
    "total_amount": "34.50",
    "grand_total": "34.50",
    "discounts": "0.00",
    "payment_method": "Visa",
    "amount_paid": "34.50",
    "ticket_number": "T-9876",
    "category": "{\"ar\": \"مقهى\", \"en\": \"Cafe\"}",
    "ai_insight": "هذا الشراء من مقهى Starbucks...",
    "invoice_type": "فاتورة شراء",
    "image_url": "https://[...]/invoice_1.jpg",
    "created_at": "2025-10-07T10:35:00"
  }
]
```

#### Status Codes
- `200 OK`: Success
- `500 Internal Server Error`: Database error

#### Example (cURL)
```bash
curl http://127.0.0.1:8000/invoices/all
```

#### Example (Postman)
```
GET http://127.0.0.1:8000/invoices/all
```

#### Example (Python)
```python
import requests

url = "http://127.0.0.1:8000/invoices/all"
response = requests.get(url)
invoices = response.json()
for invoice in invoices:
    print(f"{invoice['vendor']}: {invoice['total_amount']}")
```

#### Example (JavaScript)
```javascript
const response = await fetch("http://127.0.0.1:8000/invoices/all");
const invoices = await response.json();
invoices.forEach(inv => {
  console.log(`${inv.vendor}: ${inv.total_amount}`);
});
```

---

## 🔄 Complete Workflow Example

### Scenario: Upload and Analyze Invoice

```bash
# Step 1: Upload image
curl -X POST http://127.0.0.1:8000/upload/ \
  -F "file=@invoice.jpg"

# Response:
# {"url": "https://[...]/invoice.jpg"}

# Step 2: Analyze image
curl -X POST http://127.0.0.1:8000/vlm/analyze \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://[...]/invoice.jpg"}'

# Response:
# {
#   "status": "success",
#   "invoice_id": 42,
#   "output": {...},
#   "category": {"ar": "مقهى", "en": "Cafe"},
#   ...
# }

# Step 3: Ask question
curl -X POST http://127.0.0.1:8000/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "كم أنفقت اليوم؟"}'

# Response:
# {
#   "answer": "أنفقت 34.50 ر.س اليوم",
#   "mode": "sql"
# }

# Step 4: Get dashboard stats
curl http://127.0.0.1:8000/dashboard/stats

# Response:
# {
#   "total_invoices": 1,
#   "total_spent": 34.50,
#   "top_vendors": [{"vendor": "Starbucks", "count": 1}]
# }
```

---

## 📊 API Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      Frontend Client                          │
│              (Browser / Mobile / Postman)                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         ↓
┌──────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  CORS Middleware                                        │  │
│  │  - Allow origins: localhost:3000, 127.0.0.1:3000      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Router Layer                                           │  │
│  │                                                         │  │
│  │  GET  /                    → Health check              │  │
│  │  POST /upload/             → Upload to Supabase        │  │
│  │  POST /vlm/analyze         → VLM analysis              │  │
│  │  POST /chat/ask            → AI chat                   │  │
│  │  GET  /dashboard/stats     → Aggregations              │  │
│  │  GET  /invoices/all        → Fetch all invoices        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                                   │  │
│  │  - VLM processing                                       │  │
│  │  - Embedding generation                                 │  │
│  │  - SQL query generation                                 │  │
│  │  - Hybrid intelligence routing                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Database Layer (SQLAlchemy ORM)                        │  │
│  │  - Invoice, InvoiceEmbedding, Item models              │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────┬───────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ↓               ↓               ↓
┌──────────────┐ ┌─────────────┐ ┌──────────────────┐
│  Supabase    │ │  Supabase   │ │  Hugging Face    │
│  Database    │ │  Storage    │ │  Inference API   │
│  (Postgres)  │ │  (Bucket)   │ │  - VLM           │
│              │ │             │ │  - LLM           │
│  • invoices  │ │  • Images   │ │  - Embeddings    │
│  • items     │ │             │ │                  │
│  • embeddings│ │             │ │                  │
└──────────────┘ └─────────────┘ └──────────────────┘
```

---

## ⚙️ Error Handling

All endpoints return standard HTTP status codes and error messages:

### Common Error Responses

**400 Bad Request**:
```json
{
  "detail": "Invalid image URL"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Database connection failed"
}
```

### Error Codes Summary

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters, missing fields |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Database error, AI model error, network issue |

---

## 🔒 Rate Limiting

Currently, no rate limiting is implemented. For production:

1. Add rate limiting middleware (e.g., `slowapi`)
2. Set limits per endpoint:
   - `/upload/`: 10 requests/minute
   - `/vlm/analyze`: 5 requests/minute (expensive)
   - `/chat/ask`: 20 requests/minute
   - `/dashboard/stats`: 100 requests/minute
   - `/invoices/all`: 50 requests/minute

---

## 📦 Postman Collection

You can import this collection into Postman:

```json
{
  "info": {
    "name": "Smart Invoice Analyzer API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://127.0.0.1:8000/"
      }
    },
    {
      "name": "Upload Invoice",
      "request": {
        "method": "POST",
        "url": "http://127.0.0.1:8000/upload/",
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "file",
              "type": "file",
              "src": "invoice.jpg"
            }
          ]
        }
      }
    },
    {
      "name": "Analyze Invoice",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": "http://127.0.0.1:8000/vlm/analyze",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"image_url\": \"https://[...]/invoice.jpg\"\n}"
        }
      }
    },
    {
      "name": "Chat - Ask Question",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": "http://127.0.0.1:8000/chat/ask",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"question\": \"كم أنفقت على المطاعم؟\",\n  \"top_k\": 3\n}"
        }
      }
    },
    {
      "name": "Dashboard Stats",
      "request": {
        "method": "GET",
        "url": "http://127.0.0.1:8000/dashboard/stats"
      }
    },
    {
      "name": "Get All Invoices",
      "request": {
        "method": "GET",
        "url": "http://127.0.0.1:8000/invoices/all"
      }
    }
  ]
}
```

---

## 🚀 Interactive API Documentation

FastAPI provides automatic interactive documentation:

### Swagger UI
```
http://127.0.0.1:8000/docs
```

### ReDoc
```
http://127.0.0.1:8000/redoc
```

These provide:
- Visual interface to test endpoints
- Auto-generated request/response examples
- Schema validation
- Try-it-out functionality

---

**Last Updated**: October 7, 2025  
**Version**: 1.0.0

