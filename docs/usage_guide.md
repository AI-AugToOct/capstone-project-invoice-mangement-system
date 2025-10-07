# User Guide: Smart Invoice Analyzer (مُـفـــــوْتِــــر)

## 🎯 Overview

**مُـفـــــوْتِــــر** (Smart Invoice Analyzer) is an AI-powered invoice management system that helps you:

- 📤 Upload invoice images (drag-drop or camera capture)
- 🤖 Automatically extract data using AI (VLM)
- 📊 Visualize spending patterns with interactive charts
- 💬 Ask natural language questions about your invoices
- 📁 Organize and search all invoices in one place
- 📥 Download invoices as PDFs

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+** (for backend)
- **Node.js 18+** (for frontend)
- **Supabase Account** (free tier works)
- **Hugging Face API Token** (free)

### Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd capstone-project-invoice-mangement-system
```

#### 2. Setup Backend

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

#### 3. Setup Frontend

```bash
cd frontend-nextjs
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with API URL
```

#### 4. Database Setup

1. Create Supabase project
2. Run SQL migration:
```sql
-- See database_setup.sql
CREATE TABLE invoices (...);
CREATE TABLE invoice_embeddings (...);
CREATE TABLE items (...);
```

3. Create storage bucket named `invoices`
4. Make bucket public (see `supabase_storage_policy.sql`)

#### 5. Run Application

**Terminal 1 (Backend)**:
```bash
cd backend
uvicorn main:app --reload
```
→ Runs on `http://127.0.0.1:8000`

**Terminal 2 (Frontend)**:
```bash
cd frontend-nextjs
npm run dev
```
→ Runs on `http://localhost:3000`

---

## 📖 Step-by-Step Walkthrough

### 🏠 1. Home Page

When you open the application, you'll see:

- **Hero Section**: Brand name and tagline
- **Features**: Overview of system capabilities
- **Call-to-Action**: "ابدأ الآن مجاناً" button

**Actions**:
- Click "ابدأ الآن مجاناً" → Go to Upload page
- Click "شاهد التحليلات" → Go to Dashboard
- Use navigation bar to explore pages

---

### 📤 2. Upload Invoice Page

**Path**: `/upload`

#### Option A: Upload Image File

1. **Click "اختر ملف"** or drag-and-drop image
2. **Preview** appears
3. **Click "رفع وتحليل الفاتورة"**
4. **Progress bar** shows:
   - "جاري رفع الصورة..." (0-50%)
   - "جاري التحليل..." (50-100%)
5. **Results** display automatically

#### Option B: Capture from Camera

1. **Click "📷 التقاط من الكاميرا"**
2. **Allow camera access** (browser prompt)
3. **Point camera** at invoice
4. **Click "التقاط صورة"**
5. **Review photo**
6. **Click "استخدام الصورة"**
7. **Click "رفع وتحليل الفاتورة"**

#### Understanding Results

After analysis completes, you'll see:

**Category & Type Cards**:
- **تصنيف النشاط التجاري**: مقهى, مطعم, صيدلية, etc.
- **نوع الفاتورة**: فاتورة شراء, فاتورة ضمان, etc.

**Invoice Details**:
- رقم الفاتورة (Invoice Number)
- التاريخ (Date)
- المتجر (Vendor)
- الفرع (Branch)
- الهاتف (Phone)
- طريقة الدفع (Payment Method)

**Financial Summary**:
- 💰 المجموع الفرعي (Subtotal)
- 📊 الضريبة (Tax)
- 🎁 الخصومات (Discounts)
- 💵 الإجمالي النهائي (Total)

**AI Insight** (رؤية ذكية):
- 2-3 sentences in Arabic analyzing your purchase
- Example: "هذا الشراء من مقهى Starbucks. العميل طلب مشروبين بمبلغ معتدل..."

**Line Items Table**:
- Item description, quantity, unit price, total

**Actions**:
- **رفع فاتورة جديدة**: Upload another invoice

---

### 📋 3. Invoices Page

**Path**: `/invoices`

View all uploaded invoices with filtering and search.

#### Features

**Filter Dropdown**:
- الكل (All)
- مطاعم (Restaurants)
- مقاهي (Cafes)
- صيدليات (Pharmacies)
- تأمين (Insurance)
- شراء (Purchases)
- خدمات (Services)

