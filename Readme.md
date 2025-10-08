# 📑 Smart Invoice Analyzer

An intelligent invoice management system powered by FastAPI, Next.js, Supabase, and Friendli AI.

## 🌟 Features

- 📸 **Smart Upload**: Upload invoices via file upload or camera capture
- 🤖 **AI Analysis**: Automated invoice data extraction using VLM (Vision Language Models)
- 💬 **Chat Interface**: Ask questions about your invoices using natural language
- 📊 **Dashboard**: Comprehensive analytics and insights
- 🔍 **Invoice Management**: Search, filter, and manage all invoices
- 🌙 **Dark Mode**: Built-in theme switching

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database with pgvector extension
- **Supabase** - Backend as a Service (Storage + DB)
- **OpenAI** - Embeddings for semantic search
- **Friendli AI** - Chat completions and VLM

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Framer Motion** - Smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL (or Supabase account)
- Docker (optional)

### Option 1: One-Command Start

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

Choose between:
1. **Docker mode** - Production-like environment
2. **Local mode** - Development with hot reload

### Option 2: Docker Compose

```bash
docker-compose up -d
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 3: Manual Setup

**1. Backend Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**2. Frontend Setup**
```bash
cd frontend-nextjs
npm install
npm run dev
```

## ⚙️ Configuration

### Environment Variables

**Backend (.env):**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_BUCKET=invoices
DATABASE_URL=postgresql://user:password@host:5432/database
OPENAI_API_KEY=your_openai_key
EMBEDDING_MODEL=text-embedding-3-small
FRIENDLI_TOKEN=your_friendli_token
FRIENDLI_URL=https://api.friendli.ai/dedicated/v1/chat/completions
FRIENDLI_MODEL_ID=your_model_id
```

**Frontend (frontend-nextjs/.env.local):**
```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

See `.env.example` files for templates.

## 📦 Project Structure

```
capstone-project-invoice-mangement-system/
├── backend/
│   ├── models/           # Database models
│   ├── routers/          # API endpoints
│   ├── schemas/          # Pydantic schemas
│   ├── main.py           # FastAPI app
│   └── database.py       # DB connection
├── frontend-nextjs/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   ├── lib/              # Utilities
│   └── public/           # Static assets
├── Dockerfile.backend    # Backend container
├── Dockerfile.frontend   # Frontend container
├── docker-compose.yml    # Multi-container setup
├── run.sh               # Unix startup script
├── run.bat              # Windows startup script
└── requirements.txt     # Python dependencies
```

## 🚢 Deployment

### Railway (Backend)
1. Create new project on [Railway](https://railway.app)
2. Add environment variables from `.env`
3. Set Dockerfile path: `Dockerfile.backend`
4. Deploy

### Vercel (Frontend)
1. Import project on [Vercel](https://vercel.com)
2. Set root directory: `frontend-nextjs`
3. Add environment variables:
   - `NEXT_PUBLIC_API_BASE_URL` → Railway backend URL
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_KEY`
4. Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🧪 Testing

```bash
# Backend tests
pytest backend/

# Frontend tests
cd frontend-nextjs
npm test
```

## 📝 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Development

### Backend Development
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn backend.main:app --reload

# Format code
black backend/

# Lint
flake8 backend/
```

### Frontend Development
```bash
cd frontend-nextjs

# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint
npm run lint
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Windows
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Linux/Mac
pkill -f uvicorn
pkill -f next
```

**Docker issues:**
```bash
# Clean up
docker-compose down
docker system prune -a

# Rebuild
docker-compose build --no-cache
docker-compose up
```

**Frontend can't connect to backend:**
- Check `NEXT_PUBLIC_API_BASE_URL` in `.env.local`
- Verify backend is running on correct port
- Check browser console for CORS errors

See [DEPLOYMENT.md](DEPLOYMENT.md) for more troubleshooting tips.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Review API docs at `/docs` endpoint

---

**Built with ❤️ using FastAPI, Next.js, Supabase, and Friendli AI**
