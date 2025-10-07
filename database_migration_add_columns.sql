-- ===========================================
-- Migration: إضافة أعمدة جديدة للفواتير
-- ===========================================
-- نفّذ هذا السكريبت في Supabase SQL Editor

-- إضافة عمود invoice_type
ALTER TABLE invoices 
ADD COLUMN IF NOT EXISTS invoice_type TEXT;

-- إضافة عمود image_url
ALTER TABLE invoices 
ADD COLUMN IF NOT EXISTS image_url TEXT;

-- إضافة تعليق على الأعمدة
COMMENT ON COLUMN invoices.invoice_type IS 'نوع الفاتورة (شراء، تأمين، ضمان...)';
COMMENT ON COLUMN invoices.image_url IS 'رابط صورة الفاتورة من Supabase Storage';

-- تحديث الفواتير القديمة (اختياري)
UPDATE invoices 
SET invoice_type = 'شراء' 
WHERE invoice_type IS NULL;

-- ===========================================
-- ملاحظات:
-- ===========================================
-- 1. هذا السكريبت آمن ولن يؤثر على البيانات الموجودة
-- 2. يمكن تشغيله أكثر من مرة بأمان (IF NOT EXISTS)
-- 3. بعد التنفيذ، أعد تشغيل Backend ليتعرف على الأعمدة الجديدة
-- ===========================================

