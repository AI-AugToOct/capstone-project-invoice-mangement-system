# Smart Invoice Analyzer — End-to-End Workflow

## 🎨 Complete System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        A[👤 User] --> B[🌐 Next.js Frontend]
        B --> |Upload| C[📤 Upload Page]
        B --> |View| D[📋 Invoices Page]
        B --> |Analyze| E[📊 Dashboard Page]
        B --> |Ask| F[💬 Chat Page]
    end
    
    subgraph "API Layer"
        C --> G[POST /upload/]
        C --> H[POST /vlm/analyze]
        D --> I[GET /invoices/all]
        E --> J[GET /dashboard/stats]
        F --> K[POST /chat/ask]
    end
    
    subgraph "Backend Processing"
        G --> L[Supabase Storage]
        L --> |Image URL| H
        H --> M[VLM Processing]
        M --> N[Data Extraction]
        N --> O[Database Save]
        O --> P[Embedding Generation]
        
        K --> Q{Question Type?}
        Q --> |Aggregation| R[SQL Mode]
        Q --> |Semantic| S[RAG Mode]
        Q --> |Specific| T[Retrieval Mode]
        
        R --> U[LLM SQL Generation]
        S --> V[Embedding Search]
        T --> W[Direct DB Query]
    end
    
    subgraph "Data Storage"
        O --> X[(PostgreSQL)]
        P --> Y[(pgvector)]
        L --> Z[🗄️ Image Bucket]
    end
    
    subgraph "AI Models"
        M --> AA[🤖 Hugging Face VLM]
        U --> AB[🧠 Meta-Llama-3-8B]
        V --> AC[🔎 SentenceTransformer]
    end
    
    subgraph "Response Flow"
        X --> |Data| I
        X --> |Stats| J
        U --> |Answer| K
        V --> |Invoices| K
        W --> |Results| K
        
        I --> D
        J --> E
        K --> F
        H --> |Result| C
    end
    
    style A fill:#8dbcc7,stroke:#6fa3b0,stroke-width:3px,color:#fff
    style B fill:#d4a574,stroke:#c89563,stroke-width:3px,color:#fff
    style AA fill:#ff6b6b,stroke:#ee5a5a,stroke-width:2px,color:#fff
    style AB fill:#4ecdc4,stroke:#3dbdb4,stroke-width:2px,color:#fff
    style AC fill:#95e1d3,stroke:#85d1c3,stroke-width:2px,color:#333
    style X fill:#a8e6cf,stroke:#98d6bf,stroke-width:2px,color:#333
    style Y fill:#ffd3b6,stroke:#efc3a6,stroke-width:2px,color:#333
    style Z fill:#ffaaa5,stroke:#ef9a95,stroke-width:2px,color:#fff
