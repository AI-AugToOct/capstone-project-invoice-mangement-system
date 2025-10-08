# 🚀 DEPLOYMENT READINESS GUIDE
**Smart Invoice Analyzer** - FastAPI + Next.js + Supabase + Friendli AI

---

## 📊 PROJECT ANALYSIS SUMMARY

### ✅ What's Ready

| Component | Status | Details |
|-----------|--------|---------|
| **Backend Framework** | ✅ Ready | FastAPI 0.118.0 with Uvicorn |
| **Frontend Framework** | ✅ Ready | Next.js 14.2.3 with standalone output |
| **Database** | ✅ Configured | PostgreSQL via Supabase with SQLAlchemy |
| **CORS** | ✅ Configured | Vercel domains whitelisted |
| **Docker Support** | ✅ Ready | Dockerfile.backend exists |
| **Railway Config** | ✅ Exists | railway.json configured |
| **Vercel Config** | ✅ Exists | vercel.json configured |
| **Dependencies** | ✅ Locked | requirements.txt and package.json |
| **API Integration** | ✅ Working | Frontend uses NEXT_PUBLIC_API_BASE_URL |

### ⚠️ What Needs Attention

| Issue | Severity | Action Required |
|-------|----------|-----------------|
| **Database Password** | 🔴 Critical | Correct Supabase password needed |
| **Environment Files** | 🟡 Important | .env and .env.local are gitignored |
| **CORS Wildcard** | 🟡 Security | Remove `"*"` from CORS in production |
| **Supabase Connection** | 🟡 Important | Consider using connection pooler |

### 🔧 Configuration Details

**Backend Entry Point:** `backend.main:app`  
**Frontend Root:** `frontend-nextjs/`  
**Python Version:** 3.12  
**Node Version:** 20+

---

## 🚂 RAILWAY DEPLOYMENT (Backend)

### Configuration

```json
{
  "Root Directory": ".",
  "Builder": "Dockerfile",
  "Dockerfile Path": "Dockerfile.backend",
  "Start Command": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
  "Region": "us-west-2 (recommended)"
}
```

### Environment Variables for Railway

Copy these EXACTLY to Railway dashboard:

```bash
# ===== DATABASE =====
DATABASE_URL=postgresql://postgres:[YOUR_CORRECT_PASSWORD]@db.pcktfzshbxaljkbedrar.supabase.co:5432/postgres
# ⚠️ IMPORTANT: Replace [YOUR_CORRECT_PASSWORD] with actual password
# ⚠️ If password contains @, encode it as %40

# ===== SUPABASE =====
SUPABASE_URL=https://pcktfzshbxaljkbedrar.supabase.co
SUPABASE_KEY=[GET_FROM_SUPABASE_DASHBOARD]
SUPABASE_SERVICE_ROLE_KEY=[GET_FROM_SUPABASE_DASHBOARD]
SUPABASE_BUCKET=invoices

# ===== AI SERVICES =====
# OpenAI (for embeddings and chat)
OPENAI_API_KEY=[GET_FROM_OPENAI_DASHBOARD]
EMBEDDING_MODEL=text-embedding-3-small
REFINER_MODEL=gpt-4o-mini

# Friendli AI (for VLM analysis)
FRIENDLI_TOKEN=[GET_FROM_FRIENDLI_DASHBOARD]
FRIENDLI_URL=https://api.friendli.ai/dedicated/v1/chat/completions
FRIENDLI_MODEL_ID=[YOUR_MODEL_ID]

# ===== ENVIRONMENT =====
ENVIRONMENT=production
PORT=8000
```

### Railway Deployment Steps

1. **Connect GitHub Repository**
   - Go to Railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

2. **Configure Service**
   - Service Name: `invoice-backend`
   - Root Directory: Leave as root (.)
   - Builder: Dockerfile (automatically detected)

3. **Add Environment Variables**
   - Click "Variables" tab
   - Add ALL variables from above
   - ⚠️ **CRITICAL:** Update DATABASE_URL with correct password

4. **Deploy**
   - Railway will automatically build using Dockerfile.backend
   - Wait for deployment to complete
   - **Copy the deployment URL** (e.g., `invoice-backend-production.up.railway.app`)

5. **Verify Deployment**
   ```bash
   curl https://[your-railway-url]/
   # Should return: {"message": "Hello from FastAPI + Supabase + HuggingFace VLM 🚀"}
   
   curl https://[your-railway-url]/docs
   # Should show FastAPI Swagger UI
   ```

### Railway-Specific Notes

- ✅ Railway automatically sets `$PORT` environment variable
- ✅ Health checks via root endpoint (`/`)
- ✅ Auto-restart on failure (max 10 retries)
- ⚠️ Use connection pooler for better database performance
- 💡 Consider upgrading to Railway Pro for better performance

---

## ▲ VERCEL DEPLOYMENT (Frontend)

### Configuration

