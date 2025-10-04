import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

#  Load environment variables
load_dotenv()

#  Supabase settings from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "invoices")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📂 Uploaded Invoices")
st.write("Browse all invoices uploaded to Supabase Storage.")

if st.button("🔄 Refresh"):
    st.rerun()

try:
    files = supabase.storage.from_(SUPABASE_BUCKET).list()

    if not files:
        st.info("ℹ️ No invoices uploaded yet.")
    else:
        cols = st.columns(3)
        for idx, file in enumerate(files):
            file_name = file.get("name")
            if file_name:
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"

                with cols[idx % 3]:
                    st.image(image_url, caption=file_name, use_container_width=True)
                    st.markdown(f"[🔗 Open Link]({image_url})")

except Exception as e:
    st.error(f"❌ Failed to load files: {str(e)}")
