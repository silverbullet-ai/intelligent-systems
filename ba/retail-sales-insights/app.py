"""
app.py
------
Stakeholder-facing dashboard for the Retail Sales Performance & Business
Insights project. Run after generate_data.py and db_setup.py.

Run: streamlit run app.py
"""

import streamlit as st
import plotly.express as px

from analysis import (
    load_joined_frame,
    kpi_overview,
    revenue_by_category,
    performance_by_region,
    performance_by_segment,
    monthly_trend,
    churn_risk_by_segment,
    generate_insights,
)

st.set_page_config(page_title="Retail Sales Insights", layout="wide")
st.title("Retail Sales Performance & Business Insights")
st.caption(
    "A business-analyst view of raw transaction data: KPIs, segment "
    "performance, and auto-generated insights for stakeholders."
)

df = load_joined_frame()

# ---- Filters -----------------------------------------------------------
with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=list(df["region"].unique()))
    segments = st.multiselect("Segment", sorted(df["segment"].unique()), default=list(df["segment"].unique()))

filtered = df[df["region"].isin(regions) & df["segment"].isin(segments)]

# ---- KPI row -------------------------------------------------------------
kpis = kpi_overview(filtered)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"₹{kpis['total_revenue']:,.0f}")
c2.metric("Total Profit", f"₹{kpis['total_profit']:,.0f}")
c3.metric("Margin %", f"{kpis['margin_pct']}%")
c4.metric("Avg Order Value", f"₹{kpis['avg_order_value']:,.0f}")
c5.metric("Active Customers", kpis["active_customers"])

st.divider()

# ---- Insights -------------------------------------------------------------
st.subheader("Auto-Generated Business Insights")
for insight in generate_insights(filtered):
    st.markdown(f"- {insight}")

st.divider()

# ---- Charts -------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Profit by Category")
    cat_df = revenue_by_category(filtered)
    fig = px.bar(cat_df, x="category", y="profit", color="margin_pct", text="profit")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Region")
    region_df = performance_by_region(filtered)
    fig2 = px.bar(region_df, x="region", y="revenue", color="region")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Monthly Revenue Trend")
    trend_df = monthly_trend(filtered)
    fig3 = px.line(trend_df, x="order_month", y="revenue", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Churn Risk by Segment")
    churn_df = churn_risk_by_segment(filtered)
    fig4 = px.bar(churn_df, x="segment", y="at_risk_pct", text="at_risk_pct")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Segment Performance (table)")
st.dataframe(performance_by_segment(filtered), use_container_width=True)
