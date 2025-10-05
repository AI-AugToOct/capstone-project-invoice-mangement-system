import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# 🌍 Load environment variables
load_dotenv()

# 🔑 Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "invoices")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧾 Page setup
st.set_page_config(page_title="Uploaded Invoices", page_icon="📂", layout="wide")
st.title("📂 Uploaded Invoices")
st.caption("Browse all invoices uploaded to Supabase Storage with a clean, responsive grid view.")
st.divider()

# 🔄 Refresh button
center = st.columns([3, 1, 3])[1]
with center:
    if st.button("🔄 Refresh Invoices", use_container_width=True):
        st.rerun()

# 🧠 Load files from Supabase
try:
    files = supabase.storage.from_(SUPABASE_BUCKET).list()

    if not files:
        st.info("ℹ️ No invoices uploaded yet.")
    else:
        # 💡 Filter only image files
        valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".pdf")
        image_files = [f for f in files if f.get("name") and not f["name"].startswith(".") and f["name"].lower().endswith(valid_extensions)]

        if not image_files:
            st.warning("⚠️ No valid image or PDF files found in the bucket.")
        else:
            num_columns = 3
            cols = st.columns(num_columns)

            for idx, file in enumerate(image_files):
                file_name = file["name"]
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"

                with cols[idx % num_columns]:
                    # Detect if it’s an image or PDF
                    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff")):
                        content = f"""
                        <div style="text-align:center; border:1px solid #ddd; border-radius:10px;
                                    padding:10px; margin-bottom:15px; background-color:#fafafa;">
                            <img src="{image_url}" style="width:100%; border-radius:8px;"/>
                            <p style="margin-top:10px; font-weight:600;">{file_name}</p>
                            <a href="{image_url}" target="_blank"
                               style="display:inline-block; background:#2b7de9; color:white;
                                      text-decoration:none; padding:6px 12px; border-radius:6px;">
                               🔗 Open Link
                            </a>
                        </div>
                        """
                    else:
                        content = f"""
                        <div style="text-align:center; border:1px solid #ddd; border-radius:10px;
                                    padding:15px; margin-bottom:15px; background-color:#f8f9fa;">
                            <p style="font-size:48px;">📄</p>
                            <p style="margin-top:-10px; font-weight:600;">{file_name}</p>
                            <a href="{image_url}" target="_blank"
                               style="display:inline-block; background:#2b7de9; color:white;
                                      text-decoration:none; padding:6px 12px; border-radius:6px;">
                               🔗 Open File
                            </a>
                        </div>
                        """

                    st.markdown(content, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Failed to load files: {str(e)}")
