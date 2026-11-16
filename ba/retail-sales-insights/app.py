
"""
app.py
------
Retail Sales Performance & Business Insights Dashboard.

Run:
    streamlit run app.py
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


# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Insights",
    page_icon="📊",
    layout="wide",
)

st.title("Retail Sales Performance & Business Insights")

st.caption(
    "A business-analyst view of raw transaction data: KPIs, segment "
    "performance, and auto-generated insights for stakeholders."
)


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

@st.cache_data
def get_data():
    """Load and cache the analysis-ready dataset."""
    return load_joined_frame()


try:
    df = get_data()

except (FileNotFoundError, RuntimeError, ValueError) as error:
    st.error(f"Unable to load business data: {error}")
    st.info("Please check your database configuration and try again.")
    st.stop()


if df.empty:
    st.warning("No valid transaction records were found.")
    st.info(
        "Please populate the database with valid order, customer, "
        "and product records."
    )
    st.stop()


# ---------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------

with st.sidebar:
    st.header("Filters")

    regions = sorted(df["region"].unique().tolist())
    segments = sorted(df["segment"].unique().tolist())

    selected_regions = st.multiselect(
        "Region",
        options=regions,
        default=regions,
    )

    selected_segments = st.multiselect(
        "Segment",
        options=segments,
        default=segments,
    )

    if st.button("Reset Filters", use_container_width=True):
        st.session_state["Region"] = regions
        st.session_state["Segment"] = segments
        st.rerun()


# ---------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------

filtered = df[
    df["region"].isin(selected_regions)
    & df["segment"].isin(selected_segments)
].copy()


# ---------------------------------------------------------------------
# Empty filter handling
# ---------------------------------------------------------------------

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.info("Try selecting a different region or customer segment.")

    if st.button("Clear Filters"):
        st.session_state["Region"] = regions
        st.session_state["Segment"] = segments
        st.rerun()

    st.stop()


st.caption(
    f"Showing {len(filtered):,} transaction records "
    f"from {filtered['customer_id'].nunique():,} active customers."
)


# ---------------------------------------------------------------------
# KPI overview
# ---------------------------------------------------------------------

st.subheader("Business Performance Overview")

kpis = kpi_overview(filtered)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Revenue",
    f"₹{kpis['total_revenue']:,.0f}",
)

c2.metric(
    "Total Profit",
    f"₹{kpis['total_profit']:,.0f}",
)

c3.metric(
    "Profit Margin",
    f"{kpis['margin_pct']}%",
)

c4.metric(
    "Average Order Value",
    f"₹{kpis['avg_order_value']:,.0f}",
)

c5.metric(
    "Active Customers",
    f"{kpis['active_customers']:,}",
)


st.divider()


# ---------------------------------------------------------------------
# Business insights
# ---------------------------------------------------------------------

st.subheader("Auto-Generated Business Insights")

insights = generate_insights(filtered)

if insights:
    for insight in insights:
        st.markdown(f"- {insight}")
else:
    st.info("No business insights are currently available.")


st.divider()


# ---------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------

st.subheader("Business Analytics")

col1, col2 = st.columns(2)


# ---- Profit by category -----------------------------------------------

with col1:
    st.markdown("#### Profit by Category")

    cat_df = revenue_by_category(filtered)

    if not cat_df.empty:
        fig = px.bar(
            cat_df,
            x="category",
            y="profit",
            color="margin_pct",
            text="profit",
            color_continuous_scale="Blues",
            labels={
                "category": "Category",
                "profit": "Profit (₹)",
                "margin_pct": "Profit Margin (%)",
            },
        )

        fig.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Profit (₹)",
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No category data available.")


# ---- Revenue by region ------------------------------------------------

with col2:
    st.markdown("#### Revenue by Region")

    region_df = performance_by_region(filtered)

    if not region_df.empty:
        fig2 = px.bar(
            region_df,
            x="region",
            y="revenue",
            color="region",
            labels={
                "region": "Region",
                "revenue": "Revenue (₹)",
            },
        )

        fig2.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue (₹)",
            showlegend=False,
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("No regional data available.")


# ---- Monthly revenue trend --------------------------------------------

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Monthly Revenue Trend")

    trend_df = monthly_trend(filtered)

    if not trend_df.empty:
        fig3 = px.line(
            trend_df,
            x="order_month",
            y="revenue",
            markers=True,
            labels={
                "order_month": "Month",
                "revenue": "Revenue (₹)",
            },
        )

        fig3.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue (₹)",
        )

        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("No monthly trend data available.")


# ---- Churn risk by segment --------------------------------------------

with col4:
    st.markdown("#### Customers at Risk of Churning")

    churn_df = churn_risk_by_segment(filtered)

    if not churn_df.empty:
        fig4 = px.bar(
            churn_df,
            x="segment",
            y="at_risk_pct",
            text="at_risk_pct",
            labels={
                "segment": "Customer Segment",
                "at_risk_pct": "At-Risk Customers (%)",
            },
        )

        fig4.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
        )

        fig4.update_layout(
            xaxis_title=None,
            yaxis_title="Customers at Risk (%)",
            yaxis_range=[0, 100],
        )

        st.plotly_chart(fig4, use_container_width=True)

    else:
        st.info("No customer inactivity data available.")


st.divider()


# ---------------------------------------------------------------------
# Segment performance table
# ---------------------------------------------------------------------

st.subheader("Customer Segment Performance")

segment_df = performance_by_segment(filtered)

if not segment_df.empty:
    st.dataframe(
        segment_df,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No segment performance data available.")


# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------

st.divider()

st.caption(
    "Retail Sales Insights | Built with Python, SQLite, Pandas, "
    "Streamlit and Plotly."
)
