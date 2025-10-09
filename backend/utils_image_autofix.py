"""
🔧 Image Auto-Fix Utilities
==========================
معالجة ذكية للصور المرفوعة لتصحيح الدوران والميل والمنظور تلقائياً.

Features:
- اكتشاف الصور المقلوبة وتصحيحها
- تصحيح الميل الطفيف (Deskewing)
- تصحيح المنظور للصور الملتقطة بزاوية
"""

import cv2
import numpy as np
import logging
from pathlib import Path

# Try to import pytesseract (optional - for OSD detection)
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("⚠️ pytesseract not available. OSD detection will be skipped.")

logger = logging.getLogger("backend.image_autofix")


# ================================================================
# 🔍 دالة اكتشاف زاوية الدوران (OSD - Orientation and Script Detection)
# ================================================================
def detect_osd_angle(img):
    """
    يكتشف زاوية دوران النص في الصورة باستخدام Tesseract OSD.
    
    Args:
        img: الصورة (numpy array)
    
    Returns:
        int: الزاوية المكتشفة (0, 90, 180, 270)
    """
    if not TESSERACT_AVAILABLE:
        return 0
    
    try:
        # تحويل الصورة إلى رمادي لتحسين الدقة
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # اكتشاف الـ OSD (يحتاج Tesseract مثبت)
        osd = pytesseract.image_to_osd(gray)
        
        # استخراج زاوية الدوران
        angle = int([line for line in osd.split('\n') if 'Rotate:' in line][0].split(':')[1].strip())
        
        logger.info(f"🔍 OSD detected rotation angle: {angle}°")
        return angle
    
    except Exception as e:
        logger.warning(f"⚠️ OSD detection failed: {e}. Skipping rotation correction.")
        return 0


# ================================================================
# 📐 دالة تصحيح الميل باستخدام Minimum Area Rectangle
# ================================================================
def deskew_via_min_area_rect(img):
    """
    يصحح الميل الطفيف في الصورة باستخدام كشف الحواف وحساب الزاوية.
    
    Args:
        img: الصورة (numpy array)
    
    Returns:
        numpy array: الصورة بعد تصحيح الميل
    """
    try:
        # تحويل إلى رمادي
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Threshold لفصل النص عن الخلفية
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # إيجاد جميع النقاط البيضاء (النص)
        coords = np.column_stack(np.where(thresh > 0))
        
        if len(coords) < 5:
            logger.warning("⚠️ Not enough points for deskewing. Skipping.")
            return img
        
        # حساب أصغر مستطيل يحيط بالنص
        rect = cv2.minAreaRect(coords)
        angle = rect[-1]
        
        # تصحيح الزاوية
        if angle < -45:
            angle = 90 + angle
        elif angle > 45:
            angle = angle - 90
        
        # إذا الزاوية صغيرة جداً، لا داعي للتصحيح
        if abs(angle) < 0.5:
            logger.info("✅ Image is already straight (angle < 0.5°)")
            return img
        
        logger.info(f"📐 Deskewing by {angle:.2f}°")
        
        # تطبيق التدوير
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    except Exception as e:
        logger.error(f"❌ Deskewing failed: {e}")
        return img


