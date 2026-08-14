import os

import pandas as pd
import streamlit as st

from dashboard.api_client import AnalyticsAPIClient
from dashboard.utils.formatters import format_number

API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:8000")

client = AnalyticsAPIClient(API_URL)

st.set_page_config(page_title="Customer Cohorts", page_icon="📈", layout="wide")

st.title("Customer Cohorts")
st.caption("Customer retention and cohort analysis")

try:
    cohorts = client.get_customer_cohorts()

except Exception as exc:
    st.error("Unable to connect to the Analytics API.")
    st.exception(exc)
    st.stop()

if not cohorts:
    st.info("No cohort data available.")
    st.stop()


# -------------------------------------------------------------------
# Data preparation
# -------------------------------------------------------------------

df = pd.DataFrame(cohorts)

df["cohort_month"] = pd.to_datetime(df["cohort_month"])

df = df.sort_values(["cohort_month", "months_since_first_purchase"]).reset_index(drop=True)


# -------------------------------------------------------------------
# KPI calculations
# -------------------------------------------------------------------

total_cohorts = df["cohort_month"].nunique()

largest_cohort = df.groupby("cohort_month")["customers"].first().max()

average_retention_month_1 = df.loc[
    df["months_since_first_purchase"] == 1,
    "retention_rate",
].mean()

average_retention_month_3 = df.loc[
    df["months_since_first_purchase"] == 3,
    "retention_rate",
].mean()


# -------------------------------------------------------------------
# KPI cards
# -------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cohorts",
        format_number(total_cohorts),
    )

with col2:
    st.metric(
        "Largest Cohort",
        format_number(largest_cohort),
    )

with col3:
    if pd.notna(average_retention_month_1):
        st.metric(
            "Avg. Retention M+1",
            f"{average_retention_month_1:.1f}%",
        )
    else:
        st.metric(
            "Avg. Retention M+1",
            "N/A",
        )

with col4:
    if pd.notna(average_retention_month_3):
        st.metric(
            "Avg. Retention M+3",
            f"{average_retention_month_3:.1f}%",
        )
    else:
        st.metric(
            "Avg. Retention M+3",
            "N/A",
        )


st.divider()


# -------------------------------------------------------------------
# Cohort retention chart
# -------------------------------------------------------------------

st.subheader("Retention by Cohort")

chart_data = df.pivot(
    index="cohort_month",
    columns="months_since_first_purchase",
    values="retention_rate",
)

chart_data = chart_data.sort_index()

chart_data.columns = [f"Month {int(month)}" for month in chart_data.columns]

st.line_chart(chart_data)


st.divider()


# -------------------------------------------------------------------
# Cohort retention matrix
# -------------------------------------------------------------------

st.subheader("Cohort Retention Matrix")

retention_matrix = df.pivot(
    index="cohort_month",
    columns="months_since_first_purchase",
    values="retention_rate",
)

retention_matrix = retention_matrix.sort_index()

retention_matrix.index = retention_matrix.index.strftime("%Y-%m")

retention_matrix.columns = [f"Month {int(month)}" for month in retention_matrix.columns]

st.dataframe(
    retention_matrix.style.format(
        "{:.1f}%",
        na_rep="-",
    ),
    width="stretch",
)


st.divider()


# -------------------------------------------------------------------
# Cohort details
# -------------------------------------------------------------------

st.subheader("Cohort Details")

cohort_options = sorted(df["cohort_month"].dt.strftime("%Y-%m").unique())

selected_cohort = st.selectbox(
    "Cohort",
    ["All"] + cohort_options,
)

if selected_cohort != "All":
    selected_date = pd.to_datetime(selected_cohort + "-01")

    cohort_details = df[df["cohort_month"] == selected_date].copy()
else:
    cohort_details = df.copy()


if not cohort_details.empty:
    details_table = [
        {
            "Cohort": row["cohort_month"].strftime("%Y-%m"),
            "Month": int(row["months_since_first_purchase"]),
            "Cohort Size": format_number(row["customers"]),
            "Retained Customers": format_number(row["retained_customers"]),
            "Retention Rate": f"{row['retention_rate']:.1f}%",
        }
        for _, row in cohort_details.iterrows()
    ]

    st.dataframe(
        details_table,
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No cohort data found.")
