import streamlit as st
from supabase import create_client
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import theme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import get_light_theme_css

# Apply light theme CSS
st.markdown(get_light_theme_css(), unsafe_allow_html=True)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "invoices")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📂 الفواتير المرفوعة")
st.write("تصفح جميع الفواتير المرفوعة إلى تخزين Supabase.")

if st.button("🔄 تحديث"):
    st.rerun()

try:
    files = supabase.storage.from_(SUPABASE_BUCKET).list()
    if not files:
        st.info("ℹ️ لم يتم رفع فواتير بعد.")
    else:
        cols = st.columns(3)
        for idx, file in enumerate(files):
            file_name = file.get("name")
            if file_name:
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"
                with cols[idx % 3]:
                    st.image(image_url, caption=file_name, use_column_width=True)
                    st.markdown(f"[🔗 فتح الرابط]({image_url})")
except Exception as e:
    st.error(f"❌ فشل في تحميل الملفات: {str(e)}")
