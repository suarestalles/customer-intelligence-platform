import os

import streamlit as st

from dashboard.api_client import AnalyticsAPIClient
from dashboard.utils.formatters import format_compact_currency, format_number

API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:8000")

client = AnalyticsAPIClient(API_URL)

st.set_page_config(page_title="Products", page_icon="📦", layout="wide")

st.title("Product Analytics")
st.caption("Product performance and revenue analysis")

try:
    categories_data = client.get_product_categories(limit=100)

except Exception as exc:
    st.error("Unable to connect to the Analytics API.")
    st.exception(exc)
    st.stop()

categories = categories_data["categories"]

category_options = ["All"] + [item["category"] for item in categories if item["category"]]

selected_category = st.selectbox("Category", category_options)

category = None if selected_category == "All" else selected_category

try:
    products_data = client.get_products(category, limit=20)
except Exception as exc:
    st.error("Unable to load Products.")
    st.exception(exc)
    st.stop()

products = products_data["products"]

total_categories = categories_data["total_categories"]
total_products = products_data["total_products"]
total_items = products_data["total_items"]
total_revenue = products_data["total_revenue"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Products", format_number(total_products))

with col2:
    st.metric("Items Sold", format_number(total_items))

with col3:
    st.metric("Revenue", format_compact_currency(total_revenue))

with col4:
    st.metric("Categories", format_number(total_categories))

if selected_category == "All":
    st.divider()

    st.subheader("Revenue By Category")

    if categories:
        category_revenue = {
            item["category"] or "Unknown": item["total_revenue"] for item in categories
        }

        st.bar_chart(category_revenue, sort=False, horizontal=True)

st.divider()

st.subheader("Top Products")

if products:
    product_table = [
        {
            "Product": item["product_id"],
            "Category": item["product_category"] or "Unknown",
            "Revenue": format_compact_currency(item["total_revenue"]),
            "Items Sold": item["total_items"],
            "Orders": item["total_orders"],
            "Average Price": format_compact_currency(item["average_item_price"]),
        }
        for item in products
    ]

    st.dataframe(product_table, width="stretch", hide_index=True)
else:
    st.info("No products found for the selected category.")
