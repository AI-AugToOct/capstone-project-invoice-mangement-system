import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Invoice OCR", layout="centered")
st.title("📸 Smart Invoice OCR")

uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Invoice", use_container_width=True)

    if st.button("Extract Invoice Data"):
        response = requests.post(
            f"{API_URL}/vlm/analyze",
            json={
                "image_url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg",
                "prompt": "Describe this image"
            }
        )
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
