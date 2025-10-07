import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import theme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import get_light_theme_css

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="📊 لوحة تحكم الفواتير", layout="wide")

# Apply light theme CSS
st.markdown(get_light_theme_css(), unsafe_allow_html=True)
st.title("📊 لوحة تحكم الفواتير")
st.caption("تحليلات فورية لفواتيرك مع رؤى مدعومة بالذكاء الاصطناعي ⚙️")

try:
    stats_response = requests.get(f"{BACKEND_URL}/dashboard/stats", timeout=5)
    invoices_response = requests.get(f"{BACKEND_URL}/invoices/all", timeout=5)

    stats = stats_response.json() if stats_response.status_code == 200 else {"total_invoices": 0, "total_spent": 0.0, "top_vendors": []}
    invoices = invoices_response.json() if invoices_response.status_code == 200 else []
except Exception as e:
    st.error(f"❌ فشل في الاتصال بالخادم الخلفي: {e}")
    stats = {"total_invoices": 0, "total_spent": 0.0, "top_vendors": []}
    invoices = []

df = pd.DataFrame(invoices if isinstance(invoices, list) else [invoices])
if not df.empty:
    for col in ["invoice_date", "total_amount", "vendor", "category", "payment_method"]:
        if col not in df.columns:
            df[col] = None
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
else:
    df = pd.DataFrame(columns=["invoice_date", "vendor", "category", "total_amount", "payment_method"])

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🧾 إجمالي الفواتير", stats.get("total_invoices", 0))
with col2:
    st.metric("💰 إجمالي المصروف (ريال)", f"{stats.get('total_spent', 0.0):,.2f}")
with col3:
    avg_per_invoice = 0
    if stats.get("total_invoices", 0) > 0:
        avg_per_invoice = stats["total_spent"] / stats["total_invoices"]
    st.metric("📈 المتوسط لكل فاتورة", f"{avg_per_invoice:.2f} ريال")
with col4:
    top_vendor = stats.get("top_vendors", [{}])
    top_vendor_name = top_vendor[0].get("vendor", "غير متوفر") if top_vendor else "غير متوفر"
    st.metric("🏪 أفضل بائع", top_vendor_name)
with col5:
    st.metric("🗓️ مصروف الشهر الحالي", f"{df['total_amount'].sum():,.2f} ريال")

st.markdown("---")

# Charts
if not df.empty:
    colA, colB = st.columns(2)

    # Top Vendors
    with colA:
        top_vendors = stats.get("top_vendors", [])
        if top_vendors:
            df_vendors = pd.DataFrame(top_vendors)
            if not df_vendors.empty and "vendor" in df_vendors.columns:
                fig = px.bar(
                    df_vendors, x=df_vendors["vendor"], y="count", text_auto=True,
                    color="count", color_continuous_scale="Teal", title="🏪 Top Vendors by Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No vendor data available.")
        else:
            st.info("No vendor data available.")

    # Monthly Trend
    with colB:
        if "invoice_date" in df.columns:
            monthly = df.groupby(df["invoice_date"].dt.to_period("M"))["total_amount"].sum().reset_index()
            monthly["invoice_date"] = monthly["invoice_date"].astype(str)
            fig2 = px.line(monthly, x="invoice_date", y="total_amount", markers=True, title="📈 Monthly Spending Trend")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No date data available.")

    st.markdown("---")

    # Category Spending
    if "category" in df.columns and df["category"].notna().any():
        category_spending = df.groupby("category")["total_amount"].sum().reset_index()
        fig3 = px.pie(category_spending, values="total_amount", names="category", title="🎯 Spending by Category")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No category data available.")

    # Payment Methods
    if "payment_method" in df.columns and df["payment_method"].notna().any():
        payment_methods = df["payment_method"].value_counts().reset_index()
        payment_methods.columns = ["Payment Method", "Count"]
        fig4 = px.pie(payment_methods, values="Count", names="Payment Method", title="💳 Payment Methods Breakdown")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No payment method data available.")

    # Recent Invoices
    st.markdown("### 📋 Recent Invoices")
    display_cols = [c for c in ["invoice_number", "vendor", "category", "total_amount", "payment_method", "invoice_date"] if c in df.columns]
    if display_cols:
        st.dataframe(df[display_cols].tail(10), hide_index=True, use_container_width=True)
    else:
        st.warning("⚠️ No invoice data available yet.")
