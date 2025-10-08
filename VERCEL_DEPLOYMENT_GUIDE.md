# 🚀 Vercel Frontend Deployment Guide

## ✅ Status: Backend is Live on Railway!

**Backend URL:** `https://capstone-project-invoice-mangement-system-production.up.railway.app`

---

## 📋 Step-by-Step Vercel Deployment

### **Step 1: Push Latest Changes to GitHub**

```bash
git add .
git commit -m "✅ Backend deployed successfully on Railway"
git push origin main
```

---

### **Step 2: Login to Vercel**

1. Go to: https://vercel.com/
2. Sign in with GitHub
3. Click "Add New..." → "Project"

---

### **Step 3: Import Your Repository**

1. Select: `capstone-project-invoice-mangement-system`
2. Click "Import"

---

### **Step 4: Configure Project Settings**

#### **Framework Preset:**
- Select: `Next.js`

#### **Root Directory:**
- Change to: `frontend-nextjs`
- Click "Edit" → Select `frontend-nextjs` folder

#### **Build Settings (Auto-detected):**
```
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

---

### **Step 5: Add Environment Variables** ⚠️ **IMPORTANT!**

Click "Environment Variables" and add these **EXACTLY**:

#### **Variable 1:**
```
Name:  NEXT_PUBLIC_API_BASE_URL
Value: https://capstone-project-invoice-mangement-system-production.up.railway.app
```

#### **Variable 2:**
```
Name:  NEXT_PUBLIC_SUPABASE_URL
Value: https://pcktfzshbxaljkbedrar.supabase.co
```

#### **Variable 3:**
```
Name:  NEXT_PUBLIC_SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBja3RmenNoYnhhbGprYmVkcmFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUxNTY5NzIsImV4cCI6MjA1MDczMjk3Mn0.vxTf4MqT8rShLIzKOSjj2XZHEP_8ohLGfZIXYhg1wtc
```

---

### **Step 6: Deploy!**

1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Click on the deployed URL

---

## 🎯 Expected Result

Your frontend will be live at: `https://your-project-name.vercel.app`

You should see:
- ✅ Dashboard page loads
- ✅ Login/Register pages work (Supabase Auth)
- ✅ Invoice upload works (connects to Railway backend)
- ✅ Chat and analysis features work

---

## ⚠️ Update CORS in Backend (After Vercel Deploy)

Once you get your Vercel URL (e.g., `https://invoice-app.vercel.app`), you need to update Railway environment variables:

### **On Railway Dashboard:**

Add this environment variable:
```
Name:  FRONTEND_URL
Value: https://your-vercel-url.vercel.app
```

Then redeploy backend to apply CORS changes.

**OR** the backend already has wildcard CORS enabled for Vercel (`https://*.vercel.app`), so it should work immediately! ✅

---

## 🧪 Test Your Deployed App

### **1. Test Frontend:**
```
https://your-vercel-url.vercel.app
```

### **2. Test Backend API from Frontend:**
Open browser console and run:
```javascript
fetch('https://capstone-project-invoice-mangement-system-production.up.railway.app/')
  .then(r => r.json())
  .then(console.log)
```

Should return:
```json
{
  "status": "✅ Smart Invoice Analyzer is running successfully!"
}
```

---

## 🎉 Deployment Complete!

**Backend:** ✅ Railway → https://capstone-project-invoice-mangement-system-production.up.railway.app

**Frontend:** 🚀 Vercel → (Your URL after deployment)

**Database:** ✅ Supabase → https://pcktfzshbxaljkbedrar.supabase.co

**AI Models:** ✅ Friendli AI + OpenAI

---

## 📝 Notes

- Frontend environment variables MUST start with `NEXT_PUBLIC_`
- Never commit `.env.local` to Git (it's already in .gitignore)
- Backend CORS already allows `*.vercel.app` domains
- All secrets are secure (backend keys are in Railway, not in frontend)

---

## 🆘 Troubleshooting

### **Issue 1: API Calls Fail (CORS Error)**

**Solution:** Check that `NEXT_PUBLIC_API_BASE_URL` in Vercel matches Railway URL exactly (no trailing slash)

### **Issue 2: Supabase Auth Doesn't Work**

**Solution:** 
1. Go to Supabase Dashboard → Settings → API
2. Add your Vercel URL to "Site URL" and "Redirect URLs"

### **Issue 3: Build Fails on Vercel**

**Solution:** Check `package.json` in `frontend-nextjs/` has all dependencies

---

**Good luck! 🚀**

