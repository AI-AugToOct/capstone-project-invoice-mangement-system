-- ===========================================
-- مُفَوْتِر - Database Setup Script
-- ===========================================
-- هذا السكريبت يُنشئ جميع الجداول المطلوبة في Supabase
-- نفّذه في: Supabase Dashboard → SQL Editor

-- ----------------------------------------
-- 1. تفعيل pgvector Extension
-- ----------------------------------------
CREATE EXTENSION IF NOT EXISTS vector;

-- ----------------------------------------
-- 2. جدول الفواتير الرئيسي
-- ----------------------------------------
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    record INTEGER,
    invoice_number VARCHAR(255),
    invoice_date TIMESTAMP,
    vendor VARCHAR(255),
    tax_number VARCHAR(255),
    cashier VARCHAR(255),
    branch VARCHAR(255),
    phone VARCHAR(255),
    subtotal VARCHAR(50),
    tax VARCHAR(50),
    total_amount VARCHAR(50),
    grand_total VARCHAR(50),
    discounts VARCHAR(50),
    payment_method VARCHAR(100),
    amount_paid VARCHAR(50),
    ticket_number VARCHAR(255),
    category TEXT,
    ai_insight TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ----------------------------------------
-- 3. جدول المنتجات/البنود
-- ----------------------------------------
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) ON DELETE CASCADE,
    description VARCHAR(500),
    quantity INTEGER,
    unit_price FLOAT,
    total FLOAT
);

-- ----------------------------------------
-- 4. جدول Embeddings للبحث الدلالي
-- ----------------------------------------
CREATE TABLE IF NOT EXISTS invoice_embeddings (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) ON DELETE CASCADE,
    embedding VECTOR(384)
);

-- ----------------------------------------
-- 5. إنشاء Indexes لتحسين الأداء
-- ----------------------------------------

-- Index على vendor لتسريع البحث
CREATE INDEX IF NOT EXISTS idx_invoice_vendor 
ON invoices(vendor);

-- Index على التاريخ
CREATE INDEX IF NOT EXISTS idx_invoice_date 
ON invoices(invoice_date DESC);

-- Index على رقم الفاتورة
CREATE INDEX IF NOT EXISTS idx_invoice_number 
ON invoices(invoice_number);

-- Index على الفئة
CREATE INDEX IF NOT EXISTS idx_invoice_category 
ON invoices(category);

-- Vector Index للبحث الدلالي (IVFFlat)
CREATE INDEX IF NOT EXISTS idx_embedding_cosine 
ON invoice_embeddings 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- ----------------------------------------
-- 6. إنشاء Views للاستعلامات السريعة
-- ----------------------------------------

-- View لعرض الفواتير مع عدد المنتجات
CREATE OR REPLACE VIEW invoices_with_items AS
SELECT 
    i.*,
    COUNT(it.id) as items_count,
    SUM(it.total) as items_total
FROM invoices i
LEFT JOIN items it ON i.id = it.invoice_id
GROUP BY i.id;

-- View لأكثر المتاجر تكرارًا
CREATE OR REPLACE VIEW top_vendors AS
SELECT 
    vendor,
    COUNT(*) as invoice_count,
    SUM(CAST(total_amount AS FLOAT)) as total_spent
FROM invoices
WHERE vendor IS NOT NULL
GROUP BY vendor
ORDER BY invoice_count DESC;

-- View للإحصائيات الشهرية
CREATE OR REPLACE VIEW monthly_stats AS
SELECT 
    DATE_TRUNC('month', invoice_date) as month,
    COUNT(*) as invoice_count,
    SUM(CAST(total_amount AS FLOAT)) as total_spent,
    AVG(CAST(total_amount AS FLOAT)) as avg_amount
FROM invoices
WHERE invoice_date IS NOT NULL
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month DESC;

-- ----------------------------------------
-- 7. Functions مساعدة
-- ----------------------------------------

-- Function للبحث عن فواتير قريبة (Semantic Search)
CREATE OR REPLACE FUNCTION search_similar_invoices(
    query_embedding VECTOR(384),
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    invoice_id INT,
    vendor VARCHAR,
    total_amount VARCHAR,
    invoice_date TIMESTAMP,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id,
        i.vendor,
        i.total_amount,
        i.invoice_date,
        1 - (e.embedding <=> query_embedding) as similarity
    FROM invoices i
    JOIN invoice_embeddings e ON i.id = e.invoice_id
    ORDER BY e.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ----------------------------------------
-- 8. Triggers لتحديث timestamps تلقائياً
-- ----------------------------------------

-- Trigger لتحديث created_at
CREATE OR REPLACE FUNCTION update_created_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.created_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_created_at
    BEFORE INSERT ON invoices
    FOR EACH ROW
    EXECUTE FUNCTION update_created_at();

-- ----------------------------------------
-- 9. Sample Data للاختبار (اختياري)
-- ----------------------------------------

-- يمكنك حذف هذا القسم إذا لم تحتاجه

-- INSERT INTO invoices (
--     invoice_number, vendor, total_amount, category, invoice_date
-- ) VALUES 
-- ('INV-001', 'مطعم الأصالة', '150.50', '{"en":"Restaurant","ar":"مطعم"}', NOW()),
-- ('INV-002', 'صيدلية النهدي', '85.00', '{"en":"Pharmacy","ar":"صيدلية"}', NOW()),
-- ('INV-003', 'ستارباكس', '42.00', '{"en":"Cafe","ar":"مقهى"}', NOW());

-- ----------------------------------------
-- 10. Policies (Row Level Security) - اختياري
-- ----------------------------------------

-- لتفعيل RLS في المستقبل:
-- ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE items ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE invoice_embeddings ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------
-- ✅ تم بنجاح!
-- ----------------------------------------
-- الآن يمكنك تشغيل Backend وسيتصل بقاعدة البيانات تلقائياً

-- للتحقق من الجداول:
-- \dt

-- للتحقق من pgvector:
-- SELECT * FROM pg_extension WHERE extname = 'vector';

-- ===========================================
-- ملاحظات:
-- ===========================================
-- 1. نفّذ هذا السكريبت مرة واحدة فقط
-- 2. إذا كانت الجداول موجودة، استخدم DROP TABLE أولاً
-- 3. تأكد من أن pgvector مثبت ومُفعّل
-- ===========================================

