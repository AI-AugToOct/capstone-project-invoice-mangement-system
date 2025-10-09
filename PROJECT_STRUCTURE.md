# 📁 هيكلة مشروع مُـــفـــــوْتِـــــر

## 📋 نظرة عامة

مشروع **مُـــفـــــوْتِـــــر** هو نظام ذكي متكامل لإدارة الفواتير باستخدام الذكاء الاصطناعي. يتكون من جزئين رئيسيين:

- **Backend**: Python (FastAPI) - يتعامل مع قاعدة البيانات والذكاء الاصطناعي
- **Frontend**: Next.js 14 (React) - واجهة المستخدم

---

## 🗂️ الهيكل الكامل للمشروع

```
capstone-project-invoice-mangement-system/
│
├── 📂 backend/                    # الخادم الخلفي (Backend)
│   ├── 📂 models/                 # نماذج قاعدة البيانات (Database Models)
│   ├── 📂 routers/                # مسارات API (Endpoints)
│   ├── 📂 schemas/                # مخططات البيانات (Data Schemas)
│   ├── database.py                # إعدادات قاعدة البيانات
│   ├── main.py                    # نقطة البدء للخادم
│   ├── utils.py                   # وظائف مساعدة
│   └── requirements.txt           # المكتبات المطلوبة
│
├── 📂 frontend-nextjs/            # واجهة المستخدم (Frontend)
│   ├── 📂 app/                    # صفحات التطبيق
│   ├── 📂 components/             # مكونات React قابلة لإعادة الاستخدام
│   ├── 📂 lib/                    # وظائف مساعدة
│   ├── 📂 public/                 # الملفات الثابتة (صور، أيقونات)
│   ├── package.json               # إعدادات Node.js
│   └── next.config.js             # إعدادات Next.js
│
├── 📂 venv/                       # البيئة الافتراضية لـ Python
├── .gitignore                     # ملفات مستثناة من Git
├── README.md                      # دليل المشروع الرئيسي
└── docker-compose.yml             # إعدادات Docker

```

---

## 🔷 Backend (الخادم الخلفي)

### 📂 `backend/`

#### الملفات الرئيسية:

| الملف | الوصف |
|-------|-------|
| **`main.py`** | 🚀 **نقطة البدء الرئيسية**<br>- يشغل خادم FastAPI<br>- يربط جميع الـ Routers<br>- يضبط CORS للتواصل مع Frontend |
| **`database.py`** | 🗄️ **إعدادات قاعدة البيانات**<br>- الاتصال بـ PostgreSQL<br>- إنشاء جلسات قاعدة البيانات<br>- إعداد SQLAlchemy |
| **`utils.py`** | 🛠️ **وظائف مساعدة**<br>- توليد Embeddings للبحث الدلالي<br>- وظائف مشتركة عبر المشروع |
| **`requirements.txt`** | 📦 **قائمة المكتبات**<br>- FastAPI, SQLAlchemy, PostgreSQL<br>- OpenAI, Sentence-Transformers<br>- PyMuPDF للـ PDF |

---

### 📂 `backend/models/` - نماذج قاعدة البيانات

| الملف | الوصف |
|-------|-------|
| **`invoice_model.py`** | 🧾 **نموذج الفواتير**<br>- جدول `invoices` في قاعدة البيانات<br>- يحتوي: رقم الفاتورة، التاريخ، المتجر، المبلغ، الضريبة، إلخ |
| **`item_model.py`** | 🛒 **نموذج المشتريات**<br>- جدول `items` في قاعدة البيانات<br>- يحتوي: وصف المنتج، الكمية، السعر، المجموع |
| **`embedding_model.py`** | 🧠 **نموذج Embeddings**<br>- جدول `embeddings` للبحث الدلالي<br>- يخزن vectors للبحث الذكي باستخدام AI |

---

### 📂 `backend/routers/` - مسارات API