# ================================================================
# 🔲 دالة تصحيح المنظور (Perspective Correction)
# ================================================================
def correct_perspective(img):
    """
    يصحح المنظور للصور الملتقطة بزاوية (مثل تصوير الفاتورة من جنب).
    
    Args:
        img: الصورة (numpy array)
    
    Returns:
        numpy array: الصورة بعد تصحيح المنظور
    """
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # تطبيق Gaussian Blur لتقليل الضوضاء
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # كشف الحواف باستخدام Canny
        edged = cv2.Canny(blurred, 50, 150)
        
        # إيجاد الـ Contours
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            logger.info("ℹ️ No contours found. Skipping perspective correction.")
            return img
        
        # ترتيب الـ Contours حسب المساحة (الأكبر أولاً)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        # البحث عن contour مستطيل (4 نقاط)
        document_contour = None
        for contour in contours:
            # تقريب الـ contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # إذا كان له 4 نقاط، يُحتمل أنه الفاتورة
            if len(approx) == 4:
                document_contour = approx
                break
        
        # إذا ما لقينا مستطيل واضح، نرجع الصورة كما هي
        if document_contour is None:
            logger.info("ℹ️ No rectangular document detected. Skipping perspective correction.")
            return img
        
        # التأكد من أن المستطيل كبير بما يكفي (على الأقل 30% من مساحة الصورة)
        contour_area = cv2.contourArea(document_contour)
        image_area = img.shape[0] * img.shape[1]
        
        if contour_area < 0.3 * image_area:
            logger.info("ℹ️ Detected rectangle too small. Skipping perspective correction.")
            return img
        
        logger.info("🔲 Applying perspective correction")
        
        # ترتيب النقاط الأربع: أعلى-يسار، أعلى-يمين، أسفل-يمين، أسفل-يسار
        pts = document_contour.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        
        # مجموع الإحداثيات: أعلى-يسار له أصغر مجموع، أسفل-يمين له أكبر مجموع
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # الفرق بين الإحداثيات: أعلى-يمين له أصغر فرق، أسفل-يسار له أكبر فرق
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        # حساب العرض والطول الجديدين
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        
        # إنشاء مستطيل الوجهة
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype="float32")
        
        # حساب مصفوفة التحويل وتطبيقها
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        
        return warped
    
    except Exception as e:
        logger.error(f"❌ Perspective correction failed: {e}")
        return img


# ================================================================
# 🚀 الدالة الرئيسية: auto_fix_invoice_image
# ================================================================
def auto_fix_invoice_image(image_path: str) -> bool:
    """
    الدالة الرئيسية لتصحيح الصورة تلقائياً.
    
    تقوم بـ:
    1. اكتشاف وتصحيح الدوران (OSD)
    2. تصحيح الميل الطفيف
    3. تصحيح المنظور
    4. حفظ الصورة المصححة في نفس المسار
    
    Args:
        image_path (str): مسار الصورة المراد تصحيحها
    
    Returns:
        bool: True إذا نجحت العملية، False إذا فشلت
    """
    try:
        logger.info(f"🔧 Starting auto-fix for: {image_path}")
        
        # التحقق من وجود الملف
        if not Path(image_path).exists():
            logger.error(f"❌ Image file not found: {image_path}")
            return False
        
        # قراءة الصورة
        img = cv2.imread(image_path)
        
        if img is None:
            logger.error(f"❌ Failed to read image: {image_path}")
            return False
        
        original_shape = img.shape
        logger.info(f"📏 Original image size: {original_shape[1]}x{original_shape[0]}")
        
        # ============================================================
        # خطوة 1️⃣: اكتشاف وتصحيح الدوران (OSD)
        # ============================================================
        rotation_angle = detect_osd_angle(img)
        
        if rotation_angle != 0:
            logger.info(f"🔄 Rotating image by {rotation_angle}°")
            
            # تطبيق الدوران المناسب
            if rotation_angle == 90:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            elif rotation_angle == 180:
                img = cv2.rotate(img, cv2.ROTATE_180)
            elif rotation_angle == 270:
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # ============================================================
        # خطوة 2️⃣: تصحيح الميل الطفيف (Deskewing)
        # ============================================================
        img = deskew_via_min_area_rect(img)
        
        # ============================================================
        # خطوة 3️⃣: تصحيح المنظور (Perspective Correction)
        # ============================================================
        img = correct_perspective(img)
        
        # ============================================================
        # حفظ الصورة المصححة في نفس المسار
        # ============================================================
        success = cv2.imwrite(image_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        if success:
            new_shape = img.shape
            logger.info(f"✅ Auto-fix completed! New size: {new_shape[1]}x{new_shape[0]}")
            logger.info(f"💾 Corrected image saved to: {image_path}")
            return True
        else:
            logger.error(f"❌ Failed to save corrected image to: {image_path}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Auto-fix failed with error: {e}")
        return False


# ================================================================
# 🧪 للاختبار المحلي فقط
# ================================================================
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python utils_image_autofix.py <image_path>")
        sys.exit(1)
    
    test_image = sys.argv[1]
    result = auto_fix_invoice_image(test_image)
    
    if result:
        print(f"✅ Successfully auto-fixed: {test_image}")
    else:
        print(f"❌ Failed to auto-fix: {test_image}")

