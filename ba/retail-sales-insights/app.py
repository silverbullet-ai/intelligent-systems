
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

from data_loader import (
    read_uploaded_file,
    load_uploaded_file,
    get_upload_template,
)

from column_mapper import (
    REQUIRED_FIELDS,
    OPTIONAL_FIELDS,
    suggest_column_mapping,
    validate_mapping,
)


# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Insights",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------
# Sidebar drawer entrance animation
# ---------------------------------------------------------------------

st.markdown(
    """
    <style>
    @keyframes sidebarDrawerEnter {
        from {
            opacity: 0;
            transform: translateX(-28px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    section[data-testid="stSidebar"] {
        animation: sidebarDrawerEnter 900ms ease-out both;
    }

    @media (prefers-reduced-motion: reduce) {
        section[data-testid="stSidebar"] {
            animation: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Retail Sales Performance & Business Insights")

st.caption(
    "A self-service business analytics dashboard for exploring "
    "retail performance, customer behaviour and business insights."
)


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

@st.cache_data
def get_database_data():
    """Load and cache the default database dataset."""
    return load_joined_frame()


# ---------------------------------------------------------------------
# Data source selection
# ---------------------------------------------------------------------

with st.sidebar:
    st.header("Data Source")

    data_source = st.radio(
        "Choose data source",
        options=[
            "Sample Database",
            "Upload Your Own Data",
        ],
        key="data_source",
    )

    st.divider()

    template = get_upload_template()

    st.download_button(
        label="Download CSV Template",
        data=template.to_csv(index=False).encode("utf-8"),
        file_name="retail_upload_template.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Load selected dataset
# ---------------------------------------------------------------------

if data_source == "Sample Database":

    try:
        df = get_database_data()

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        st.error(f"Unable to load database: {error}")
        st.stop()

else:

    st.subheader("Upload Your Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
        help="Maximum file size: 50 MB.",
        key="dataset_upload",
    )

    if uploaded_file is None:
        st.info(
            "Upload a CSV or Excel file to begin analysing "
            "your own retail dataset."
        )
        st.stop()

    # -------------------------------------------------------------
    # Read uploaded dataset
    # -------------------------------------------------------------

    try:
        raw_df = read_uploaded_file(uploaded_file)

    except (ValueError, RuntimeError) as error:
        st.error(f"Unable to read uploaded file: {error}")
        st.stop()

    st.success(
        f"File loaded: {uploaded_file.name}"
    )

    st.caption(
        f"{len(raw_df):,} records · "
        f"{len(raw_df.columns)} columns"
    )

    # -------------------------------------------------------------
    # Dataset preview
    # -------------------------------------------------------------

    with st.expander("Preview Uploaded Dataset", expanded=True):

        st.dataframe(
            raw_df.head(10),
            use_container_width=True,
            hide_index=True,
        )

        st.write("Available columns:")

        st.write(", ".join(map(str, raw_df.columns.tolist())))

    st.divider()

    # -------------------------------------------------------------
    # Dynamic column mapping
    # -------------------------------------------------------------

    st.subheader("Map Your Dataset Columns")

    st.write(
        "Match the columns in your uploaded dataset with the "
        "business fields required by our analytics engine."
    )

    st.caption(
        "We automatically suggest mappings when column names "
        "match known aliases. You can change any suggestion."
    )

    suggestions = suggest_column_mapping(
        raw_df.columns.tolist()
    )

    available_columns = [
        "",
        *raw_df.columns.tolist(),
    ]

    mapping = {}

    # -------------------------------------------------------------
    # Mapping form
    # -------------------------------------------------------------

    with st.form("column_mapping_form"):

        st.markdown("#### Mandatory Fields")

        st.caption(
            "These six fields are required to calculate "
            "the core business KPIs."
        )

        for field, config in REQUIRED_FIELDS.items():

            suggested = suggestions.get(field, "")

            default_index = (
                available_columns.index(suggested)
                if suggested in available_columns
                else 0
            )

            mapping[field] = st.selectbox(
                config["label"],
                options=available_columns,
                index=default_index,
                format_func=lambda x: x if x else "-- Select a column --",
                key=f"mapping_{uploaded_file.name}_{field}",
                help="Required for business analysis.",
            )

        st.divider()

        st.markdown("#### Optional Fields")

        st.caption(
            "These fields provide additional analytical dimensions. "
            "Leave them unselected if unavailable."
        )

        for field, config in OPTIONAL_FIELDS.items():

            suggested = suggestions.get(field, "")

            default_index = (
                available_columns.index(suggested)
                if suggested in available_columns
                else 0
            )

            mapping[field] = st.selectbox(
                config["label"],
                options=available_columns,
                index=default_index,
                format_func=lambda x: x if x else "-- Not available --",
                key=f"mapping_{uploaded_file.name}_{field}",
                help="Optional analytical dimension.",
            )

        st.divider()

        submitted = st.form_submit_button(
            "Validate & Load Dataset",
            use_container_width=True,
            type="primary",
        )

    # -------------------------------------------------------------
    # Mapping validation and transformation
    # -------------------------------------------------------------

    if not submitted:
        st.info(
            "Review your column selections and click "
            "'Validate & Load Dataset' to continue."
        )
        st.stop()

    is_valid, errors = validate_mapping(
        mapping,
        raw_df.columns.tolist(),
    )

    if not is_valid:

        st.error("Column mapping validation failed.")

        for error in errors:
            st.write(f"- {error}")

        st.stop()

    # -------------------------------------------------------------
    # Process uploaded dataset
    # -------------------------------------------------------------

    try:

        df, upload_report = load_uploaded_file(
            uploaded_file,
            mapping,
        )

        st.success(
            f"Successfully processed "
            f"{upload_report['valid_rows']:,} valid records."
        )

        # ---------------------------------------------------------
        # Data quality report
        # ---------------------------------------------------------

        with st.expander("Data Quality Report"):

            q1, q2, q3 = st.columns(3)

            q1.metric(
                "Total Rows",
                f"{upload_report['total_rows']:,}",
            )

            q2.metric(
                "Valid Rows",
                f"{upload_report['valid_rows']:,}",
            )

            q3.metric(
                "Rejected Rows",
                f"{upload_report['rejected_rows']:,}",
            )

            st.write(
                f"**Uploaded file:** {upload_report['file_name']}"
            )

            if upload_report["validation_warnings"]:

                st.warning("Data validation warnings:")

                for warning in upload_report["validation_warnings"]:
                    st.write(f"- {warning}")

            else:
                st.success("No invalid records detected.")

            st.write("**Applied column mapping:**")

            mapping_summary = [
                {
                    "Business Field": field,
                    "Uploaded Column": source or "Not mapped",
                }
                for field, source in mapping.items()
            ]

            st.dataframe(
                mapping_summary,
                use_container_width=True,
                hide_index=True,
            )

    except (ValueError, RuntimeError) as error:
        st.error(f"Dataset processing failed: {error}")
        st.stop()


# ---------------------------------------------------------------------
# Final dataset validation
# ---------------------------------------------------------------------

if df.empty:
    st.warning("No valid transaction records are available.")
    st.stop()


# ---------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------

regions = sorted(df["region"].dropna().unique().tolist())
segments = sorted(df["segment"].dropna().unique().tolist())


def reset_filters():
    """Restore all available filter selections."""
    st.session_state["region_filter"] = regions
    st.session_state["segment_filter"] = segments


# Reconcile filter state when switching datasets.
if (
    "region_filter" not in st.session_state
    or not set(st.session_state["region_filter"]).issubset(regions)
):
    st.session_state["region_filter"] = regions

if (
    "segment_filter" not in st.session_state
    or not set(st.session_state["segment_filter"]).issubset(segments)
):
    st.session_state["segment_filter"] = segments


with st.sidebar:

    st.divider()
    st.header("Filters")

    selected_regions = st.multiselect(
        "Region",
        options=regions,
        key="region_filter",
    )

    selected_segments = st.multiselect(
        "Customer Segment",
        options=segments,
        key="segment_filter",
    )

    st.button(
        "Reset Filters",
        on_click=reset_filters,
        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------

filtered = df[
    df["region"].isin(selected_regions)
    & df["segment"].isin(selected_segments)
].copy()


if filtered.empty:

    st.warning("No records match the selected filters.")

    st.info(
        "Try selecting a different region or customer segment."
    )

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
# Business analytics
# ---------------------------------------------------------------------

st.subheader("Business Analytics")

col1, col2 = st.columns(2)


# ---- Profit by category -----------------------------------------------

with col1:

    st.markdown("#### Profit by Category")

    cat_df = revenue_by_category(filtered)

    cat_df = cat_df[
        cat_df["category"] != "Unknown"
    ]

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
                "profit": "Profit",
                "margin_pct": "Profit Margin (%)",
            },
        )

        fig.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Profit",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:
        st.info(
            "Category analysis is unavailable "
            "because no product category was supplied."
        )


# ---- Revenue by region ------------------------------------------------

with col2:

    st.markdown("#### Revenue by Region")

    region_df = performance_by_region(filtered)

    region_df = region_df[
        region_df["region"] != "Unknown"
    ]

    if not region_df.empty:

        fig2 = px.bar(
            region_df,
            x="region",
            y="revenue",
            color="region",
            labels={
                "region": "Region",
                "revenue": "Revenue",
            },
        )

        fig2.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue",
            showlegend=False,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    else:
        st.info(
            "Regional analysis is unavailable "
            "because no region information was supplied."
        )


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
                "revenue": "Revenue",
            },
        )

        fig3.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue",
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    else:
        st.info("No monthly trend data available.")


# ---- Churn risk by segment --------------------------------------------

with col4:

    st.markdown("#### Customers at Risk of Churning")

    churn_df = churn_risk_by_segment(filtered)

    churn_df = churn_df[
        churn_df["segment"] != "Unknown"
    ]

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

        st.plotly_chart(
            fig4,
            use_container_width=True,
        )

    else:
        st.info(
            "Churn-risk segmentation is unavailable "
            "because no customer segment was supplied."
        )


st.divider()


# ---------------------------------------------------------------------
# Customer segment performance
# ---------------------------------------------------------------------

st.subheader("Customer Segment Performance")

segment_df = performance_by_segment(filtered)

segment_df = segment_df[
    segment_df["segment"] != "Unknown"
]

if not segment_df.empty:

    st.dataframe(
        segment_df,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info(
        "Customer segment analysis is unavailable "
        "because no segment information was supplied."
    )


# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------

st.divider()

st.caption(
    "Retail Sales Insights | Built with Python, SQLite, Pandas, "
    "Streamlit and Plotly."
)