| الملف | المسار | الوصف |
|-------|--------|-------|
| **`upload.py`** | `/upload/` | 📤 **رفع الصور**<br>- يرفع الصور/PDF إلى Supabase Storage<br>- يحول PDF إلى صورة تلقائياً |
| **`vlm.py`** | `/vlm/` | 🤖 **تحليل الفواتير بالـ AI**<br>- `/analyze-only`: يحلل بدون حفظ (للمراجعة)<br>- `/analyze`: يحلل ويحفظ في قاعدة البيانات<br>- يستخدم FriendliAI VLM (Qwen2.5) |
| **`invoices.py`** | `/invoices/` | 🗂️ **إدارة الفواتير**<br>- `/save-analyzed`: حفظ بيانات معدلة<br>- `GET /`: استرجاع كل الفواتير<br>- `DELETE /{id}`: حذف فاتورة |
| **`items.py`** | `/items/` | 🛍️ **إدارة المشتريات**<br>- `POST /`: إضافة منتج<br>- `GET /`: استرجاع المنتجات |
| **`dashboard.py`** | `/dashboard/` | 📊 **البيانات التحليلية**<br>- إحصائيات المصروفات<br>- تحليل حسب الفئات والتواريخ |
| **`chat.py`** | `/chat/` | 💬 **المساعد الذكي**<br>- يجيب على أسئلة المستخدم عن الفواتير<br>- يستخدم RAG (البحث الدلالي + OpenAI) |

---

### 📂 `backend/schemas/` - مخططات البيانات

| الملف | الوصف |
|-------|-------|
| **`invoice_schema.py`** | ✅ **مخطط بيانات الفاتورة**<br>- يحدد شكل البيانات المرسلة/المستقبلة<br>- Validation باستخدام Pydantic |
| **`item_schema.py`** | ✅ **مخطط بيانات المشتريات**<br>- يحدد شكل بيانات المنتجات |

---

## 🔶 Frontend (واجهة المستخدم)

### 📂 `frontend-nextjs/`

#### الملفات الرئيسية:

| الملف | الوصف |
|-------|-------|
| **`package.json`** | 📦 **إعدادات المشروع**<br>- Next.js, React, Tailwind CSS<br>- Framer Motion للـ Animations<br>- Shadcn/ui للمكونات الجاهزة |
| **`next.config.js`** | ⚙️ **إعدادات Next.js**<br>- ضبط الصور المسموحة (Supabase)<br>- Standalone output للـ Deployment |
| **`tailwind.config.ts`** | 🎨 **إعدادات Tailwind CSS**<br>- الألوان المخصصة<br>- إعدادات الـ Dark Mode |
| **`tsconfig.json`** | 📝 **إعدادات TypeScript**<br>- قواعد TypeScript |

---

### 📂 `frontend-nextjs/app/` - الصفحات

#### الملفات الأساسية:

| الملف | الوصف |
|-------|-------|
| **`layout.tsx`** | 🏗️ **Layout الرئيسي**<br>- Navbar ثابت<br>- Footer<br>- Theme Provider (Dark Mode)<br>- خطوط Cairo العربية |
| **`page.tsx`** | 🏠 **الصفحة الرئيسية**<br>- Hero Section<br>- قسم "كيف يعمل النظام"<br>- قسم المميزات |
| **`globals.css`** | 🎨 **الأنماط العامة**<br>- Tailwind CSS<br>- تحسينات النصوص العربية<br>- Dark Mode Styles |

#### الصفحات الفرعية:

