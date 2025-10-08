# ⚡ QUICK DEPLOY REFERENCE

## 🚂 Railway (Backend) - Copy & Paste

### Project Settings
```
Service Name:      invoice-backend
Root Directory:    . (leave empty/root)
Builder:          Dockerfile
Start Command:     (auto-detected from railway.json)
```

### Environment Variables
```bash
DATABASE_URL=postgresql://postgres:[FIX_PASSWORD]@db.pcktfzshbxaljkbedrar.supabase.co:5432/postgres
SUPABASE_URL=https://pcktfzshbxaljkbedrar.supabase.co
SUPABASE_KEY=[GET_FROM_SUPABASE_DASHBOARD]
SUPABASE_SERVICE_ROLE_KEY=[GET_FROM_SUPABASE_DASHBOARD]
SUPABASE_BUCKET=invoices
OPENAI_API_KEY=[GET_FROM_OPENAI_DASHBOARD]
EMBEDDING_MODEL=text-embedding-3-small
REFINER_MODEL=gpt-4o-mini
FRIENDLI_TOKEN=[GET_FROM_FRIENDLI_DASHBOARD]
FRIENDLI_URL=https://api.friendli.ai/dedicated/v1/chat/completions
FRIENDLI_MODEL_ID=[YOUR_MODEL_ID]
ENVIRONMENT=production
PORT=8000
```

---

## ▲ Vercel (Frontend) - Copy & Paste

### Project Settings
```
Framework Preset:     Next.js
Root Directory:       frontend-nextjs
Build Command:        npm run build (default)
Output Directory:     .next (default)
Install Command:      npm install (default)
Node Version:         20.x
```

### Environment Variables
```bash
NEXT_PUBLIC_API_BASE_URL=https://[YOUR-RAILWAY-URL].up.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://pcktfzshbxaljkbedrar.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=[GET_ANON_KEY_FROM_SUPABASE]
```

**⚠️ Important:** Update `NEXT_PUBLIC_API_BASE_URL` after Railway deployment!

---

## 🔄 Deployment Order

1. ✅ Deploy Backend to Railway **FIRST**
2. ✅ Copy Railway URL
3. ✅ Deploy Frontend to Vercel with Railway URL
4. ✅ Test integration

---

## ✅ Success Checklist

### Railway Deployed Successfully When:
- [ ] Build completes without errors
- [ ] `https://[railway-url]/` returns JSON message
- [ ] `https://[railway-url]/docs` shows Swagger UI
- [ ] No database connection errors in logs

### Vercel Deployed Successfully When:
- [ ] Build completes without errors
- [ ] Homepage loads at `https://[vercel-url]`
- [ ] No errors in browser console (F12)
- [ ] Upload page loads
- [ ] Dashboard page loads

### Full Integration Working When:
- [ ] Can upload invoice from Vercel frontend
- [ ] Invoice appears in dashboard
- [ ] Can chat about invoices
- [ ] Data persists in Supabase

---

## 🐛 Quick Fixes

**Database Error?**
→ Fix DATABASE_URL password in Railway

**Frontend Can't Connect?**
→ Update NEXT_PUBLIC_API_BASE_URL in Vercel

**CORS Error?**
→ Add Vercel domain to backend/main.py CORS

**Build Failing?**
→ Check Railway/Vercel build logs

