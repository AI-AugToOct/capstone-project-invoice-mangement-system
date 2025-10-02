# 🧾 Invoice Management & Analysis

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📋 Overview

Invoice Management & Analysis is a comprehensive capstone project that leverages AI-powered OCR to streamline invoice processing. The system uses the Qwen 32B Vision-Language Model to automatically extract metadata and line items from invoices in both Arabic and English, providing businesses with an efficient way to digitize and manage their financial documents.

## ✨ Features

- **Multi-format Upload**: Support for JPG, PNG, and PDF invoice formats through an intuitive Streamlit interface
- **Bilingual OCR**: Advanced data extraction powered by Qwen 32B VLM for Arabic and English invoices
- **Smart Extraction**: Automatic detection of invoice metadata (date, vendor, total) and line items (description, quantity, price)
- **Human-in-the-Loop**: Review and edit extracted data before committing to database
- **Persistent Storage**: Secure storage in PostgreSQL via Supabase cloud infrastructure
- **Interactive Dashboard**: View, search, and manage all saved invoices in real-time
- **RESTful API**: Comprehensive API with auto-generated Swagger documentation
- **Cloud-Ready**: Deployed on Streamlit Cloud for easy access and scalability

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Streamlit UI]
    end
    
    subgraph "Backend Layer"
        B[FastAPI Server]
        C[SQLAlchemy ORM]
    end
    
    subgraph "AI/ML Layer"
        D[Qwen 32B VLM]
    end
    
    subgraph "Data Layer"
        E[(PostgreSQL on Supabase)]
    end
    
    A -->|HTTP Requests| B
    B -->|Invoice Processing| D
    B -->|ORM Queries| C
    C -->|SQL Operations| E
    D -->|Extracted Data| B
    B -->|JSON Response| A
    
    style A fill:#ff4b4b
    style B fill:#009688
    style D fill:#8b5cf6
    style E fill:#3ecf8e
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, SQLAlchemy, Uvicorn |
| **Frontend** | Streamlit |
| **Database** | PostgreSQL (Supabase) |
| **AI/ML** | Qwen 32B Vision-Language Model |
| **Deployment** | Streamlit Cloud, Supabase Cloud |
| **Language** | Python 3.9+ |

## 🗄️ Database Schema

```sql
-- Invoices Table
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    vendor_name VARCHAR(255) NOT NULL,
    invoice_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'SAR',
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items Table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    line_total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster queries
CREATE INDEX idx_invoice_number ON invoices(invoice_number);
CREATE INDEX idx_invoice_date ON invoices(invoice_date);
CREATE INDEX idx_invoice_id_items ON items(invoice_id);
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.9 or higher
- PostgreSQL database (Supabase account)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/invoice-management.git
   cd invoice-management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   QWEN_API_KEY=your_qwen_api_key
   ```

5. **Initialize the database**
   ```bash
   python -m backend.database.init_db
   ```

6. **Run the backend server**
   ```bash
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://localhost:8000`
   
   Swagger docs: `http://localhost:8000/docs`

7. **Run the frontend (in a new terminal)**
   ```bash
   streamlit run app.py
   ```
   The app will open at `http://localhost:8501`

### 📦 Project Structure

```
invoice-management/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── database/
│   │   ├── connection.py       # Database connection
│   │   └── init_db.py          # Database initialization
│   ├── services/
│   │   ├── ocr_service.py      # Qwen VLM integration
│   │   └── invoice_service.py  # Business logic
│   └── routers/
│       └── invoices.py         # API endpoints
├── app.py                      # Streamlit frontend
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### 🌐 Deployment on Streamlit Cloud

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Add your environment variables in the "Advanced settings"
   - Click "Deploy"

3. **Backend Deployment**
   
   For the FastAPI backend, consider deploying to:
   - **Railway**: Easy deployment with GitHub integration
   - **Render**: Free tier available with automatic deployments
   - **Heroku**: Classic platform with straightforward setup
   
   Update your Streamlit app with the deployed backend URL.

## 📊 Example Workflow

1. **Upload Invoice**: User uploads an invoice image or PDF through the Streamlit interface
2. **AI Extraction**: Qwen 32B VLM processes the document and extracts:
   - Invoice number, date, vendor name, total amount
   - Line items with descriptions, quantities, and prices
3. **Review & Edit**: User reviews the extracted data in an editable form
4. **Confirm & Save**: User confirms accuracy and saves to PostgreSQL database
5. **View Dashboard**: Access all invoices through the interactive dashboard with search and filter capabilities

## 🗺️ Roadmap

- [ ] **Analytics Dashboard**: Visualization of spending patterns and vendor analysis
- [ ] **Export Functionality**: Export invoices to CSV, Excel, and PDF formats
- [ ] **Multi-user Support**: Role-based access control and user authentication
- [ ] **Email Integration**: Automatic invoice extraction from email attachments
- [ ] **Mobile App**: React Native mobile application for on-the-go invoice scanning
- [ ] **Advanced Search**: Full-text search with filters by date range, vendor, and amount
- [ ] **Duplicate Detection**: AI-powered duplicate invoice detection
- [ ] **Multi-currency Support**: Automatic currency conversion and multi-currency reporting
- [ ] **Audit Trail**: Complete history of invoice modifications and user actions
- [ ] **API Webhooks**: Real-time notifications for invoice processing events

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
- [Streamlit](https://streamlit.io/) - The fastest way to build data apps
- [Supabase](https://supabase.com/) - Open source Firebase alternative
- [Qwen](https://github.com/QwenLM/Qwen) - Alibaba Cloud's Vision-Language Model
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM

---

⭐ If you found this project helpful, please give it a star!

📧 For questions or support, please open an issue or contact me directly.
