import os

import streamlit as st

from dashboard.api_client import AnalyticsAPIClient
from dashboard.utils.formatters import format_compact_currency, format_currency, format_number

API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:8000")

client = AnalyticsAPIClient(API_URL)

st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="📊",
    layout="wide",
)

st.title("Customer Intelligence Platform")
st.caption("E-commerce Analytics Dashboard")

try:
    kpis = client.get_kpis()
    revenue = client.get_revenue()
    segments = client.get_segments()
except Exception as exc:
    st.error("Unable to connect to the Analytics API.")
    st.exception(exc)
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue", format_compact_currency(kpis["total_revenue"]))

with col2:
    st.metric("Orders", format_number(kpis["total_orders"]))

with col3:
    st.metric("Customers", format_number(kpis["total_customers"]))

with col4:
    st.metric("Average Order Value", format_currency(kpis["average_order_value"]))

st.divider()

st.subheader("Revenue Over Time")

monthly_revenue = revenue["monthly"]

if monthly_revenue:
    chart_data = {item["month"]: item["revenue"] for item in monthly_revenue}

    st.line_chart(chart_data)

st.divider()

st.subheader("Customer Segments")

if segments:
    segment_data = {item["segment"]: item["customers"] for item in segments}

    st.bar_chart(
        segment_data,
        horizontal=True,
        sort=False,
    )
