# 🔧 Image Auto-Fix Feature

## 📋 نظرة عامة

تم إضافة ميزة تصحيح الصور التلقائي (Auto-Fix) لمعالجة الفواتير المرفوعة وتحسين دقة التحليل بالذكاء الاصطناعي.

---

## ✨ المميزات

### 1️⃣ **اكتشاف وتصحيح الدوران (OSD)**
- يكتشف الصور المقلوبة (90°, 180°, 270°)
- يصححها تلقائياً للاتجاه الصحيح
- يستخدم Tesseract OSD (Orientation and Script Detection)

### 2️⃣ **تصحيح الميل (Deskewing)**
- يكتشف الميل الطفيف في الصورة
- يحسب الزاوية باستخدام Minimum Area Rectangle
- يطبق تدوير دقيق لتصحيح الميل

### 3️⃣ **تصحيح المنظور (Perspective Correction)**
- يصحح الصور الملتقطة بزاوية
- يكتشف حواف الفاتورة تلقائياً
- يطبق تحويل المنظور للحصول على صورة مسطحة

---

## 📁 الملفات المعدلة

### 1. `backend/utils_image_autofix.py` (جديد)
```python
# الدوال الرئيسية:
- auto_fix_invoice_image(image_path)  # الدالة الرئيسية
- detect_osd_angle(img)                # اكتشاف زاوية الدوران
- deskew_via_min_area_rect(img)       # تصحيح الميل
- correct_perspective(img)             # تصحيح المنظور
```

### 2. `backend/routers/upload.py` (معدل)
```python
# تم إضافة:
- استيراد auto_fix_invoice_image
- حفظ الصورة مؤقتاً
- تطبيق التصحيح التلقائي
- قراءة الصورة المصححة
- حذف الملف المؤقت
```

### 3. `backend/requirements.txt` (محدث)
```
opencv-python==4.10.0.84
pytesseract==0.3.13
```

---

## 🔧 المتطلبات

### Python Libraries:
```bash
pip install opencv-python pytesseract numpy
```

### Tesseract OCR (للـ OSD):
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# تحميل من: https://github.com/UB-Mannheim/tesseract/wiki
# وإضافة المسار إلى PATH
```

**ملاحظة**: إذا لم يكن Tesseract مثبت، الكود يعمل بدون ميزة OSD فقط (يتخطى تصحيح الدوران).

---

## 🚀 كيفية الاستخدام

### تلقائياً في `/upload/`:
```python
# الكود يعمل تلقائياً عند رفع أي صورة
POST /upload/
```

### اختبار يدوي:
```bash
python backend/utils_image_autofix.py path/to/invoice.jpg
```

---

## 📊 سير العمل (Workflow)

```
1️⃣ المستخدم يرفع صورة/PDF
          ↓
2️⃣ تحويل PDF إلى صورة (إذا لزم)
          ↓
3️⃣ حفظ الصورة مؤقتاً
          ↓
4️⃣ تطبيق Auto-Fix:
   ├─ اكتشاف وتصحيح الدوران (OSD)
   ├─ تصحيح الميل (Deskewing)
   └─ تصحيح المنظور (Perspective)
          ↓
5️⃣ قراءة الصورة المصححة
          ↓
6️⃣ رفع الصورة المصححة إلى Supabase
          ↓
7️⃣ حذف الملف المؤقت
          ↓
8️⃣ إرجاع رابط الصورة للـ Frontend
```

---

## 🧪 أمثلة على التصحيحات

### مثال 1: صورة مقلوبة 180°
```
Input:  🙃 (مقلوبة)
Output: 🙂 (معدلة تلقائياً)
```

### مثال 2: صورة مائلة 5°
```
Input:  / (مائلة)
Output: | (مستقيمة)
```

### مثال 3: صورة بمنظور
```
Input:  ▱ (ملتقطة من زاوية)
Output: ▬ (مسطحة)
```

---

## ⚙️ إعدادات متقدمة

### تعطيل Auto-Fix مؤقتاً:
```python
# في upload.py، علّق على السطر:
# auto_fix_success = auto_fix_invoice_image(temp_file_path)
```

### تعديل حساسية الميل:
```python
# في utils_image_autofix.py
if abs(angle) < 0.5:  # غير 0.5 إلى قيمة أخرى
    return img
```

### تعديل حجم الـ Contour:
```python
# في correct_perspective()
if contour_area < 0.3 * image_area:  # غير 0.3 إلى قيمة أخرى
    return img
```

---

## 🐛 استكشاف الأخطاء (Troubleshooting)

### 1. Tesseract not found:
```bash
# تأكد من تثبيت Tesseract
which tesseract  # Linux/Mac
where tesseract  # Windows

# إذا كان مثبت ولكن ما يشتغل، أضف المسار يدوياً:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 2. OpenCV import error:
```bash
# حاول تثبيت النسخة headless:
pip uninstall opencv-python
pip install opencv-python-headless
```

### 3. Auto-fix يستغرق وقت طويل:
```python
# قلل دقة الصورة قبل المعالجة:
max_size = 2000
if img.shape[0] > max_size or img.shape[1] > max_size:
    scale = max_size / max(img.shape[0], img.shape[1])
    img = cv2.resize(img, None, fx=scale, fy=scale)
```

---

## 📈 الأداء

### متوسط الوقت:
- **OSD Detection**: ~0.5-1 ثانية
- **Deskewing**: ~0.1-0.3 ثانية
- **Perspective Correction**: ~0.2-0.5 ثانية
- **الإجمالي**: ~1-2 ثانية لكل صورة

### استهلاك الذاكرة:
- صورة 2MB: ~50-100MB ذاكرة
- صورة 5MB: ~100-200MB ذاكرة

---

## ✅ الفوائد

1. **تحسين دقة التحليل**: صور مستقيمة = استخراج أفضل للبيانات
2. **تجربة مستخدم أفضل**: لا حاجة لتعديل الصورة يدوياً
3. **أتمتة كاملة**: كل شيء يحدث في الخلفية
4. **مرونة**: يعمل مع جميع أنواع الصور والزوايا

---

## 🔒 الأمان والخصوصية

- ✅ الصور تُحفظ مؤقتاً فقط
- ✅ يتم حذف الملفات المؤقتة تلقائياً بعد المعالجة
- ✅ لا يتم تخزين أي بيانات إضافية في قاعدة البيانات
- ✅ المعالجة تتم على الخادم (لا ترسل بيانات لأطراف ثالثة)

---

## 📝 ملاحظات مهمة

1. **Tesseract اختياري**: الكود يعمل بدونه (بدون OSD فقط)
2. **الأداء**: قد يزيد وقت الرفع بـ 1-2 ثانية
3. **الجودة**: تُحفظ الصور بجودة 95% (JPEG)
4. **الحجم**: قد يزيد حجم الصورة قليلاً بعد المعالجة

---

## 🚀 الخطوات القادمة (Future Enhancements)

- [ ] دعم معالجة دفعات (Batch Processing)
- [ ] تحسين سرعة المعالجة (GPU Acceleration)
- [ ] إضافة Image Denoising (إزالة الضوضاء)
- [ ] دعم Super-Resolution (تحسين جودة الصور)
- [ ] إضافة تصحيح الإضاءة (Lighting Correction)

---

**📅 آخر تحديث**: 2025-10-09  
**🔧 تم التطوير بواسطة**: فريق مُـــفـــــوْتِـــــر

---

**✨ الآن الفواتير تُصحح تلقائياً! لا مزيد من الصور المائلة أو المقلوبة!** 🎉