```

---

## 📊 Detailed Data Flow Diagram

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant F as 🌐 Frontend
    participant B as ⚙️ Backend API
    participant S as 🗄️ Supabase Storage
    participant V as 🤖 VLM API
    participant D as 💾 Database
    participant E as 🔎 Embeddings
    participant L as 🧠 LLM API

    Note over U,L: 1️⃣ Invoice Upload & Analysis Flow
    
    U->>F: Select/Capture Invoice Image
    F->>B: POST /upload/ (multipart)
    B->>S: Upload image to bucket
    S-->>B: Return public URL
    B-->>F: {"url": "https://..."}
    
    F->>B: POST /vlm/analyze {"image_url": "..."}
    B->>V: Send image + structured prompt
    
    Note over V: VLM processes image<br/>Extracts text, numbers<br/>Classifies category & type<br/>Generates Arabic insight
    
    V-->>B: JSON response (all fields)
    B->>D: Save invoice data
    B->>E: Generate & store embedding
    D-->>B: invoice_id
    B-->>F: Complete analysis result
    F->>U: Display structured data

    Note over U,L: 2️⃣ Chat Question Flow (SQL Mode)
    
    U->>F: Type: "كم أنفقت على المطاعم؟"
    F->>B: POST /chat/ask {"question": "..."}
    
    Note over B: Detects aggregation keywords<br/>Selects SQL Mode
    
    B->>L: Send question with SQL prompt
    L-->>B: "SELECT SUM(CAST(total_amount...))"
    B->>D: Execute SQL query
    D-->>B: [(345.50)]
    B-->>F: {"answer": "أنفقت 345.50 ر.س"}
    F->>U: Display answer

    Note over U,L: 3️⃣ Chat Question Flow (RAG Mode)
    
    U->>F: Type: "ما هي آخر مشترياتي؟"
    F->>B: POST /chat/ask {"question": "..."}
    
    Note over B: Semantic search required<br/>Selects RAG Mode
    
    B->>E: Generate question embedding
    E->>D: Cosine similarity search
    D-->>E: Top-3 matching invoices
    E-->>B: Invoice data + metadata
    B->>L: Send context + question
    L-->>B: Natural language answer
    B-->>F: {"answer": "...", "invoices": [...]}
    F->>U: Display answer + invoice cards

    Note over U,L: 4️⃣ Dashboard Analytics Flow
    
    U->>F: Navigate to Dashboard
    F->>B: GET /invoices/all
    B->>D: SELECT * FROM invoices
    D-->>B: All invoice records
    B-->>F: JSON array
    
    F->>B: GET /dashboard/stats
    B->>D: Aggregation queries
    D-->>B: Counts, sums, top vendors
    B-->>F: {"total_invoices": ..., "total_spent": ...}
    
    Note over F: Frontend processes data<br/>Filters by category/month<br/>Generates charts<br/>Calculates insights
    
    F->>U: Display interactive dashboard
```

---

## 🔄 Component Interaction Diagram

```mermaid
graph LR
    subgraph "Frontend Components"
        A[Home Page] --> B[Navbar]
        C[Upload Page] --> D[CameraCapture]
        C --> E[InvoiceResultCard]
        F[Invoices Page] --> G[ImageModal]
        H[Dashboard Page] --> I[Charts Recharts]
        J[Chat Page] --> K[ScrollArea]
        J --> L[Invoice Cards]
    end
    
    subgraph "API Calls"
        C --> M[/upload/ + /vlm/analyze]
        F --> N[/invoices/all]
        H --> O[/dashboard/stats + /invoices/all]
        J --> P[/chat/ask]
    end
    
    subgraph "Backend Routes"
        M --> Q[upload.py + vlm.py]
        N --> R[invoices.py]
        O --> S[dashboard.py + invoices.py]
        P --> T[chat.py]
    end
    
    subgraph "Data Layer"
        Q --> U[(invoices table)]
        Q --> V[(invoice_embeddings)]
        R --> U
        S --> U
        T --> U
        T --> V
        T --> W[LLM]
    end
    
    style A fill:#8dbcc7,stroke:#6fa3b0,stroke-width:2px
    style C fill:#d4a574,stroke:#c89563,stroke-width:2px
    style F fill:#a8e6cf,stroke:#98d6bf,stroke-width:2px
    style H fill:#ffd3b6,stroke:#efc3a6,stroke-width:2px
    style J fill:#ffaaa5,stroke:#ef9a95,stroke-width:2px
```

---

## 🧠 AI Processing Pipeline

```mermaid
graph TD
    A[📷 Invoice Image] --> B{Upload Type}
    B -->|File| C[Direct Upload]
    B -->|Camera| D[Capture → Convert]
    
    C --> E[Supabase Storage]
    D --> E
    
    E --> F[Public Image URL]
    F --> G[VLM API Call]
    
    G --> H{VLM Processing}
    H --> I[OCR Arabic/English]
    H --> J[Extract Structured Data]
    H --> K[Detect Category]
    H --> L[Classify Invoice Type]
    H --> M[Generate AI Insight AR]
    
    I --> N[Parse JSON Response]
    J --> N
    K --> N
    L --> N
    M --> N
    
    N --> O{Validation}
    O -->|Valid| P[Save to Database]
    O -->|Invalid| Q[Use Fallback Values]
    Q --> P
    
    P --> R[Generate Text Representation]
    R --> S[Sentence Transformer Encode]
    S --> T[384D Vector Embedding]
    T --> U[Save to pgvector]
    
    P --> V[✅ Analysis Complete]
    U --> V
    
    style G fill:#ff6b6b,stroke:#ee5a5a,stroke-width:3px,color:#fff
    style S fill:#4ecdc4,stroke:#3dbdb4,stroke-width:3px,color:#fff
    style P fill:#95e1d3,stroke:#85d1c3,stroke-width:3px,color:#333
```

