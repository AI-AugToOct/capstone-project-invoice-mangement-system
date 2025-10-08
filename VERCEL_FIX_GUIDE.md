# 🔧 Fix Vercel Deployment Failure

## 🚨 Issue: Build Failed with "npm run build exited with 1"

---

## ✅ **Solution: Configure Root Directory in Vercel**

### **Step 1: Go to Vercel Dashboard**
1. Open your deployment: https://vercel.com/dashboard
2. Click on your project: `capstone-project-invoice-mangement-system`
3. Click **"Settings"** (top menu)

### **Step 2: Set Root Directory** ⚠️ **CRITICAL**
1. In Settings, click **"General"** (left sidebar)
2. Scroll down to **"Root Directory"**
3. Click **"Edit"**
4. Enter: `frontend-nextjs`
5. Click **"Save"**

### **Step 3: Set Environment Variable**
1. In Settings, click **"Environment Variables"** (left sidebar)
2. Click **"Add New"**
3. Add this variable:
   ```
   Name:  NEXT_PUBLIC_API_BASE_URL
   Value: https://capstone-project-invoice-mangement-system-production.up.railway.app
   ```
4. Check **"Production"**, **"Preview"**, and **"Development"**
5. Click **"Save"**

### **Step 4: Redeploy**
1. Go to **"Deployments"** tab
2. Click the **"..."** menu on the latest deployment
3. Click **"Redeploy"**
4. Make sure "Use existing Build Cache" is **UNCHECKED**
5. Click **"Redeploy"**

---

## 🔍 **If Build Still Fails, Check These:**

### **1. Framework Preset**
Settings → General → Framework Preset → Should be **"Next.js"**

### **2. Build Command** (should be auto-detected)
```
npm run build
```

### **3. Output Directory** (should be auto-detected)
```
.next
```

### **4. Install Command** (should be auto-detected)
```
npm install
```

### **5. Node.js Version**
Settings → General → Node.js Version → **20.x** (recommended)

---

## 📋 **Complete Checklist**

- [ ] Root Directory set to `frontend-nextjs`
- [ ] Environment variable `NEXT_PUBLIC_API_BASE_URL` added
- [ ] Framework Preset is "Next.js"
- [ ] Redeployed without cache
- [ ] Deploying from `main` branch
- [ ] Latest commit `821fb16` is deployed

---

## 🆘 **Still Getting Errors?**

### **Show Me the Complete Error Log:**

1. In Vercel, click on the failed deployment
2. Click **"Build Logs"**
3. Scroll to the **bottom** where the error appears
4. Copy the **last 50-100 lines** (especially after "next build")
5. Share the error message

Common errors to look for:
```
Error: Cannot find module...
Type error: ...
Module not found: Can't resolve...
```

---

## 🎯 **Expected Successful Build Output**

When configured correctly, you should see:
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (8/8)
✓ Finalizing page optimization

Route (app)                              Size     First Load JS
┌ ○ /                                    4.71 kB         151 kB
├ ○ /chat                                10.4 kB         291 kB
├ ○ /dashboard                           118 kB          281 kB
└ ○ /upload                              10.7 kB         148 kB

○  (Static)  prerendered as static content

Build completed successfully
```

---

## 🚀 **Quick Fix Script (Alternative)**

If settings UI doesn't work, create `vercel.json` in the **repository root**:

```json
{
  "buildCommand": "cd frontend-nextjs && npm install && npm run build",
  "outputDirectory": "frontend-nextjs/.next",
  "framework": "nextjs",
  "installCommand": "cd frontend-nextjs && npm install"
}
```

Then commit and push:
```bash
git add vercel.json
git commit -m "fix: add Vercel configuration"
git push origin main
```

---

## ✅ **After Successful Deployment**

Your frontend will be live at:
```
https://your-project-name.vercel.app
```

Test these pages:
- `/` - Home page
- `/upload` - Upload invoices
- `/dashboard` - View analytics
- `/chat` - AI chat
- `/invoices` - Invoice list

All should connect to your Railway backend! 🎉

