# 🚂 Railway Setup Guide - Step by Step

## 📋 Settings to Configure

### 1️⃣ **Source Repo**
```
Repository: AI-AugToOct/capstone-project-invoice-mangement-system
Branch: main
```

### 2️⃣ **Root Directory** 
```
LEAVE EMPTY (or set to: /)
```
**Important:** Don't set it to `backend` - we'll use Dockerfile instead!

---

### 3️⃣ **Networking**
```
Public Networking: ✅ Enabled
Domain: capstone-project-invoice-mangement-system-production.up.railway.app
Port: 8000
```

---

### 4️⃣ **Build Settings**

#### Option A: Using Dockerfile (RECOMMENDED) ⭐
```
Builder: Dockerfile

Dockerfile Path: Dockerfile.backend

Build Command: (leave empty)

Watch Paths: (leave empty)
```

#### Option B: Using Nixpacks (Alternative)
```
Builder: Nixpacks

Build Command: pip install -r requirements.txt

Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Watch Paths: (leave empty)
```

---

### 5️⃣ **Deploy Settings**
```
Start Command: (leave empty if using Dockerfile)

OR if using Nixpacks:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

### 6️⃣ **Regions**
```
Region: EU West (Amsterdam, Netherlands)
Replicas: 1
```

---

### 7️⃣ **Restart Policy**
```
Policy: On Failure
Max restart retries: 10
```

---

### 8️⃣ **Railway Config File**
```
✅ We already have railway.json in the repo
This will be automatically detected
```

---

## 🔑 **Environment Variables (CRITICAL!)**

Go to: **Variables** tab in Railway dashboard

Add these variables one by one:

### Database
```bash
DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@db.pcktfzshbxaljkbedrar.supabase.co:5432/postgres
```
⚠️ Replace `[YOUR_PASSWORD]` with your actual Supabase password
⚠️ If password has `@`, encode it as `%40`

### Supabase
```bash
SUPABASE_URL=https://pcktfzshbxaljkbedrar.supabase.co
SUPABASE_KEY=[YOUR_ANON_KEY]
SUPABASE_SERVICE_ROLE_KEY=[YOUR_SERVICE_ROLE_KEY]
SUPABASE_BUCKET=invoices
```

### AI Services
```bash
OPENAI_API_KEY=[YOUR_OPENAI_KEY]
EMBEDDING_MODEL=text-embedding-3-small
REFINER_MODEL=gpt-4o-mini
FRIENDLI_TOKEN=[YOUR_FRIENDLI_TOKEN]
FRIENDLI_URL=https://api.friendli.ai/dedicated/v1/chat/completions
FRIENDLI_MODEL_ID=[YOUR_MODEL_ID]
```

### Environment
```bash
ENVIRONMENT=production
PORT=8000
```

---

## 🎯 **Quick Fix for Current Error:**

Your build is failing because of wrong paths. Here's what to do:

### Step 1: Change Root Directory
```
Root Directory: (LEAVE EMPTY or delete "backend")
```

### Step 2: Change Builder
```
Builder: Dockerfile
Dockerfile Path: Dockerfile.backend
```

### Step 3: Clear Commands
```
Build Command: (delete everything, leave empty)
Start Command: (delete everything, leave empty)
```

### Step 4: Add Environment Variables
Go to Variables tab and add ALL the variables listed above.

### Step 5: Re-deploy
Click "Deploy" button again.

---

## ✅ **Expected Result:**

After fixing these settings, you should see:
```
✅ Build image (success)
✅ Deploy (success)
✅ Service available at: https://capstone-project-invoice-mangement-system-production.up.railway.app
```

---

## 🔧 **If Still Failing:**

Check the build logs for specific errors. Common issues:
- Missing environment variables
- Wrong database password
- Missing dependencies

---

## 📞 **Need Help?**

Check the Railway logs and share the error message for specific troubleshooting.