---

## 💬 Hybrid Chat Intelligence Flow

```mermaid
graph TB
    A[👤 User Question] --> B{Analyze Question}
    
    B --> C{Contains Aggregation?}
    C -->|Yes: كم, مجموع, إجمالي| D[🧮 SQL Mode]
    C -->|No| E{Contains Vendor/Type?}
    
    E -->|Yes: دانكن, ستاربكس| F[🖼️ Retrieval Mode]
    E -->|No| G[📄 RAG Mode]
    
    D --> H[LLM: Text → SQL]
    H --> I[Fix Numeric Casts]
    I --> J[Execute Query]
    J --> K[Format Result in Arabic]
    K --> L[Return Answer]
    
    F --> M[Extract Keywords]
    M --> N[Direct ILIKE Search]
    N --> O[Fetch Matching Invoices]
    O --> P[Include image_url]
    P --> Q[Return Answer + Cards]
    
    G --> R[Generate Question Embedding]
    R --> S[pgvector Cosine Search]
    S --> T[Retrieve Top-K Invoices]
    T --> U[Send Context to LLM]
    U --> V[Generate Contextual Answer]
    V --> W[Return Answer + Context]
    
    L --> X[📱 Frontend Display]
    Q --> X
    W --> X
    
    style D fill:#ffd93d,stroke:#efc92d,stroke-width:3px,color:#333
    style F fill:#6bcf7f,stroke:#5bbf6f,stroke-width:3px,color:#fff
    style G fill:#4ecdc4,stroke:#3ebdb4,stroke-width:3px,color:#fff
    style H fill:#ff6b6b,stroke:#ef5b5b,stroke-width:2px,color:#fff
    style S fill:#a8e6cf,stroke:#98d6bf,stroke-width:2px,color:#333
```

---

## 📊 Database Schema Relationships

```mermaid
erDiagram
    INVOICES ||--o{ ITEMS : contains
    INVOICES ||--o| INVOICE_EMBEDDINGS : has
    
    INVOICES {
        int id PK
        int record
        string invoice_number
        datetime invoice_date
        string vendor
        string tax_number
        string cashier
        string branch
        string phone
        string subtotal
        string tax
        string total_amount
        string grand_total
        string discounts
        string payment_method
        string amount_paid
        string ticket_number
        string category
        string ai_insight
        string invoice_type
        string image_url
        datetime created_at
    }
    
    ITEMS {
        int id PK
        int invoice_id FK
        string description
        float quantity
        float unit_price
        float total
    }
    
    INVOICE_EMBEDDINGS {
        int id PK
        int invoice_id FK
        vector_384 embedding
    }
```

---

## 🚀 Technology Stack Overview

```mermaid
graph TB
    subgraph "Frontend Stack"
        A[Next.js 14 App Router]
        B[React 18 TypeScript]
        C[Tailwind CSS]
        D[shadcn/ui Components]
        E[Framer Motion]
        F[Recharts]
        G[jsPDF]
    end
    
    subgraph "Backend Stack"
        H[FastAPI Python]
        I[SQLAlchemy ORM]
        J[Pydantic Schemas]
        K[Uvicorn Server]
    end
    
    subgraph "Database Stack"
        L[PostgreSQL Supabase]
        M[pgvector Extension]
        N[Supabase Storage S3]
    end
    
    subgraph "AI Stack"
        O[Hugging Face VLM]
        P[Meta-Llama-3-8B]
        Q[SentenceTransformer]
        R[all-MiniLM-L6-v2]
    end
    
    A --> H
    H --> L
    H --> N
    H --> O
    H --> P
    H --> Q
    Q --> R
    
    style A fill:#8dbcc7,stroke:#6fa3b0,stroke-width:2px,color:#fff
    style H fill:#d4a574,stroke:#c89563,stroke-width:2px,color:#fff
    style L fill:#a8e6cf,stroke:#98d6bf,stroke-width:2px,color:#333
    style O fill:#ff6b6b,stroke:#ef5b5b,stroke-width:2px,color:#fff
```