**Invoice Cards**:

Each card displays:
- **Image Thumbnail** (click to enlarge)
- **Vendor Name** + Invoice Type badge
- **Date**, Cashier, Branch
- **Total Amount**, Discount, Payment Method
- **AI Insight** text

**Actions per Invoice**:
- **Click Image**: Opens full-screen modal with zoom/pan
- **تحميل كـ PDF**: Downloads original invoice image as PDF
- **Hover**: Card scales up slightly

#### Using Filters

1. **Click dropdown**: "اختر الفئة"
2. **Select category**: e.g., "مقاهي"
3. **View updates instantly** (no page reload)
4. **Reset**: Select "الكل"

#### Image Modal

When you click an invoice image:
- **Full-screen view** opens
- **Controls**:
  - 🔍 Zoom In
  - 🔍 Zoom Out
  - 🔄 Reset view
  - ⬇️ Download image
  - Drag to pan
  - Close with X button

#### PDF Download

1. **Click "تحميل كـ PDF"**
2. **Wait** for "جاري التنزيل..."
3. **PDF downloads** automatically
4. **Filename**: `{Vendor}_{InvoiceNumber}.pdf`
5. **Content**: Original invoice image (full page, A4)

---

### 📊 4. Dashboard Page

**Path**: `/dashboard`

Comprehensive analytics and insights.

#### Interactive Filters

**Three filter dropdowns**:
1. **التصنيف** (Category): مطعم, مقهى, صيدلية, etc.
2. **الشهر** (Month): يناير, فبراير, ..., ديسمبر
3. **طريقة الدفع** (Payment): Cash, Visa, Mada, etc.

**How to Use**:
- Select any combination of filters
- Dashboard updates **instantly**
- All stats, charts, and insights reflect filtered data
- Reset: Select "الكل" in any filter

#### Statistics Cards

**Top Row**:
- 📄 **إجمالي الفواتير**: Total count
- 💵 **إجمالي الإنفاق**: Total spending (SAR)
- 📊 **متوسط الفاتورة**: Average per invoice
- 🏪 **الأكثر تكراراً**: Most frequent vendor

#### Charts

**1. Category Pie Chart** (توزيع المصروفات حسب التصنيف):
- **Donut chart** showing spending by business type
- **Legend below** chart for clarity
- **Hover** over segment to see exact amount
- **Colors**: Pastel palette (blue, green, yellow, red, purple)

**2. Monthly Area Chart** (الإنفاق الشهري):
- **Trend line** showing spending over time
- **Filled area** for visual impact
- **X-axis**: Months
- **Y-axis**: Amount (SAR)

**3. Payment Method Bar Chart** (الإنفاق حسب طريقة الدفع):
- **Vertical bars** for each payment type
- **Compare**: Cash vs Visa vs Mada
- **Hover**: See exact amount

**4. Day of Week Radar Chart** (الإنفاق حسب اليوم):
- **Pentagon shape** showing spending pattern by weekday
- **Identify**: Which days you spend most
- **Example**: High on weekends, low on weekdays

#### Smart Insights (رؤى ذكية متقدمة)

**6 dynamic insights** generated from your data:

1. **Invoice count by category**:
   > "لديك ١٥ فاتورة مقهى — يبدو أنك من محبي القهوة!"

2. **Spending distribution**:
   > "٦٠٪ من إنفاقك على المطاعم والمقاهي"

3. **Payment preference**:
   > "أكثر طرق الدفع استخدامًا: Visa (٤٥ مرة)"

4. **Spending trend**:
   > "إنفاقك زاد بنسبة ١٥٪ عن الشهر الماضي"

5. **Vendor loyalty**:
   > "أكثر متجر تتعامل معه: Starbucks (٢٣ مرة)"

6. **Average insight**:
   > "متوسط الفاتورة الواحدة: ٨٥.٥٠ ر.س"

#### Top Vendors Table

