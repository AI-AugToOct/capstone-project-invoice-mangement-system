-- إضافة عمود is_valid_invoice لجدول invoices
-- هذا العمود يحدد إذا كانت الصورة المرفوعة فاتورة حقيقية أم لا

ALTER TABLE invoices 
ADD COLUMN IF NOT EXISTS is_valid_invoice BOOLEAN DEFAULT true;

-- إضافة index للبحث السريع عن الفواتير الصحيحة فقط
CREATE INDEX IF NOT EXISTS idx_invoices_is_valid 
ON invoices(is_valid_invoice);

-- تحديث الفواتير الموجودة لتكون صحيحة افتراضياً
UPDATE invoices 
SET is_valid_invoice = true 
WHERE is_valid_invoice IS NULL;

COMMENT ON COLUMN invoices.is_valid_invoice IS 'يحدد إذا كانت الصورة فاتورة حقيقية (true) أو مستند آخر (false)';

