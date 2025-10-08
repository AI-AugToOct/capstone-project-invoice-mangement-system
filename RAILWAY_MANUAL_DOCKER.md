# 🚂 Railway Manual Docker Setup (للحسابات المجانية)

## ✅ **الملفات جاهزة في المشروع:**

```
✓ railway.json         (يجبر Railway على استخدام Docker)
✓ Dockerfile.backend   (تعليمات البناء)
```

---

## 📋 **الإعدادات الصحيحة في Railway Dashboard:**

### 1️⃣ **Root Directory**
```
(LEAVE EMPTY - لا تضع شيء)
```
⚠️ **مهم جداً**: احذف أي شيء موجود هنا (مثل "backend")

---

### 2️⃣ **Builder**
```
اختر: Railpack (أو أي خيار متاح)
```
لا تقلق - ملف `railway.json` سيجبره على استخدام Docker تلقائياً 👍

---

### 3️⃣ **Build Command**
```
(LEAVE EMPTY - احذف كل شيء)
```

---

### 4️⃣ **Start Command**
```
(LEAVE EMPTY - احذف كل شيء)
```

---

### 5️⃣ **Watch Paths**
```
(LEAVE EMPTY)
```

---

## 🔑 **Environment Variables (الأهم!)**

اذهب إلى تبويب **Variables** واضغط **"New Variable"**

أضف هذه المتغيرات **واحدة واحدة**:

### 📊 Database
```
Variable Name: DATABASE_URL
Value: postgresql://postgres:YOUR_PASSWORD@db.pcktfzshbxaljkbedrar.supabase.co:5432/postgres
```
⚠️ استبدل `YOUR_PASSWORD` بكلمة المرور الحقيقية من Supabase

---

### 🗄️ Supabase
```
Variable Name: SUPABASE_URL
Value: https://pcktfzshbxaljkbedrar.supabase.co
```

```
Variable Name: SUPABASE_KEY
Value: [احصل عليه من Supabase → Settings → API → anon public]
```

```
Variable Name: SUPABASE_SERVICE_ROLE_KEY
Value: [احصل عليه من Supabase → Settings → API → service_role]
```

```
Variable Name: SUPABASE_BUCKET
Value: invoices
```

---

### 🤖 OpenAI
```
Variable Name: OPENAI_API_KEY
Value: [احصل عليه من https://platform.openai.com/api-keys]
```

```
Variable Name: EMBEDDING_MODEL
Value: text-embedding-3-small
```

```
Variable Name: REFINER_MODEL
Value: gpt-4o-mini
```

---

### 🧠 Friendli AI
```
Variable Name: FRIENDLI_TOKEN
Value: [احصل عليه من Friendli Dashboard]
```

```
Variable Name: FRIENDLI_URL
Value: https://api.friendli.ai/dedicated/v1/chat/completions
```

```
Variable Name: FRIENDLI_MODEL_ID
Value: [احصل عليه من Friendli Dashboard]
```

---

### ⚙️ Environment
```
Variable Name: ENVIRONMENT
Value: production
```

```
Variable Name: PORT
Value: 8000
```

---

## 🚀 **بعد إضافة كل المتغيرات:**

1. اضغط على **"Deploy"**
2. انتظر بناء الـ Docker image (قد يستغرق 2-5 دقائق)
3. راقب الـ **Build Logs**

---

## ✅ **النتيجة المتوقعة:**

```
✓ Building with Dockerfile
✓ Step 1/9 : FROM python:3.12-slim
✓ Step 2/9 : WORKDIR /app
✓ Step 3/9 : RUN apt-get update...
✓ Step 4/9 : COPY requirements.txt .
✓ Step 5/9 : RUN pip install...
✓ Step 6/9 : COPY backend/ ./backend/
✓ Step 7/9 : ENV PYTHONPATH=/app
✓ Step 8/9 : EXPOSE 8000
✓ Step 9/9 : CMD ["uvicorn"...]
✓ Successfully built
✓ Deploy successful
```

---

## 🌐 **اختبار الـ API:**

بعد نجاح الـ Deploy، افتح:

```
https://capstone-project-invoice-mangement-system-production.up.railway.app/docs
```

يجب أن تشاهد واجهة Swagger UI 🎉

---

## 🆘 **إذا فشل البناء:**

### خطأ: "No Dockerfile found"
✅ **الحل**: تأكد أن Root Directory فارغ تماماً

### خطأ: "Module not found"
✅ **الحل**: تحقق من أن جميع المكتبات في `requirements.txt`

### خطأ: "Database connection failed"
✅ **الحل**: راجع `DATABASE_URL` وتأكد من كلمة المرور

### خطأ: "Port already in use"
✅ **الحل**: Railway يوفر PORT تلقائياً، لا تحتاج تغيير شيء

---

## 📝 **ملخص سريع:**

| الإعداد | القيمة |
|---------|--------|
| Root Directory | **(فارغ)** |
| Builder | Railpack (أي خيار) |
| Build Command | **(فارغ)** |
| Start Command | **(فارغ)** |
| Variables | **13 متغير** |

---

## 🎯 **الخطوة التالية:**

بعد نجاح الـ deploy، احفظ رابط Railway:
```
https://capstone-project-invoice-mangement-system-production.up.railway.app
```

ستحتاجه لإعداد Vercel للـ frontend! 🚀

