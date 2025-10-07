import streamlit as st
import requests
import time
import os
from supabase import create_client
from dotenv import load_dotenv
from theme import get_light_theme_css, get_page_config

# ============================================================
# ⚙️ App Configuration
# ============================================================
load_dotenv()

# Configure the main app with light theme
config = get_page_config()
st.set_page_config(**config)

# Apply light theme CSS
st.markdown(get_light_theme_css(), unsafe_allow_html=True)

# 🔑 Environment Variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/vlm/analyze")
UPLOAD_URL = os.getenv("UPLOAD_URL", "http://127.0.0.1:8000/upload/")

# ⚡ Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================
# 🔍 Analyze Invoice Page
# ============================================================

# Beautiful header with light theme
st.markdown("""
<div class="invoice-header">
    <h1 style="margin: 0; font-size: 3rem;">📑 محلل الفواتير الذكي</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
        قم برفع فاتورة ودع الذكاء الاصطناعي يستخرج البيانات ويصنفها وينتج رؤى تحليلية 🧠
    </p>
</div>
""", unsafe_allow_html=True)

# Feature overview with light theme cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #8DBCC7; margin-top: 0;">🤖 التحليل بالذكاء الاصطناعي</h3>
        <p>نماذج التعلم الآلي المتقدمة تستخرج البيانات الأساسية من فواتيرك تلقائياً.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #A4CCD9; margin-top: 0;">☁️ التخزين السحابي</h3>
        <p>تخزين آمن مع تكامل Supabase لجميع مستنداتك المهمة.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #C4E1E6; margin-top: 0;">📊 الرؤى التحليلية</h3>
        <p>إنتاج رؤى تجارية مفيدة وتحليلات من بيانات فواتيرك.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# File uploader section
st.subheader("📤 ارفع فاتورتك")
st.markdown("*الصيغ المدعومة: JPG, JPEG, PNG*")

uploaded_file = st.file_uploader("📤 ارفع صورة الفاتورة", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

    if st.button("🔍 تحليل الفاتورة"):
        try:
            start_time = time.time()
            st.info("⏳ جاري رفع الصورة إلى Supabase وتحليلها بالذكاء الاصطناعي...")

            # 1️⃣ Upload file to backend
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            upload_response = requests.post(UPLOAD_URL, files=files)
            if upload_response.status_code != 200:
                st.error(f"❌ فشل في الرفع: {upload_response.text}")
                st.stop()

            image_url = upload_response.json().get("url")
            st.success(f"✅ تم رفع الصورة إلى Supabase بنجاح!\n\n{image_url}")

            # 2️⃣ Prepare payload for backend (VLM analysis)
            payload = {
                "image_url": image_url,
                "prompt": """
                Read the invoice carefully and return ONE valid JSON object only.
                The goal is to extract invoice data AND infer business type and spending insight.
                If any field is missing, set it to "Not Mentioned".

                Return these keys exactly:
                {
                    "Invoice Number": ..., "Date": ..., "Vendor": ..., "Tax Number": ...,
                    "Cashier": ..., "Branch": ..., "Phone": ...,
                    "Items": [ {"description": ..., "quantity": ..., "unit_price": ..., "total": ...} ],
                    "Subtotal": ..., "Tax": ..., "Total Amount": ..., "Grand Total (before tax)": ...,
                    "Discounts": ..., "Payment Method": ..., "Amount Paid": ..., "Ticket Number": ...,
                    "Category": ..., "AI_Insight": ...
                }

                Rules:
                - Output valid JSON only (no explanations or markdown).
                - Category must classify the type of business (Cafe, Restaurant, Supermarket, etc.).
                - AI_Insight: short English insight sentence.
                - Vendor = store name.
                - Subtotal, Tax, and Total must match the printed values exactly.
                """
            }

            # 3️⃣ Send to backend (FastAPI → FriendliAI)
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code != 200:
                st.error(f"❌ خطأ في الخادم الخلفي: {response.text}")
                st.stop()

            data = response.json()
            result = data.get("output", {})
            ai_insight = data.get("ai_insight", "غير مذكور")
            category_data = data.get("category", {"en": "Not Mentioned", "ar": "غير مذكور"})
            elapsed = round(time.time() - start_time, 2)

            # 4️⃣ Display results
            st.success("✅ تم تحليل الفاتورة بنجاح!")

            # Invoice Info
            st.subheader("🧾 تفاصيل الفاتورة")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**رقم الفاتورة:** {result.get('Invoice Number', 'غير مذكور')}")
                st.write(f"**التاريخ:** {result.get('Date', 'غير مذكور')}")
                st.write(f"**البائع:** {result.get('Vendor', 'غير مذكور')}")
                st.write(f"**الرقم الضريبي:** {result.get('Tax Number', 'غير مذكور')}")
                st.write(f"**أمين الصندوق:** {result.get('Cashier', 'غير مذكور')}")
            with col2:
                st.write(f"**الفرع:** {result.get('Branch', 'غير مذكور')}")
                st.write(f"**الهاتف:** {result.get('Phone', 'غير مذكور')}")
                st.write(f"**طريقة الدفع:** {result.get('Payment Method', 'غير مذكور')}")
                st.write(f"**المبلغ المدفوع:** {result.get('Amount Paid', 'غير مذكور')} ريال")
            st.markdown("---")

            # Totals
            st.subheader("💰 الإجماليات")
            totals_cols = st.columns(3)
            totals_cols[0].metric("المجموع الفرعي", f"{result.get('Subtotal', '0')} ريال")
            totals_cols[1].metric("الضريبة", f"{result.get('Tax', '0')} ريال")
            totals_cols[2].metric("الإجمالي", f"{result.get('Total Amount', '0')} ريال")
            st.write(f"**الإجمالي الكبير (قبل الضريبة):** {result.get('Grand Total (before tax)', 'غير مذكور')} ريال")
            st.write(f"**الخصومات:** {result.get('Discounts', '0')} ريال")
            st.write(f"**رقم التذكرة:** {result.get('Ticket Number', 'غير مذكور')}")

            # Category & Insight
            st.subheader("🏷️ التصنيف والرؤى")
            st.info(f"**التصنيف:** {category_data.get('ar')} | {category_data.get('en')}")
            st.markdown(f"🧠 **رؤية الذكاء الاصطناعي:** {ai_insight}")

            # Items
            st.subheader("🛒 العناصر")
            items = result.get("Items", [])
            if not items:
                st.warning("لم يتم اكتشاف عناصر.")
            else:
                for i, item in enumerate(items, start=1):
                    with st.expander(f"العنصر {i}"):
                        st.write(f"- **الوصف:** {item.get('description', 'غير مذكور')}")
                        st.write(f"- **الكمية:** {item.get('quantity', 'غير مذكور')}")
                        st.write(f"- **سعر الوحدة:** {item.get('unit_price', 'غير مذكور')}")
                        st.write(f"- **الإجمالي:** {item.get('total', 'غير مذكور')}")

            st.info(f"⏱️ إجمالي الوقت المستغرق: {elapsed} ثانية")

        except Exception as e:
            st.error(f"❌ خطأ غير متوقع: {str(e)}")
