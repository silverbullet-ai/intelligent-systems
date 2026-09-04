"""
analysis.py
-----------
Core business-analysis logic. Pulls from the SQLite database built by
db_setup.py, computes KPIs a stakeholder actually cares about, and
generates plain-English insights from them (not just raw numbers).

Run standalone: python analysis.py   -> prints a KPI + insight summary.
Also imported by app.py for the Streamlit dashboard.
"""

import os
import sqlite3
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "retail.db")


def load_joined_frame() -> pd.DataFrame:
    """Join orders + customers + products into one analysis-ready frame."""
    conn = sqlite3.connect(DB_PATH)
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
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["cost"] = df["quantity"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


# ---------------------------------------------------------------------
# KPI functions
# ---------------------------------------------------------------------

def kpi_overview(df: pd.DataFrame) -> dict:
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    margin_pct = (total_profit / total_revenue * 100) if total_revenue else 0
    avg_order_value = df.groupby("order_id")["revenue"].sum().mean()
    active_customers = df["customer_id"].nunique()
    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "margin_pct": round(margin_pct, 1),
        "avg_order_value": round(avg_order_value, 2),
        "active_customers": active_customers,
    }


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("category")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .assign(margin_pct=lambda d: (d["profit"] / d["revenue"] * 100).round(1))
        .sort_values("profit", ascending=False)
        .reset_index()
    )
    return out


def performance_by_region(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("region")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), customers=("customer_id", "nunique"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    return out


def performance_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("segment")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), customers=("customer_id", "nunique"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    return out


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("order_month")
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("order_month")
    )
    out["avg_order_value"] = (out["revenue"] / out["orders"]).round(2)
    return out


def churn_risk_by_segment(df: pd.DataFrame, inactivity_days: int = 90) -> pd.DataFrame:
    """
    Flags customers as 'at risk' if their most recent order is older than
    `inactivity_days` relative to the latest date in the dataset — a simple
    recency-based churn proxy, the kind of first-pass metric a BA proposes
    before a data-science team builds a full churn model.
    """
    last_order = df.groupby("customer_id")["order_date"].max().reset_index()
    last_order.columns = ["customer_id", "last_order_date"]
    max_date = df["order_date"].max()
    last_order["days_since_last_order"] = (max_date - last_order["last_order_date"]).dt.days
    last_order["at_risk"] = last_order["days_since_last_order"] > inactivity_days

    seg_map = df[["customer_id", "segment"]].drop_duplicates()
    merged = last_order.merge(seg_map, on="customer_id")

    out = (
        merged.groupby("segment")
        .agg(customers=("customer_id", "count"), at_risk=("at_risk", "sum"))
        .assign(at_risk_pct=lambda d: (d["at_risk"] / d["customers"] * 100).round(1))
        .sort_values("at_risk_pct", ascending=False)
        .reset_index()
    )
    return out


# ---------------------------------------------------------------------
# Insight generation — turns numbers into stakeholder-ready sentences
# ---------------------------------------------------------------------

def generate_insights(df: pd.DataFrame) -> list:
    insights = []

    cat = revenue_by_category(df)
    top_profit_cat = cat.iloc[0]
    insights.append(
        f"{top_profit_cat['category']} drives the most profit "
        f"(₹{top_profit_cat['profit']:,.0f}, {top_profit_cat['margin_pct']}% margin), "
        f"even though it may not be the top category by raw revenue."
    )
    lowest_margin_cat = cat.sort_values("margin_pct").iloc[0]
    insights.append(
        f"{lowest_margin_cat['category']} has the thinnest margin at "
        f"{lowest_margin_cat['margin_pct']}% — worth reviewing supplier cost or pricing."
    )

    region = performance_by_region(df)
    top_region = region.iloc[0]
    bottom_region = region.iloc[-1]
    insights.append(
        f"{top_region['region']} is the strongest region by revenue "
        f"(₹{top_region['revenue']:,.0f}), while {bottom_region['region']} lags at "
        f"₹{bottom_region['revenue']:,.0f} — a candidate for a targeted marketing push."
    )

    churn = churn_risk_by_segment(df)
    top_risk_seg = churn.iloc[0]
    insights.append(
        f"{top_risk_seg['segment']} has the highest churn risk this period at "
        f"{top_risk_seg['at_risk_pct']}% of customers inactive 90+ days — "
        f"a retention campaign here would have outsized impact."
    )

    trend = monthly_trend(df)
    if len(trend) >= 2:
        last, prev = trend.iloc[-1], trend.iloc[-2]
        direction = "up" if last["avg_order_value"] >= prev["avg_order_value"] else "down"
        change_pct = abs(last["avg_order_value"] - prev["avg_order_value"]) / prev["avg_order_value"] * 100
        insights.append(
            f"Average order value moved {direction} {change_pct:.1f}% month-over-month "
            f"({prev['order_month']} → {last['order_month']})."
        )

    return insights


def main():
    df = load_joined_frame()
    overview = kpi_overview(df)

    print("=== KPI OVERVIEW ===")
    for k, v in overview.items():
        print(f"{k}: {v}")

    print("\n=== BUSINESS INSIGHTS ===")
    for i, insight in enumerate(generate_insights(df), start=1):
        print(f"{i}. {insight}")


if __name__ == "__main__":
    main()