```json
{
  "Framework": "Next.js",
  "Root Directory": "frontend-nextjs",
  "Build Command": "npm run build",
  "Output Directory": ".next",
  "Install Command": "npm install",
  "Node Version": "20.x"
}
```

### Environment Variables for Vercel

Add these in Vercel Dashboard → Settings → Environment Variables:

```bash
# ===== API CONFIGURATION =====
# ⚠️ UPDATE THIS AFTER RAILWAY DEPLOYMENT!
NEXT_PUBLIC_API_BASE_URL=https://[YOUR-RAILWAY-BACKEND-URL].up.railway.app

# ===== SUPABASE (PUBLIC KEYS ONLY) =====
NEXT_PUBLIC_SUPABASE_URL=https://pcktfzshbxaljkbedrar.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=[GET_ANON_KEY_FROM_SUPABASE]
```

### Vercel Deployment Steps

1. **Connect GitHub Repository**
   - Go to Vercel.com
   - Click "Add New Project"
   - Import from GitHub
   - Select your repository

2. **Configure Project**
   - Framework Preset: **Next.js** (auto-detected)
   - Root Directory: `frontend-nextjs`
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

3. **Add Environment Variables**
   - Click "Environment Variables"
   - Add the 3 variables above
   - **IMPORTANT:** Update `NEXT_PUBLIC_API_BASE_URL` with your Railway backend URL
   - Apply to: Production, Preview, Development

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - **Copy the deployment URL** (e.g., `invoice-app.vercel.app`)

5. **Verify Deployment**
   - Visit your Vercel URL
   - Should see the homepage with dark/light theme toggle
   - Check browser console for any API errors
   - Test upload functionality

### Vercel-Specific Notes

- ✅ Automatic HTTPS
- ✅ Global CDN deployment
- ✅ Preview deployments for each PR
- ⚠️ Only `NEXT_PUBLIC_*` variables are exposed to browser
- 💡 Standalone output mode enabled for optimal performance

---

## 🔒 SECURITY CHECKLIST

### Before Production Deployment

- [ ] **Update DATABASE_URL** with correct password
- [ ] **Remove CORS wildcard** (`"*"`) from backend/main.py
- [ ] **Replace with specific Vercel domain:**
  ```python
  allow_origins=[
      "https://your-app.vercel.app",
      "https://your-custom-domain.com",
  ]
  ```
- [ ] **Verify no private keys** in frontend .env.local
- [ ] **Enable Supabase RLS** (Row Level Security)
- [ ] **Test database connection** from Railway
- [ ] **Test API calls** from Vercel to Railway
- [ ] **Check Supabase usage limits**
- [ ] **Monitor OpenAI API costs**
- [ ] **Monitor Friendli AI usage**

### Environment Variables Security

| Variable | Location | Type | Exposed to Browser? |
|----------|----------|------|---------------------|
| DATABASE_URL | Railway | Secret | ❌ No |
| SUPABASE_SERVICE_ROLE_KEY | Railway | Secret | ❌ No |
| OPENAI_API_KEY | Railway | Secret | ❌ No |
| FRIENDLI_TOKEN | Railway | Secret | ❌ No |
| NEXT_PUBLIC_API_BASE_URL | Vercel | Public | ✅ Yes |
| NEXT_PUBLIC_SUPABASE_URL | Vercel | Public | ✅ Yes |
| NEXT_PUBLIC_SUPABASE_KEY | Vercel | Public (anon key) | ✅ Yes |

---

## 🔗 API ENDPOINTS

Your backend exposes these endpoints (verify after deployment):

```
GET  /                           # Health check
GET  /docs                       # Swagger UI
POST /upload/                    # Upload invoice to Supabase
POST /vlm/analyze                # Analyze invoice with Friendli VLM
POST /chat/ask                   # Chat with invoices (RAG)
GET  /dashboard/stats            # Get dashboard statistics
GET  /invoices/all               # Get all invoices
GET  /invoices/{id}              # Get specific invoice
DELETE /invoices/{id}            # Delete invoice
```

---

## 📦 DEPENDENCIES

### Backend (requirements.txt)

✅ All dependencies pinned to specific versions
✅ Compatible versions verified:
- fastapi==0.118.0
- uvicorn==0.37.0
- supabase==2.9.0
- openai==1.54.0
- httpx==0.27.2 (compatible with openai)
- sentence-transformers==5.1.1

### Frontend (package.json)

✅ All dependencies pinned
✅ Next.js 14.2.3 with React 18
✅ TypeScript enabled
✅ Tailwind CSS + Radix UI components

---

## 🧪 TESTING DEPLOYMENT

### 1. Test Backend on Railway

```bash
# Health check
curl https://[your-railway-url]/

# API documentation
open https://[your-railway-url]/docs

# Test upload endpoint (requires file)
curl -X POST https://[your-railway-url]/upload/ -F "file=@test-invoice.jpg"
```

