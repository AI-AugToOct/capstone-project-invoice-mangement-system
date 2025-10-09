"""
Migration Script: إضافة عمود is_valid_invoice

هذا السكريبت يضيف عمود is_valid_invoice لجدول invoices
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment variables")
    exit(1)

print("🔧 Starting migration...")
print(f"📊 Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'unknown'}")

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # إضافة العمود
        print("➕ Adding is_valid_invoice column...")
        conn.execute(text("""
            ALTER TABLE invoices 
            ADD COLUMN IF NOT EXISTS is_valid_invoice BOOLEAN DEFAULT true;
        """))
        
        # إضافة index
        print("📊 Creating index...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_invoices_is_valid 
            ON invoices(is_valid_invoice);
        """))
        
        # تحديث الفواتير الموجودة
        print("🔄 Updating existing records...")
        conn.execute(text("""
            UPDATE invoices 
            SET is_valid_invoice = true 
            WHERE is_valid_invoice IS NULL;
        """))
        
        conn.commit()
        
        # التحقق
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = 'invoices' AND column_name = 'is_valid_invoice';
        """))
        
        row = result.fetchone()
        if row:
            print("✅ Migration completed successfully!")
            print(f"   Column: {row[0]}")
            print(f"   Type: {row[1]}")
            print(f"   Default: {row[2]}")
        else:
            print("⚠️ Column might not have been added")
            
except Exception as e:
    print(f"❌ Migration failed: {e}")
    exit(1)

