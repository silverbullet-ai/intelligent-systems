"""
analysis.py
-----------
Core business-analysis logic. Pulls from the SQLite database built by
db_setup.py, computes stakeholder-focused KPIs, and generates
plain-English insights.

Run standalone:
    python analysis.py

Also imported by app.py for the Streamlit dashboard and data_loader.py
for validating user-uploaded datasets.
"""

import os
import sqlite3
import warnings
from contextlib import closing

import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "retail.db")


# ---------------------------------------------------------------------
# Schema configuration
# ---------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "quantity",
    "customer_id",
    "unit_cost",
    "unit_price",
]

OPTIONAL_COLUMNS = [
    "region",
    "segment",
    "signup_date",
    "category",
]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def safe_divide(numerator, denominator, default=0):
    """Divide safely, returning default for missing or zero denominators."""
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return default

    return numerator / denominator


def empty_frame(columns: list) -> pd.DataFrame:
    """Return an empty DataFrame with the requested columns."""
    return pd.DataFrame(columns=columns)


# ---------------------------------------------------------------------
# Data validation and preparation
# ---------------------------------------------------------------------

def validate_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean an analysis-ready transaction DataFrame.

    Required fields:
        order_id, order_date, quantity, customer_id, unit_cost, unit_price

    Optional descriptive fields:
        region, segment, signup_date, category

    Missing optional descriptive fields are populated with "Unknown".
    Missing signup dates remain NaT. Invalid transaction records are
    excluded with a warning.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {', '.join(missing)}"
        )

    df = df.copy()
    original_count = len(df)

    # Add optional fields when they are not supplied by the dataset.
    for column in OPTIONAL_COLUMNS:
        if column not in df.columns:
            if column == "signup_date":
                df[column] = pd.NaT
            else:
                df[column] = "Unknown"

    # Convert dates safely.
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )
    df["signup_date"] = pd.to_datetime(
        df["signup_date"], errors="coerce"
    )

    # Convert numeric fields safely.
    numeric_columns = ["quantity", "unit_cost", "unit_price"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Treat whitespace-only identifiers as missing.
    for column in ["order_id", "customer_id"]:
        df[column] = df[column].replace(
            r"^\s*$", pd.NA, regex=True
        )

    # Identify invalid transaction records.
    valid = (
        df["order_id"].notna()
        & df["customer_id"].notna()
        & df["order_date"].notna()
        & df["quantity"].notna()
        & df["unit_cost"].notna()
        & df["unit_price"].notna()
        & (df["quantity"] > 0)
        & (df["unit_cost"] >= 0)
        & (df["unit_price"] >= 0)
    )

    invalid_count = int((~valid).sum())

    if invalid_count:
        invalid_pct = (
            invalid_count / original_count * 100
            if original_count else 0
        )
        warnings.warn(
            f"Excluded {invalid_count} invalid records out of "
            f"{original_count} ({invalid_pct:.1f}%).",
            UserWarning,
            stacklevel=2,
        )

    df = df.loc[valid].copy()

    # Normalize optional descriptive fields.
    descriptive_columns = ["region", "segment", "category"]

    for column in descriptive_columns:
        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype("string")
            .str.strip()
            .replace("", "Unknown")
        )

    # Calculate financial metrics.
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["cost"] = df["quantity"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]

    # Derive calendar month for trend analysis.
    df["order_month"] = (
        df["order_date"].dt.to_period("M").astype(str)
    )

    return df.reset_index(drop=True)


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

def load_joined_frame() -> pd.DataFrame:
    """Join orders, customers and products into one analysis-ready frame."""

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at: {DB_PATH}\n"
            "Run db_setup.py first to create the database."
        )

    query = """
        SELECT
            o.order_id,
            o.order_date,
            o.quantity,
            c.customer_id,
            c.region,
            c.segment,
            c.signup_date,
            p.category,
            p.unit_cost,
            p.unit_price
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
    """

    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            df = pd.read_sql_query(query, conn)

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to retrieve data from the database: {error}"
        ) from error

    return validate_frame(df)


# ---------------------------------------------------------------------
# KPI functions
# ---------------------------------------------------------------------