| المجلد/الملف | المسار | الوصف |
|-------------|--------|-------|
| **`upload/page.tsx`** | `/upload` | 📤 **صفحة رفع الفاتورة**<br>- رفع صورة أو PDF<br>- التقاط صورة بالكاميرا<br>- عرض البيانات للمراجعة والتعديل<br>- تأكيد الحفظ |
| **`invoices/page.tsx`** | `/invoices` | 📋 **صفحة الفواتير**<br>- عرض جميع الفواتير المحفوظة<br>- معاينة الصور<br>- حذف الفواتير |
| **`dashboard/page.tsx`** | `/dashboard` | 📊 **لوحة التحكم**<br>- رسوم بيانية للمصروفات<br>- إحصائيات شاملة<br>- تحليل حسب الفئات |
| **`chat/page.tsx`** | `/chat` | 💬 **صفحة الدردشة**<br>- مساعد ذكي عربي<br>- يجيب عن أسئلة الفواتير<br>- واجهة محادثة تفاعلية |

---

### 📂 `frontend-nextjs/components/` - المكونات

#### المكونات الرئيسية:

| الملف | الوصف |
|-------|-------|
| **`Navbar.tsx`** | 🧭 **شريط التنقل العلوي**<br>- اللوقو النصي<br>- روابط الصفحات<br>- زر Dark/Light Mode |
| **`MufawterLogo.tsx`** | ✨ **لوقو مُـــفـــــوْتِـــــر**<br>- نص عربي مع تدرج لوني<br>- Animations بـ Framer Motion<br>- أحجام متعددة (sm, md, lg, xl) |
| **`InvoiceResultCard.tsx`** | 🎴 **بطاقة عرض نتيجة الفاتورة**<br>- عرض البيانات المستخرجة<br>- الملخص المالي<br>- رؤية AI |
| **`CameraCapture.tsx`** | 📷 **مكون الكاميرا**<br>- التقاط صورة مباشرة<br>- معاينة الفيديو |
| **`ImageModal.tsx`** | 🖼️ **نافذة معاينة الصورة**<br>- عرض صورة الفاتورة بحجم كبير<br>- Zoom In/Out<br>- تحميل الصورة |
| **`ThemeToggle.tsx`** | 🌓 **زر تبديل الثيم**<br>- التبديل بين Dark/Light Mode |
| **`theme-provider.tsx`** | 🎨 **مزود الثيم**<br>- إدارة Dark Mode في كامل التطبيق |

---

### 📂 `frontend-nextjs/components/ui/` - مكونات UI

مكتبة مكونات قابلة لإعادة الاستخدام (مبنية على Shadcn/ui):

| الملف | الوصف |
|-------|-------|
| **`button.tsx`** | 🔘 أزرار بتصاميم متعددة |
| **`card.tsx`** | 🃏 بطاقات لعرض المحتوى |
| **`dialog.tsx`** | 💬 نوافذ منبثقة |
| **`input.tsx`** | ⌨️ حقول الإدخال |
| **`label.tsx`** | 🏷️ تسميات الحقول |
| **`progress.tsx`** | 📊 شريط التقدم |
| **`select.tsx`** | 📋 قوائم منسدلة |
| **`toast.tsx`** | 🔔 إشعارات منبثقة |
| **`scroll-area.tsx`** | 📜 منطقة تمرير مخصصة |

---

### 📂 `frontend-nextjs/lib/` - الوظائف المساعدة

| الملف | الوصف |
|-------|-------|
| **`utils.ts`** | 🛠️ **وظائف عامة**<br>- `cn()` للجمع بين class names<br>- `API_BASE` لرابط Backend |
| **`pdfUtils.ts`** | 📄 **وظائف PDF**<br>- معالجة ملفات PDF<br>- تحويل PDF إلى صورة |

---

### 📂 `frontend-nextjs/public/` - الملفات الثابتة

| نوع الملف | الوصف |
|-----------|-------|
| **`favicon.svg`** | أيقونة المتصفح |
| **`logo-*.svg`** | شعارات بنسخ Light/Dark |
| **`title-*.svg`** | عناوين الصفحات (SVG - قديمة، تم استبدالها بنص) |

---

## 🔧 ملفات الإعدادات

### ملفات Docker:

