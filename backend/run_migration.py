"""
Migration Script: Add new columns to invoices table
Run this if you can't access Supabase SQL Editor directly
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

def run_migration():
    """Add invoice_type and image_url columns to invoices table"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please make sure you have a .env file with DATABASE_URL")
        return
    
    print("🔄 Connecting to database...")
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("✅ Connected successfully!")
            
            # Add invoice_type column
            print("\n📝 Adding 'invoice_type' column...")
            try:
                conn.execute(text("""
                    ALTER TABLE invoices 
                    ADD COLUMN IF NOT EXISTS invoice_type TEXT;
                """))
                conn.commit()
                print("✅ invoice_type column added!")
            except Exception as e:
                print(f"⚠️ invoice_type column might already exist: {e}")
            
            # Add image_url column
            print("\n📝 Adding 'image_url' column...")
            try:
                conn.execute(text("""
                    ALTER TABLE invoices 
                    ADD COLUMN IF NOT EXISTS image_url TEXT;
                """))
                conn.commit()
                print("✅ image_url column added!")
            except Exception as e:
                print(f"⚠️ image_url column might already exist: {e}")
            
            # Update existing invoices
            print("\n📝 Updating existing invoices...")
            try:
                result = conn.execute(text("""
                    UPDATE invoices 
                    SET invoice_type = 'شراء'
                    WHERE invoice_type IS NULL;
                """))
                conn.commit()
                print(f"✅ Updated {result.rowcount} invoices with default type!")
            except Exception as e:
                print(f"⚠️ Could not update existing invoices: {e}")
            
            # Verify columns exist
            print("\n🔍 Verifying columns...")
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'invoices' 
                  AND column_name IN ('invoice_type', 'image_url');
            """))
            
            columns = result.fetchall()
            print("\n✅ Migration completed successfully!")
            print("\nNew columns:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
            
            print("\n🎉 Done! You can now restart your backend.")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 INVOICE MANAGEMENT SYSTEM - DATABASE MIGRATION")
    print("=" * 60)
    print("\nThis script will add the following columns to 'invoices' table:")
    print("  - invoice_type (TEXT)")
    print("  - image_url (TEXT)")
    print("\n" + "=" * 60)
    
    response = input("\n⚠️  Continue? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        run_migration()
    else:
        print("\n❌ Migration cancelled.")

