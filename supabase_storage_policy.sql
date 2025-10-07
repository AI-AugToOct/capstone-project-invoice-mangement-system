-- ===========================================
-- Supabase Storage Policy for Public Access
-- ===========================================
-- Run this in Supabase SQL Editor

-- 1. Create policy for public read access
CREATE POLICY IF NOT EXISTS "Public read access for invoices"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'invoices');

-- 2. Create policy for authenticated uploads (optional)
CREATE POLICY IF NOT EXISTS "Authenticated users can upload invoices"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'invoices');

-- 3. Create policy for authenticated updates (optional)
CREATE POLICY IF NOT EXISTS "Authenticated users can update invoices"
ON storage.objects FOR UPDATE
TO authenticated
USING (bucket_id = 'invoices');

-- 4. Create policy for authenticated deletes (optional)
CREATE POLICY IF NOT EXISTS "Authenticated users can delete invoices"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'invoices');

-- ===========================================
-- Verify policies
-- ===========================================
SELECT * 
FROM pg_policies 
WHERE tablename = 'objects' 
  AND schemaname = 'storage';

-- ===========================================
-- Alternative: Make bucket public (simpler)
-- ===========================================
-- Go to: Storage → invoices → Configuration
-- Enable: "Public bucket"
-- ===========================================

