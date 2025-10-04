import streamlit as st
import requests
import time
import os
from supabase import create_client
from dotenv import load_dotenv

# 📌 Load environment variables from .env
load_dotenv()

st.set_page_config(page_title="📑 Smart Invoice Analyzer", layout="wide")

# 🔑 Read from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/vlm/analyze")
UPLOAD_URL = os.getenv("UPLOAD_URL", "http://127.0.0.1:8000/upload/")

# ⚡ Init Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📂 Sidebar navigation
page = st.sidebar.radio("📂 Navigate", ["Analyze Invoice", "Uploaded Invoices"])

# ==============================
# 🔍 Analyze Invoice Page
# ==============================
if page == "Analyze Invoice":
    st.title("📑 Smart Invoice Analyzer")
    st.write("Upload an invoice and let AI analyze it")

    uploaded_file = st.file_uploader("Upload invoice image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
        if st.button("🔍 Analyze Invoice"):
            try:
                start_time = time.time()
                st.info("⏳ Sending to backend...")

                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                upload_response = requests.post(UPLOAD_URL, files=files)

                if upload_response.status_code != 200:
                    st.error(f"❌ Upload failed: {upload_response.text}")
                else:
                    upload_data = upload_response.json()
                    image_url = upload_data["url"]
                    st.success(f"✅ Image uploaded to Supabase!\n\n{image_url}")

                    payload = {
                        "image_url": image_url,
                        "prompt": """
    Read the invoice carefully and return ONLY one valid JSON object.

    The JSON **must** follow exactly this structure and order:

    {
      "Invoice Number": "...",
      "Date": "...",
      "Vendor": "...",
      "Tax Number": "...",
      "Cashier": "...",
      "Branch": "...",
      "Phone": "...",
      "Items": [
        {
          "description": "...",
          "quantity": "...",
          "unit_price": "...",
          "total": "..."
        }
      ],
      "Subtotal": "...",
      "Tax": "...",
      "Total Amount": "...",
      "Grand Total (before tax)": "...",
      "Discounts": "...",
      "Payment Method": "...",
      "Amount Paid": "...",
      "Ticket Number": "...",
      "Category": "...",
      "Currency": "SAR"
    }

    ### Rules:
    - If any field is missing in the invoice, set its value to "Not Mentioned".
    - Vendor must always be the store/restaurant name (not the cashier).
    - Cashier should be the employee/terminal ID if explicitly shown, else "Not Mentioned".
    - Branch = the physical location (city/university) if shown, else "Not Mentioned".
    - Phone must only be included if explicitly written. If missing, "Not Mentioned".
    - Subtotal must be taken exactly from the printed "Subtotal" field (before VAT).
    - Tax must be taken exactly from the printed "VAT / Tax" field.
    - Total Amount must be taken exactly from the printed "Total Amount".
    - Grand Total (before tax) must equal Subtotal.
    - Discounts must always be positive numbers.
    - If text is in Arabic, translate it into English before returning.
    - Do not add explanations, extra keys, or Markdown — return JSON only.
    """
                    }

                    response = requests.post(BACKEND_URL, json=payload)

                    if response.status_code != 200:
                        st.error(f"❌ Error from VLM: {response.text}")
                    else:
                        data = response.json()
                        result = data.get("output", {})
                        elapsed = round(time.time() - start_time, 2)

                        st.success("✅ Analysis complete!")

                        st.subheader("🧾 Invoice Details")

                        cols = st.columns(2)
                        with cols[0]:
                            st.markdown(f"**Invoice Number:** {result.get('Invoice Number', 'Not Mentioned')}")
                            st.markdown(f"**Date:** {result.get('Date', 'Not Mentioned')}")
                            st.markdown(f"**Vendor:** {result.get('Vendor', 'Not Mentioned')}")
                            st.markdown(f"**Tax Number:** {result.get('Tax Number', 'Not Mentioned')}")
                            st.markdown(f"**Cashier:** {result.get('Cashier', 'Not Mentioned')}")
                        with cols[1]:
                            st.markdown(f"**Branch:** {result.get('Branch', 'Not Mentioned')}")
                            st.markdown(f"**Phone:** {result.get('Phone', 'Not Mentioned')}")
                            st.markdown(f"**Category:** {result.get('Category', 'Not Mentioned')}")
                            st.markdown(f"**Payment Method:** {result.get('Payment Method', 'Not Mentioned')}")
                            st.markdown(f"**Amount Paid:** {result.get('Amount Paid', 'Not Mentioned')}")
                            st.markdown(f"**Currency:** {result.get('Currency', 'Not Mentioned')}")

                        # 🛒 Items
                        st.subheader("🛒 Items")
                        for idx, item in enumerate(result.get("Items", []), start=1):
                            with st.expander(f"Item {idx}"):
                                st.markdown(f"- **Description:** {item.get('description', 'Not Mentioned')}")
                                st.markdown(f"- **Quantity:** {item.get('quantity', 'Not Mentioned')}")
                                st.markdown(f"- **Unit Price:** {item.get('unit_price', 'Not Mentioned')}")
                                st.markdown(f"- **Total:** {item.get('total', 'Not Mentioned')}")

                        st.info(f"⏱️ Total time taken: {elapsed} seconds")

            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

# ==============================
# 📂 Uploaded Invoices Page
# ==============================
elif page == "Uploaded Invoices":
    st.title("📂 Uploaded Invoices")
    st.write("Browse all invoices uploaded to Supabase Storage.")

    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        response = supabase.storage.from_("invoices").list(path="")
        st.write("🔍 Raw response:", response)

        if isinstance(response, dict):
            files = response.get("data", [])
        else:
            files = response

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