### 2. Test Frontend on Vercel

1. Visit your Vercel URL
2. Open Browser DevTools → Console
3. Check for errors
4. Test pages:
   - `/` - Homepage
   - `/upload` - Upload invoice
   - `/dashboard` - View statistics
   - `/invoices` - List invoices
   - `/chat` - Chat with invoices

### 3. Test Integration

1. Upload an invoice via Vercel frontend
2. Check if it appears in dashboard
3. Try chatting about the invoice
4. Verify data persists in Supabase

---

## 🐛 COMMON DEPLOYMENT ISSUES

### Issue 1: Database Connection Failed

**Error:** `password authentication failed for user "postgres"`

**Solution:**
1. Get correct password from Supabase Dashboard
2. URL-encode special characters (@ → %40)
3. Update DATABASE_URL in Railway
4. Consider using connection pooler:
   ```
   postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
   ```

### Issue 2: Frontend Can't Connect to Backend

**Error:** `Failed to fetch` or CORS errors in browser console

**Solutions:**
1. Verify `NEXT_PUBLIC_API_BASE_URL` points to Railway URL
2. Check Railway backend is running
3. Verify CORS in backend/main.py includes Vercel domain
4. Redeploy Vercel after updating environment variables

### Issue 3: Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solutions:**
- Backend: Ensure requirements.txt is complete
- Frontend: Run `npm install` and commit package-lock.json
- Railway: Check build logs for pip install errors
- Vercel: Check build logs for npm install errors

### Issue 4: Build Timeout on Vercel

**Solutions:**
- Ensure `output: 'standalone'` in next.config.js ✅ (already configured)
- Check for large dependencies
- Consider upgrading Vercel plan

---

## 📝 DEPLOYMENT SEQUENCE

Follow this order for successful deployment:

1. ✅ **Fix Database Password**
   - Get correct password from Supabase
   - Update locally and test

2. ✅ **Deploy Backend to Railway**
   - Connect repository
   - Add all environment variables
   - Deploy
   - Verify with `/docs` endpoint
   - **Save Railway URL**

3. ✅ **Deploy Frontend to Vercel**
   - Connect repository
   - Set root directory: `frontend-nextjs`
   - Add environment variables
   - **Update NEXT_PUBLIC_API_BASE_URL with Railway URL**
   - Deploy
   - Verify frontend loads

4. ✅ **Test Integration**
   - Upload invoice from Vercel
   - Check database in Supabase
   - Test all features

5. ✅ **Secure CORS**
   - Update backend/main.py
   - Replace `"*"` with Vercel domain
   - Redeploy Railway

6. ✅ **Monitor**
   - Check Railway logs
   - Check Vercel analytics
   - Monitor API usage (OpenAI, Friendli)
   - Monitor database connections

---

## 🎯 FINAL CHECKLIST

### Pre-Deployment

- [ ] Database password verified and correct
- [ ] All environment variables documented
- [ ] CORS configured for production
- [ ] Dependencies up to date
- [ ] Local testing completed

### Railway (Backend)

- [ ] GitHub repository connected
- [ ] All environment variables added
- [ ] DATABASE_URL with correct password
- [ ] Dockerfile.backend detected
- [ ] Deployment successful
- [ ] `/docs` endpoint accessible
- [ ] Railway URL saved

### Vercel (Frontend)

- [ ] GitHub repository connected
- [ ] Root directory set to `frontend-nextjs`
- [ ] All NEXT_PUBLIC_* variables added
- [ ] NEXT_PUBLIC_API_BASE_URL points to Railway
- [ ] Deployment successful
- [ ] Frontend loads without errors
- [ ] Vercel URL saved

### Post-Deployment

- [ ] Upload feature works
- [ ] Invoice analysis works
- [ ] Dashboard displays data
- [ ] Chat feature works
- [ ] Database persists data
- [ ] No CORS errors
- [ ] CORS wildcard removed
- [ ] Monitoring enabled

---

## 📊 ESTIMATED COSTS

### Railway (Backend)
- **Hobby Plan:** $5/month
- **Pro Plan:** $20/month (recommended)
- Includes: 512MB RAM, shared CPU

### Vercel (Frontend)
- **Hobby:** Free (100GB bandwidth)
- **Pro:** $20/month (1TB bandwidth)

### Supabase
- **Free Tier:** 500MB database, 1GB file storage
- **Pro:** $25/month (8GB database, 100GB storage)

### External APIs
- **OpenAI:** Pay-per-use (~$0.0002/request for embeddings)
- **Friendli AI:** According to your plan

**Total Estimated:** $25-70/month depending on usage

---

## 🆘 SUPPORT RESOURCES

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Next.js Deployment: https://nextjs.org/docs/deployment
- Supabase Docs: https://supabase.com/docs

---

**Last Updated:** 2025-01-08  
**Project Version:** 1.0.0  
**Status:** ⚠️ Ready for deployment (fix database password first)

