# frontend/pages/Dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ------------------------------------------------------
# ⚙️ Page Config
# ------------------------------------------------------
st.set_page_config(page_title="📊 Invoice Dashboard", layout="wide")

st.title("📊 Invoice Dashboard")
st.caption("Real-time analytics of your invoices with insights powered by AI ⚙️")

BACKEND_URL = "http://127.0.0.1:8000"

# ------------------------------------------------------
# 📡 Fetch Data from Backend
# ------------------------------------------------------
try:
    stats_response = requests.get(f"{BACKEND_URL}/dashboard/stats", timeout=5)
    invoices_response = requests.get(f"{BACKEND_URL}/invoices/all", timeout=5)

    if stats_response.status_code == 200:
        stats = stats_response.json()
    else:
        stats = {"total_invoices": 0, "total_spent": 0.0, "top_vendors": []}

    if invoices_response.status_code == 200:
        invoices = invoices_response.json()
    else:
        invoices = []
except Exception as e:
    st.error(f"❌ Failed to connect to backend: {e}")
    stats = {"total_invoices": 0, "total_spent": 0.0, "top_vendors": []}
    invoices = []

# ------------------------------------------------------
# 🧮 Data Processing
# ------------------------------------------------------
df = pd.DataFrame(invoices if isinstance(invoices, list) else [invoices])
if not df.empty:
    # Ensure required columns exist
    for col in ["invoice_date", "total_amount", "vendor", "category", "payment_method"]:
        if col not in df.columns:
            df[col] = None

    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
else:
    df = pd.DataFrame(columns=["invoice_date", "vendor", "category", "total_amount", "payment_method"])

# ------------------------------------------------------
# 💡 KPI Section
# ------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🧾 Total Invoices", stats.get("total_invoices", 0))
with col2:
    st.metric("💰 Total Spent (SAR)", f"{stats.get('total_spent', 0.0):,.2f}")
with col3:
    avg_per_invoice = 0
    if stats.get("total_invoices", 0) > 0:
        avg_per_invoice = stats["total_spent"] / stats["total_invoices"]
    st.metric("📈 Average per Invoice", f"{avg_per_invoice:.2f} SAR")
with col4:
    top_vendor = stats.get("top_vendors", [{}])
    top_vendor_name = top_vendor[0].get("vendor", "N/A") if top_vendor else "N/A"
    st.metric("🏪 Top Vendor", top_vendor_name)
with col5:
    st.metric("🗓️ Current Month Spend", f"{df['total_amount'].sum():,.2f} SAR", "+0.0% vs last month")

st.markdown("---")

# ------------------------------------------------------
# 📊 Charts Section
# ------------------------------------------------------
if not df.empty:
    colA, colB = st.columns(2)

    # 🏪 Top Vendors Chart
    with colA:
        top_vendors = stats.get("top_vendors", [])
        if top_vendors:
            df_vendors = pd.DataFrame(top_vendors)
            if not df_vendors.empty and "vendor" in df_vendors.columns:
                fig = px.bar(
                    df_vendors,
                    x=df_vendors.index,
                    y="count",
                    text_auto=True,
                    color="count",
                    color_continuous_scale="Teal",
                    title="🏪 Top Vendors by Frequency"
                )
                fig.update_layout(xaxis_title="Vendor", yaxis_title="Count", height=350)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No vendor data available yet.")
        else:
            st.info("No vendor data available yet.")

    # 📈 Monthly Trend
    with colB:
        if "invoice_date" in df.columns:
            monthly = df.groupby(df["invoice_date"].dt.to_period("M"))["total_amount"].sum().reset_index()
            monthly["invoice_date"] = monthly["invoice_date"].astype(str)
            fig2 = px.line(monthly, x="invoice_date", y="total_amount", markers=True, title="📈 Monthly Spending Trend")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No date data available.")

    st.markdown("---")

    # 🎯 Spending by Category
    if "category" in df.columns and df["category"].notna().any():
        category_spending = df.groupby("category")["total_amount"].sum().reset_index()
        fig3 = px.pie(category_spending, values="total_amount", names="category", title="🎯 Spending by Category")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No category data available.")

    # 💳 Payment Methods Breakdown
    if "payment_method" in df.columns and df["payment_method"].notna().any():
        payment_methods = df["payment_method"].value_counts().reset_index()
        payment_methods.columns = ["Payment Method", "Count"]
        fig4 = px.pie(payment_methods, values="Count", names="Payment Method", title="💳 Payment Methods Breakdown")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No payment method data available.")

    # 🗂 Recent Invoices
    st.markdown("### 📋 Recent Invoices")
    display_cols = [c for c in ["invoice_number", "vendor", "category", "total_amount", "payment_method", "invoice_date"] if c in df.columns]
    if display_cols:
        st.dataframe(df[display_cols].tail(10), hide_index=True, use_container_width=True)
else:
    st.warning("⚠️ No invoice data available yet.")