**Displays**:
- Rank (#1, #2, etc.)
- Vendor name
- Number of visits
- Total spending

**Sorted by**: Frequency (most frequent first)

---

### 💬 5. Chat with AI Page

**Path**: `/chat`

Ask natural language questions about your invoices.

#### How It Works

The AI uses **3 intelligent modes**:

1. **🧮 SQL Mode**: Numerical questions (sum, count, average)
2. **📄 RAG Mode**: Descriptive questions (semantic search)
3. **🖼️ Retrieval Mode**: Specific vendor/type requests

#### Example Questions

**SQL Mode Questions**:
- "كم أنفقت على المطاعم؟"
- "كم عدد الفواتير هذا الشهر؟"
- "ما هو متوسط الفاتورة؟"
- "كم أنفقت في شهر سبتمبر؟"

**RAG Mode Questions**:
- "ما هي آخر مشترياتي؟"
- "اعطني نصائح لتوفير المال"
- "ما هي عاداتي الشرائية؟"

**Retrieval Mode Questions**:
- "أرسل لي فواتير دانكن"
- "أرني فواتير المقاهي"
- "عندي كم فاتورة من ستاربكس؟"

#### Using the Chat

1. **Type question** in input box
2. **Press Enter** or click "إرسال"
3. **Wait** for AI response (shows "جاري معالجة سؤالك...")
4. **View answer**:
   - **Text response** (Arabic)
   - **Invoice cards** (if applicable)

#### Understanding Responses

**Text-Only Response** (SQL mode):
```
أنفقت 345.50 ر.س على المطاعم
```

**Response with Invoices** (Retrieval mode):
```
تم العثور على 3 فواتير من دانكن:

[Invoice Card 1]
┌─────────────────────┐
│ 📷 [Image]          │
│ دانكن               │
│ فاتورة شراء         │
│ 2025-09-30          │
│ 35.25 ر.س          │
│ [تحميل PDF]        │
└─────────────────────┘

[Invoice Card 2]
[Invoice Card 3]
```

#### Invoice Cards in Chat

Each card shows:
- **Invoice image** (thumbnail)
- **Vendor name**
- **Invoice type** (فاتورة شراء, etc.)
- **Date**
- **Total amount**
- **تحميل PDF** button

**Actions**:
- **Click image**: Opens full-screen modal
- **Click PDF button**: Downloads invoice

#### Tips for Best Results

✅ **Good Questions**:
- Specific: "كم أنفقت على المقاهي في سبتمبر؟"
- Clear: "أرني فواتير ستاربكس"
- Natural: "عندي كم فاتورة هذا الشهر؟"

❌ **Avoid**:
- Too vague: "معلومات"
- Multiple questions: "كم أنفقت وماذا اشتريت وأين؟"
- Unrelated: "ما هو الطقس اليوم؟"

---

## 🎨 Theme & Customization

### Dark Mode

**Toggle**: Click 🌙 icon in navbar

**Options**:
- **فاتح** (Light): White background, dark text
- **داكن** (Dark): Dark background, light text
- **النظام** (System): Follows OS preference

**Benefits**:
- Reduces eye strain at night
- Saves battery (OLED screens)
- Looks modern and professional

### Color Scheme

The app uses a **teal-gold palette**:
- **Primary**: `#8dbcc7` (Teal/Cyan)
- **Secondary**: `#d4a574` (Gold/Beige)
- **Background**: Animated gradient
- **Text**: Cairo font (Arabic-optimized)

---

## 🔍 Advanced Features

### Camera Capture

**Browser Compatibility**:
- ✅ Chrome/Edge (desktop & mobile)
- ✅ Safari (iOS & macOS)
- ✅ Firefox
- ❌ Internet Explorer (not supported)

**Privacy**:
- Camera access **only** when you click button
- Images uploaded to **your Supabase** (not third-party)
- No data sent except to your backend

### PDF Generation

**Technology**: jsPDF

**Process**:
1. Fetches original invoice image from Supabase
2. Embeds image in A4 PDF (full page)
3. Downloads to your device
4. Filename includes vendor + invoice number

**Quality**: Same as original upload (lossless)

### Responsive Design

**Mobile** (< 768px):
- Single column layout
- Stacked cards
- Larger touch targets
- Bottom navigation (optional)

**Tablet** (768px - 1024px):
- 2-column grids
- Larger fonts
- Touch-optimized

**Desktop** (> 1024px):
- 3-column grids
- Hover effects
- Keyboard shortcuts

---

## ❓ Troubleshooting

### Upload Issues

**Problem**: "Upload failed"
**Solution**:
- Check file size (< 10MB recommended)
- Use JPG or PNG format
- Ensure Supabase bucket is public

**Problem**: "Camera not working"
**Solution**:
- Allow camera permission in browser
- Use HTTPS (required for camera API)
- Try different browser

### Analysis Issues

**Problem**: "Analysis failed" or wrong data
**Solution**:
- Ensure invoice image is clear (not blurry)
- Good lighting (no shadows/glare)
- Invoice fully visible (not cropped)
- Text is readable

**Problem**: Some fields show "Not Mentioned"
**Solution**:
- Normal if field doesn't exist on invoice
- VLM cannot guess missing information
- You can manually add data later (future feature)

### Dashboard Issues

**Problem**: Charts not loading
**Solution**:
- Refresh page
- Check if invoices exist (need at least 1)
- Clear browser cache

**Problem**: Filters not working
**Solution**:
- Reset filters to "الكل"
- Check if category names match database values

### Chat Issues

**Problem**: "Error processing question"
**Solution**:
- Rephrase question more clearly
- Check internet connection
- Ensure backend is running

**Problem**: No invoices returned
**Solution**:
- Verify vendor name spelling
- Upload at least one invoice first
- Try broader question

---

## 💡 Tips & Best Practices

### For Best Upload Results

1. **Good Lighting**: Natural light or bright indoor lighting
2. **Flat Surface**: Lay invoice flat (no wrinkles)
3. **Full Frame**: Capture entire invoice, minimal margins
4. **High Resolution**: Use good quality camera (5MP+)
5. **Focus**: Ensure text is sharp and readable

### For Accurate Analysis

1. **Wait for Complete Processing**: Don't interrupt upload/analysis
2. **Review Results**: Check if extracted data is correct
3. **Consistent Format**: Same invoice format helps AI learn
4. **Clear Receipts**: Thermal receipts fade over time - scan ASAP

### For Effective Chat

1. **Be Specific**: Include time periods, vendor names, categories
2. **One Question at a Time**: Break complex queries into simple ones
3. **Use Natural Language**: Ask as if talking to a person
4. **Learn from Examples**: Start with sample questions above

---

## 🔐 Security & Privacy

### Data Storage

- **Images**: Stored in **your** Supabase bucket (you control access)
- **Database**: Your Supabase PostgreSQL (encrypted at rest)
- **Embeddings**: Stored locally in your database

### API Keys

- **Never share** your `.env` file
- **Use environment variables** (not hardcoded)
- **Rotate keys** if exposed

### Access Control

- Currently no authentication (single-user)
- For production: Add Supabase Auth
- For multi-user: Add role-based access control

---

## 🚀 Next Steps

### Immediate Actions

1. ✅ Upload your first invoice
2. ✅ Explore dashboard analytics
3. ✅ Try asking chat questions
4. ✅ Enable dark mode
5. ✅ Download invoice as PDF

### Future Enhancements

- [ ] Manual invoice editing
- [ ] Bulk upload (multiple invoices)
- [ ] Export data as CSV/Excel
- [ ] Receipt scanning from WhatsApp/Email
- [ ] Budget alerts and limits
- [ ] Mobile app (iOS/Android)
- [ ] Multi-currency support
- [ ] Multi-user accounts

---

## 📞 Support

### Documentation

- **Backend**: `docs/backend_overview.md`
- **Frontend**: `docs/frontend_overview.md`
- **AI Models**: `docs/ai_models_overview.md`
- **API**: `docs/api_reference.md`

### Common Resources

- **Supabase Docs**: https://supabase.com/docs
- **Hugging Face**: https://huggingface.co/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Next.js**: https://nextjs.org/docs

---

## 🎓 Learning Resources

### For Developers

**Backend**:
- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy ORM: https://docs.sqlalchemy.org
- Supabase Python: https://supabase.com/docs/reference/python

**Frontend**:
- Next.js App Router: https://nextjs.org/docs/app
- Tailwind CSS: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com

**AI/ML**:
- Hugging Face Inference: https://huggingface.co/docs/api-inference
- Sentence Transformers: https://www.sbert.net
- pgvector: https://github.com/pgvector/pgvector

---

**Happy Invoice Management! 🎉**

**مُـفـــــوْتِــــر — يحفظ،يدير، يحلل، ويختصر وقتك.**

---

**Last Updated**: October 7, 2025  
**Version**: 1.0.0