def kpi_overview(df: pd.DataFrame) -> dict:
    """Calculate the overall business KPIs."""

    if df.empty:
        return {
            "total_revenue": 0,
            "total_profit": 0,
            "margin_pct": 0,
            "avg_order_value": 0,
            "active_customers": 0,
        }

    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()

    margin_pct = safe_divide(
        total_profit, total_revenue
    ) * 100

    order_revenue = df.groupby("order_id")["revenue"].sum()
    avg_order_value = order_revenue.mean()

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "margin_pct": round(margin_pct, 1),
        "avg_order_value": round(avg_order_value, 2),
        "active_customers": int(df["customer_id"].nunique()),
    }


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate revenue, profit and margin for each category."""

    columns = [
        "category", "revenue", "profit", "orders", "margin_pct"
    ]

    if df.empty:
        return empty_frame(columns)

    out = (
        df.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    out["margin_pct"] = (
        out["profit"]
        / out["revenue"].replace(0, float("nan"))
        * 100
    ).fillna(0).round(1)

    return (
        out.sort_values("profit", ascending=False)
        .reset_index(drop=True)
    )


def performance_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate business performance by region."""

    columns = ["region", "revenue", "profit", "customers"]

    if df.empty:
        return empty_frame(columns)

    return (
        df.groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            customers=("customer_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index()
    )


def performance_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate business performance by customer segment."""

    columns = ["segment", "revenue", "profit", "customers"]

    if df.empty:
        return empty_frame(columns)

    return (
        df.groupby("segment")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            customers=("customer_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index()
    )


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly revenue, orders and average order value."""

    columns = [
        "order_month", "revenue", "orders", "avg_order_value"
    ]

    if df.empty:
        return empty_frame(columns)

    out = (
        df.groupby("order_month")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    out["avg_order_value"] = (
        out["revenue"]
        / out["orders"].replace(0, float("nan"))
    ).fillna(0).round(2)

    return out.reset_index(drop=True)


def churn_risk_by_segment(
    df: pd.DataFrame,
    inactivity_days: int = 90,
) -> pd.DataFrame:
    """
    Flag customers as at risk if their most recent order is older than
    inactivity_days relative to the latest order date in the dataset.

    This is a recency-based inactivity proxy, not a predictive churn model.
    """

    if inactivity_days < 0:
        raise ValueError("inactivity_days cannot be negative.")

    columns = ["segment", "customers", "at_risk", "at_risk_pct"]

    if df.empty:
        return empty_frame(columns)

    last_order = (
        df.groupby("customer_id")["order_date"]
        .max()
        .reset_index()
    )

    last_order.columns = ["customer_id", "last_order_date"]

    max_date = df["order_date"].max()

    if pd.isna(max_date):
        return empty_frame(columns)

    last_order["days_since_last_order"] = (
        max_date - last_order["last_order_date"]
    ).dt.days

    last_order["at_risk"] = (
        last_order["days_since_last_order"] > inactivity_days
    )

    seg_map = (
        df[["customer_id", "segment"]]
        .drop_duplicates(subset=["customer_id"])
    )

    merged = last_order.merge(
        seg_map,
        on="customer_id",
        how="left",
    )

    merged["segment"] = merged["segment"].fillna("Unknown")

    out = (
        merged.groupby("segment")
        .agg(
            customers=("customer_id", "count"),
            at_risk=("at_risk", "sum"),
        )
        .reset_index()
    )

    out["at_risk_pct"] = (
        out["at_risk"]
        / out["customers"].replace(0, float("nan"))
        * 100
    ).fillna(0).round(1)

    return (
        out.sort_values("at_risk_pct", ascending=False)
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------
# Insight generation
# ---------------------------------------------------------------------

def generate_insights(df: pd.DataFrame) -> list:
    """Generate stakeholder-friendly business insights."""

    if df.empty:
        return [
            "No business insights available. "
            "The dataset contains no valid order records."
        ]

    insights = []

    # Category insights: only generate when category data is available.
    cat = revenue_by_category(df)
    cat = cat[cat["category"] != "Unknown"]

    if not cat.empty:
        top_profit_cat = cat.iloc[0]

        insights.append(
            f"{top_profit_cat['category']} drives the most profit "
            f"(₹{top_profit_cat['profit']:,.0f}, "
            f"{top_profit_cat['margin_pct']}% margin)."
        )

        lowest_margin_cat = cat.sort_values("margin_pct").iloc[0]

        insights.append(
            f"{lowest_margin_cat['category']} has the thinnest margin "
            f"at {lowest_margin_cat['margin_pct']}% — "
            "worth reviewing supplier cost or pricing."
        )

    # Regional insights: only generate when region data is available.
    region = performance_by_region(df)
    region = region[region["region"] != "Unknown"]

    if not region.empty:
        top_region = region.iloc[0]
        bottom_region = region.iloc[-1]

        insights.append(
            f"{top_region['region']} is the strongest region by revenue "
            f"(₹{top_region['revenue']:,.0f}), while "
            f"{bottom_region['region']} has the lowest revenue "
            f"(₹{bottom_region['revenue']:,.0f})."
        )

    # Churn insights: only generate when segment data is available.
    churn = churn_risk_by_segment(df)
    churn = churn[churn["segment"] != "Unknown"]

    if not churn.empty:
        top_risk_seg = churn.iloc[0]

        insights.append(
            f"{top_risk_seg['segment']} has the highest inactivity-based "
            f"churn risk at {top_risk_seg['at_risk_pct']}% of customers "
            "inactive for more than 90 days."
        )

    # Monthly trend insights.
    trend = monthly_trend(df)

    if len(trend) >= 2:
        last = trend.iloc[-1]
        prev = trend.iloc[-2]

        previous_aov = prev["avg_order_value"]
        current_aov = last["avg_order_value"]

        previous_month = pd.Period(prev["order_month"], freq="M")
        current_month = pd.Period(last["order_month"], freq="M")

        if previous_aov == 0:
            insights.append(
                f"Average order value comparison between "
                f"{prev['order_month']} and {last['order_month']} "
                "is unavailable because the previous month's AOV is zero."
            )
        else:
            change_pct = (
                abs(current_aov - previous_aov)
                / previous_aov
                * 100
            )

            direction = (
                "up" if current_aov >= previous_aov else "down"
            )

            comparison = (
                "month-over-month"
                if current_month.ordinal - previous_month.ordinal == 1
                else "between the latest available months"
            )

            insights.append(
                f"Average order value moved {direction} "
                f"{change_pct:.1f}% {comparison} "
                f"({prev['order_month']} → {last['order_month']})."
            )

    if not insights:
        insights.append(
            "Insufficient data to generate meaningful business insights."
        )

    return insights


# ---------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------

def main():
    try:
        df = load_joined_frame()
        overview = kpi_overview(df)

        print("=== KPI OVERVIEW ===")

        for key, value in overview.items():
            print(f"{key}: {value}")

        print("\n=== BUSINESS INSIGHTS ===")

        for i, insight in enumerate(generate_insights(df), start=1):
            print(f"{i}. {insight}")

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()
