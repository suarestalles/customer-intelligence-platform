import os

import streamlit as st

from dashboard.api_client import AnalyticsAPIClient
from dashboard.utils.formatters import (
    format_compact_currency,
    format_currency,
    format_date,
    format_decimal,
    format_number,
)

API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:8000")

client = AnalyticsAPIClient(API_URL)

st.set_page_config(page_title="Customers", page_icon="👥", layout="wide")

st.title("Customer Analytics")
st.caption("Customer behavior and segmentation")

try:
    summary = client.get_customer_summary()
    segments = client.get_segments()

except Exception as exc:
    st.error("Unable to connect to the Analytics API.")
    st.exception(exc)
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Customers", format_number(summary["total_customers"]))

with col2:
    st.metric("Revenue", format_compact_currency(summary["total_revenue"]))

with col3:
    st.metric("Average Spend", format_currency(summary["average_spend"]))

with col4:
    st.metric("Average Orders", format_decimal(summary["average_orders"]))

st.divider()

st.subheader("Customer Segments")

if segments:
    segment_data = {item["segment"]: item["customers"] for item in segments}

    st.bar_chart(segment_data, sort=False)

st.divider()

st.subheader("Customers")

segment_options = ["All"] + [item["segment"] for item in segments]

selected_segment = st.selectbox("Segment", segment_options)

segment = None if selected_segment == "All" else selected_segment

try:
    customer_data = client.get_customers(segment, 50)

except Exception as exc:
    st.error("Unable to load customers.")
    st.exception(exc)
    st.stop()

customers = customer_data

if customers:
    customer_table = [
        {
            "Customer": item["customer_id"],
            "Total Orders": format_number(item["total_orders"]),
            "Total Items": format_number(item["total_items"]),
            "Total Spent": format_compact_currency(item["total_spent"]),
            "Average Order Value": format_compact_currency(item["average_order_value"]),
            "First Order Date": format_date(item["first_order_date"]),
            "Last Order Date": format_date(item["last_order_date"]),
            "Customer Lifetime Days": format_number(item["customer_lifetime_days"]),
        }
        for item in customers
    ]

    st.dataframe(customer_table, width="stretch", hide_index=True)
else:
    st.info("No customers found for the selected segment.")
