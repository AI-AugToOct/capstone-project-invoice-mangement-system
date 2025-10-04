import streamlit as st
import requests
import time
import os
from supabase import create_client
from dotenv import load_dotenv

# ============================================================
# ⚙️ App Configuration
# ============================================================
load_dotenv()
st.set_page_config(page_title="📑 Smart Invoice Analyzer", layout="wide")

# 🔑 Environment Variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/vlm/analyze")
UPLOAD_URL = os.getenv("UPLOAD_URL", "http://127.0.0.1:8000/upload/")

# ⚡ Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📂 Sidebar Navigation
page = st.sidebar.radio("📂 Navigate", ["Analyze Invoice", "Uploaded Invoices"])

# ============================================================
# 🔍 PAGE 1: Analyze Invoice
# ============================================================
if page == "Analyze Invoice":
    st.title("📑 Smart Invoice Analyzer")
    st.caption("Upload an invoice and let the AI extract data, classify it, and generate insights 🧠")

    uploaded_file = st.file_uploader("📤 Upload invoice image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

        if st.button("🔍 Analyze Invoice"):
            try:
                start_time = time.time()
                st.info("⏳ Uploading image to Supabase and analyzing with AI...")

                # 1️⃣ Upload the file to backend (Supabase storage)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                upload_response = requests.post(UPLOAD_URL, files=files)
                if upload_response.status_code != 200:
                    st.error(f"❌ Upload failed: {upload_response.text}")
                    st.stop()

                image_url = upload_response.json().get("url")
                st.success(f"✅ Image uploaded to Supabase!\n\n{image_url}")

                # 2️⃣ Prepare request payload for backend (VLM analysis)
                payload = {
                    "image_url": image_url,
                    "prompt": """
Read the invoice carefully and return ONE valid JSON object only.

The goal is to both extract invoice data AND infer business type and spending insight.

If any field is missing or unreadable, set it to "Not Mentioned".

Return all these exact keys:

{
  "Invoice Number": ...,
  "Date": ...,
  "Vendor": ...,
  "Tax Number": ...,
  "Cashier": ...,
  "Branch": ...,
  "Phone": ...,
  "Items": [
      {"description": ..., "quantity": ..., "unit_price": ..., "total": ...}
  ],
  "Subtotal": ...,
  "Tax": ...,
  "Total Amount": ...,
  "Grand Total (before tax)": ...,
  "Discounts": ...,
  "Payment Method": ...,
  "Amount Paid": ...,
  "Ticket Number": ...,
  "Category": ...,
  "AI_Insight": ...
}

### Rules:
- Always output valid JSON (no explanations, no Markdown).
- "Category" must classify the type of business in English, e.g.:
  Cafe, Restaurant, Supermarket, Pharmacy, Clothing, Electronics, Utility, Education, Health, Transport, Delivery, or Other.
- "AI_Insight" must be a short sentence like:
  "This purchase is from a cafe. Spending frequency at this vendor increased this month."
- Vendor should be the store name, not the cashier or branch.
- Subtotal, Tax, and Total must exactly match printed values.
"""
                }

                # 3️⃣ Send to backend (FastAPI → FriendliAI)
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code != 200:
                    st.error(f"❌ Backend error: {response.text}")
                    st.stop()

                data = response.json()
                result = data.get("output", {})
                ai_insight = data.get("ai_insight", "Not Mentioned")
                category_data = data.get("category", {"en": "Not Mentioned", "ar": "غير مذكور"})
                elapsed = round(time.time() - start_time, 2)

                # 4️⃣ Display results
                st.success("✅ Invoice analysis complete!")

                # ==============================
                # 🧾 Invoice Information
                # ==============================
                st.subheader("🧾 Invoice Details")

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Invoice Number:** {result.get('Invoice Number', 'Not Mentioned')}")
                    st.write(f"**Date:** {result.get('Date', 'Not Mentioned')}")
                    st.write(f"**Vendor:** {result.get('Vendor', 'Not Mentioned')}")
                    st.write(f"**Tax Number:** {result.get('Tax Number', 'Not Mentioned')}")
                    st.write(f"**Cashier:** {result.get('Cashier', 'Not Mentioned')}")
                with col2:
                    st.write(f"**Branch:** {result.get('Branch', 'Not Mentioned')}")
                    st.write(f"**Phone:** {result.get('Phone', 'Not Mentioned')}")
                    st.write(f"**Payment Method:** {result.get('Payment Method', 'Not Mentioned')}")
                    st.write(f"**Amount Paid:** {result.get('Amount Paid', 'Not Mentioned')} SAR")

                st.markdown("---")

                # ==============================
                # 💰 Totals
                # ==============================
                st.subheader("💰 Totals")
                totals_cols = st.columns(3)
                totals_cols[0].metric("Subtotal", f"{result.get('Subtotal', '0')} SAR")
                totals_cols[1].metric("Tax", f"{result.get('Tax', '0')} SAR")
                totals_cols[2].metric("Total", f"{result.get('Total Amount', '0')} SAR")

                st.write(f"**Grand Total (before tax):** {result.get('Grand Total (before tax)', 'Not Mentioned')} SAR")
                st.write(f"**Discounts:** {result.get('Discounts', '0')} SAR")
                st.write(f"**Ticket Number:** {result.get('Ticket Number', 'Not Mentioned')}")

                # ==============================
                # 🏷️ Category & Insight
                # ==============================
                st.subheader("🏷️ Category & Insight")
                st.info(f"**Category:** {category_data.get('en')} | {category_data.get('ar')}")
                st.markdown(f"🧠 **AI Insight:** {ai_insight}")

                # ==============================
                # 🛒 Items
                # ==============================
                st.subheader("🛒 Items")
                items = result.get("Items", [])
                if not items:
                    st.warning("No items detected.")
                else:
                    for i, item in enumerate(items, start=1):
                        with st.expander(f"Item {i}"):
                            st.write(f"- **Description:** {item.get('description', 'Not Mentioned')}")
                            st.write(f"- **Quantity:** {item.get('quantity', 'Not Mentioned')}")
                            st.write(f"- **Unit Price:** {item.get('unit_price', 'Not Mentioned')}")
                            st.write(f"- **Total:** {item.get('total', 'Not Mentioned')}")

                st.info(f"⏱️ Total time taken: {elapsed} seconds")

            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# ============================================================
# 📂 PAGE 2: Uploaded Invoices
# ============================================================
elif page == "Uploaded Invoices":
    st.title("📂 Uploaded Invoices")
    st.write("Browse all invoices uploaded to Supabase Storage.")

    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        response = supabase.storage.from_("invoices").list(path="")
        files = response.get("data", []) if isinstance(response, dict) else response

        if not files:
            st.info("ℹ️ No invoices uploaded yet.")
        else:
            cols = st.columns(3)
            for idx, file in enumerate(files):
                file_name = file.get("name")
                if file_name:
                    image_url = f"{SUPABASE_URL}/storage/v1/object/public/invoices/{file_name}"
                    with cols[idx % 3]:
                        st.image(image_url, caption=file_name, use_container_width=True)
                        st.markdown(f"[🔗 Open Link]({image_url})")

    except Exception as e:
        st.error(f"❌ Failed to load files: {str(e)}")