| الملف | الوصف |
|-------|-------|
| **`docker-compose.yml`** | 🐳 **Docker Compose للإنتاج**<br>- يشغل Backend + Frontend + PostgreSQL |
| **`docker-compose.dev.yml`** | 🛠️ **Docker للتطوير**<br>- بيئة تطوير محلية |
| **`Dockerfile.backend`** | 📦 بناء صورة Docker للـ Backend |
| **`Dockerfile.frontend`** | 📦 بناء صورة Docker للـ Frontend |
| **`docker-entrypoint.py`** | ⚡ سكريبت تشغيل Container |

---

### ملفات قاعدة البيانات:

| الملف | الوصف |
|-------|-------|
| **`database_setup.sql`** | 🗄️ **SQL لإنشاء الجداول**<br>- إنشاء قاعدة البيانات الأولية |
| **`run_migration.py`** | 🔄 **سكريبت الترحيل**<br>- تحديث قاعدة البيانات |

---

### ملفات التشغيل:

| الملف | الوصف |
|-------|-------|
| **`run.bat`** | ▶️ تشغيل المشروع على Windows |
| **`run.sh`** | ▶️ تشغيل المشروع على Linux/Mac |
| **`Makefile`** | ⚙️ أوامر Make لتسهيل التطوير |

---

### ملفات التوثيق:

| الملف | الوصف |
|-------|-------|
| **`README.md`** | 📖 دليل المشروع الرئيسي |
| **`VERCEL_DEPLOYMENT_GUIDE.md`** | 🚀 دليل رفع Frontend على Vercel |
| **`RAILWAY_SETUP_GUIDE.md`** | 🚂 دليل رفع Backend على Railway |
| **`SECURITY_CHECKLIST.md`** | 🔒 قائمة تدقيق الأمان |
| **`DEPLOYMENT_SUCCESS.md`** | ✅ ملخص النشر الناجح |

---

## 🔐 ملفات الأمان (مخفية)

هذه الملفات **لا تُرفع على Git** (محمية بـ `.gitignore`):

| الملف | الوصف |
|-------|-------|
| **`.env`** | 🔑 **متغيرات البيئة السرية**<br>- API Keys (OpenAI, Friendli, Supabase)<br>- Database URL<br>- Secret Keys |
| **`.env.local`** | 🔐 متغيرات البيئة المحلية (Frontend) |

---

## 📊 تدفق البيانات في المشروع

```
┌─────────────────────────────────────────────────────────────┐
│                      المستخدم (User)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Frontend (Next.js - Vercel)                    │
│  • Navbar, Pages, Components                                │
│  • Dark Mode, Animations                                    │
│  • مراجعة وتعديل البيانات                                  │
└────────────────────┬────────────────────────────────────────┘
                     │ API Calls
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI - Railway)                    │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐                │
│  │  Upload  │  │   VLM    │  │  Chat AI  │                │
│  │ Supabase │  │ Friendli │  │  OpenAI   │                │
│  └──────────┘  └──────────┘  └───────────┘                │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────┐                  │
│  │  Routers (Endpoints)                 │                  │
│  │  • /upload/ • /vlm/ • /invoices/     │                  │
│  │  • /dashboard/ • /chat/ • /items/    │                  │
│  └──────────────────────────────────────┘                  │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────┐                  │
│  │  Models & Database Layer             │                  │
│  │  • Invoice Model • Item Model        │                  │
│  │  • Embedding Model                   │                  │
│  └──────────────────────────────────────┘                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           PostgreSQL Database (Supabase)                    │
│  • جدول invoices (الفواتير)                                │
│  • جدول items (المشتريات)                                  │
│  • جدول embeddings (للبحث الذكي)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 رحلة رفع الفاتورة (User Journey)

```
1️⃣ المستخدم يرفع صورة/PDF
           ↓
2️⃣ Frontend → Backend: POST /upload/
           ↓
