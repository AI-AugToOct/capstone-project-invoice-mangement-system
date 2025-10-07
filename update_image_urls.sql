-- ===========================================
-- Update image URLs for existing invoices
-- ===========================================
-- Run this in Supabase SQL Editor

-- 1. Add image_url column if not exists
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS image_url TEXT;

-- 2. Update specific invoices (adjust IDs based on your data)
-- Replace the URLs with your actual Supabase project URL

UPDATE invoices 
SET image_url = 'https://pcktfzshbxaljkbedrar.supabase.co/storage/v1/object/public/invoices/invoice_2.jpg'
WHERE id = 2 OR id = 6;

UPDATE invoices 
SET image_url = 'https://pcktfzshbxaljkbedrar.supabase.co/storage/v1/object/public/invoices/invoice_3.jpg'
WHERE id = 3 OR id = 7;

-- 3. Verify the updates
SELECT id, vendor, invoice_number, image_url 
FROM invoices 
WHERE image_url IS NOT NULL;

-- ===========================================
-- Note: Adjust the WHERE conditions based on 
-- your actual invoice IDs that have images
-- ===========================================

