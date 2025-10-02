import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Invoice OCR", layout="centered")
st.title("📸 Smart Invoice OCR + VLM")

# رفع ملف صورة
uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Invoice", use_container_width=True)

    prompt = st.text_input("Prompt", "Describe this invoice in one sentence.")

    if st.button("Analyze with VLM"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

        try:
            response = requests.post(
                f"{API_URL}/vlm/analyze",
                json={
                    "image_url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg",  # ⚠️ هنا لو عندك سيرفر رفع صور اربطه
                    "prompt": prompt
                }
            )

            if response.status_code == 200:
                st.subheader("✅ VLM Response")
                st.json(response.json())
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"⚠️ Request failed: {str(e)}")