3️⃣ Backend يرفع على Supabase Storage
           ↓
4️⃣ Backend → VLM API: تحليل الصورة بالـ AI
           ↓
5️⃣ Backend → Frontend: إرجاع البيانات المستخرجة
           ↓
6️⃣ Frontend: عرض البيانات في حقول قابلة للتعديل
           ↓
7️⃣ المستخدم يراجع ويعدل البيانات
           ↓
8️⃣ المستخدم يضغط "تأكيد وحفظ"
           ↓
9️⃣ Frontend → Backend: POST /invoices/save-analyzed
           ↓
🔟 Backend يحفظ في PostgreSQL
           ↓
1️⃣1️⃣ Backend يولد Embedding للبحث الذكي
           ↓
1️⃣2️⃣ عرض النتيجة النهائية ✅
```

---

## 🛠️ التقنيات المستخدمة

### Backend:
- **FastAPI**: إطار Python سريع لبناء APIs
- **PostgreSQL**: قاعدة بيانات علائقية
- **SQLAlchemy**: ORM للتعامل مع قاعدة البيانات
- **OpenAI API**: للمساعد الذكي (Chat)
- **FriendliAI (Qwen2.5-VL)**: لتحليل الفواتير بالـ Vision AI
- **Sentence-Transformers**: لتوليد Embeddings
- **Supabase Storage**: لحفظ الصور
- **PyMuPDF**: لمعالجة ملفات PDF

### Frontend:
- **Next.js 14 (App Router)**: إطار React حديث
- **TypeScript**: للـ Type Safety
- **Tailwind CSS**: للتصميم السريع
- **Shadcn/ui**: مكتبة مكونات جاهزة
- **Framer Motion**: للـ Animations السلسة
- **Radix UI**: للمكونات التفاعلية (Dialog, Select)
- **React Hook Form**: لإدارة النماذج

### Deployment:
- **Vercel**: استضافة Frontend
- **Railway**: استضافة Backend
- **Supabase**: قاعدة البيانات + التخزين
- **Docker**: للحاويات (Containers)

---

## 📈 ميزات المشروع

### ✅ ميزات مكتملة:

- ✅ **رفع الفواتير**: صور، PDF، كاميرا
- ✅ **تحليل ذكي بالـ AI**: استخراج كل البيانات تلقائياً
- ✅ **مراجعة وتعديل**: قبل الحفظ
- ✅ **لوحة تحكم تحليلية**: رسوم بيانية وإحصائيات
- ✅ **مساعد ذكي عربي**: للإجابة عن الأسئلة
- ✅ **بحث دلالي**: RAG-based Search
- ✅ **Dark Mode**: افتراضي
- ✅ **متعدد اللغات**: عربي + إنجليزي
- ✅ **Responsive**: يعمل على جميع الأجهزة

---

## 🚀 كيفية تشغيل المشروع محلياً

### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend:
```bash
cd frontend-nextjs
npm install
npm run dev
```

---

## 📝 ملاحظات مهمة

1. **ملفات `.env` مخفية**: لا تُرفع على Git أبداً لحماية API Keys
2. **Dark Mode افتراضي**: تم تعيينه في `layout.tsx`
3. **اللوقو نصي**: تم استبدال الصور بنص عربي نظيف
4. **مراجعة البيانات**: ميزة جديدة تسمح بتعديل البيانات قبل الحفظ

---

## 🔗 روابط مفيدة

- **Frontend**: https://mufawter.vercel.app
- **Backend API Docs**: https://your-backend.railway.app/docs
- **GitHub Repo**: https://github.com/AI-AugToOct/capstone-project-invoice-mangement-system

---

**📅 آخر تحديث**: 2025-10-09  
**👨‍💻 تم تطويره بواسطة**: فريق مُـــفـــــوْتِـــــر

---

**🎉 مشروع تخرج متكامل واحترافي! نفتخر بما أنجزناه! 💪✨**

