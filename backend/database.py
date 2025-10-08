from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os, time
from dotenv import load_dotenv
import psycopg2
from sqlalchemy.exc import OperationalError

load_dotenv()

raw_url = os.getenv("DATABASE_URL", "").strip()

# 🔧 تصحيح أي "DATABASE_URL=" مضافة بالغلط
if raw_url.startswith("DATABASE_URL="):
    raw_url = raw_url.split("=", 1)[1].strip()

# ✅ نضيف إعدادات الاتصال الآمنة والترميز
connect_args = {"sslmode": "require", "client_encoding": "utf8"}

for attempt in range(3):
    try:
        engine = create_engine(raw_url, connect_args=connect_args, pool_pre_ping=True)
        # تجربة اتصال سريعة
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        print("✅ تم الاتصال بقاعدة البيانات بنجاح!")
        break
    except OperationalError as e:
        print(f"❌ محاولة {attempt+1}: فشل الاتصال بقاعدة البيانات → {e}")
        time.sleep(3)
else:
    print("🚨 لم يتم الاتصال بـ Supabase بعد 3 محاولات")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