---

## 🎨 UI Component Hierarchy

```mermaid
graph TD
    A[RootLayout] --> B[ThemeProvider]
    B --> C[Navbar + ThemeToggle]
    B --> D[Page Content]
    B --> E[Footer]
    B --> F[Toaster]
    
    D --> G[Home Page]
    D --> H[Upload Page]
    D --> I[Invoices Page]
    D --> J[Dashboard Page]
    D --> K[Chat Page]
    
    H --> L[CameraCapture]
    H --> M[InvoiceResultCard]
    H --> N[Progress]
    H --> O[GlobalLoader]
    
    I --> P[Select Filter]
    I --> Q[Invoice Cards Grid]
    I --> R[ImageModal]
    
    Q --> S[Card + Image]
    Q --> T[PDF Download Button]
    
    J --> U[Filter Dropdowns x3]
    J --> V[Stats Cards x4]
    J --> W[Charts x4]
    J --> X[Smart Insights]
    
    W --> Y[PieChart Recharts]
    W --> Z[AreaChart]
    W --> AA[BarChart]
    W --> AB[RadarChart]
    
    K --> AC[ScrollArea Messages]
    K --> AD[Input + Send Button]
    K --> AE[Invoice Cards in Chat]
    
    style A fill:#1a1a1a,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#8dbcc7,stroke:#6fa3b0,stroke-width:2px,color:#fff
    style C fill:#d4a574,stroke:#c89563,stroke-width:2px,color:#fff
```

---

## 📈 Performance & Scalability

```mermaid
graph LR
    subgraph "Optimization Layers"
        A[Frontend Caching] --> B[API Response Cache]
        B --> C[Database Connection Pool]
        C --> D[Vector Index ivfflat]
        D --> E[Batch Embedding Generation]
    end
    
    subgraph "Scalability Options"
        F[Horizontal Scaling]
        G[Load Balancer]
        H[Database Replication]
        I[CDN for Images]
        J[Serverless Functions]
    end
    
    A --> F
    B --> G
    C --> H
    D --> I
    E --> J
    
    style A fill:#4ecdc4,color:#fff
    style B fill:#95e1d3
    style C fill:#ffd3b6
    style D fill:#ffaaa5,color:#fff
    style E fill:#ff6b6b,color:#fff
```

---

## 🎯 User Journey Map

```mermaid
journey
    title Smart Invoice Analyzer User Journey
    section Discovery
      Visit Homepage: 5: User
      Read Features: 4: User
      Click "ابدأ الآن": 5: User
    section Upload
      Select Invoice Image: 4: User
      Wait for Upload: 3: System
      See Progress Bar: 4: System
      View Analysis Results: 5: User, System
    section Explore
      Navigate to Invoices: 5: User
      Filter by Category: 5: User
      View Invoice Image: 5: User
      Download PDF: 5: User
    section Analyze
      Go to Dashboard: 5: User
      Apply Filters: 4: User
      Explore Charts: 5: User
      Read Smart Insights: 5: User
    section Interact
      Open Chat Page: 5: User
      Ask Question: 4: User
      Receive AI Answer: 5: System
      View Invoice Cards: 5: User
    section Customize
      Toggle Dark Mode: 5: User
      Enjoy Experience: 5: User
```

---

**This diagram suite provides a comprehensive visual overview of the Smart Invoice Analyzer system, suitable for presentations, documentation, and poster displays.**

**Color Legend:**
- 🔵 **Teal (#8dbcc7)**: Frontend/UI components
- 🟡 **Gold (#d4a574)**: Backend/API layer
- 🟢 **Green (#a8e6cf)**: Database/Storage
- 🔴 **Red (#ff6b6b)**: AI/ML models
- 🟣 **Purple (#95e1d3)**: Processing/Logic

---

**Last Updated**: October 7, 2025  
**Version**: 1.0.0

