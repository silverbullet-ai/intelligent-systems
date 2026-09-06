# Retail Sales Performance \& Business Insights Dashboard

A business-analyst style project that turns raw retail transaction data into
stakeholder-ready KPIs, trend analysis, and written business insights.

## What this project demonstrates

* **Requirements gathering → KPI definition**: translated a set of stakeholder
questions ("Which regions are underperforming?", "Are we retaining
customers?") into concrete, measurable KPIs.
* **Data modeling**: a normalized SQLite schema (customers, products, orders)
built from raw CSV data, queried with SQL.
* **Analysis \& reporting**: Python/Pandas logic that computes revenue,
margin, churn, and segment performance, then auto-generates plain-English
business insights (not just numbers).
* **Stakeholder-facing output**: an interactive Streamlit dashboard so
non-technical stakeholders can self-serve answers instead of waiting on
ad-hoc reports.

## Project structure

```
ba-project/
├── analysis.py          # core BA logic: KPIs, segmentation, insight generation
├── app.py               # Streamlit dashboard (stakeholder-facing view)
├── requirements.txt
└── data/                # CSVs + SQLite db land here
```

## How to run

```bash
pip install -r requirements.txt
python analysis.py           # prints KPI + insight summary to console
streamlit run app.py         # launches the interactive dashboard
```

## Sample business questions this answers

1. Which product category drives the most profit, not just revenue?
2. Which customer segment has the highest churn risk this quarter?
3. Which region should get the next marketing budget increase?
4. Is average order value trending up or down month over month?

