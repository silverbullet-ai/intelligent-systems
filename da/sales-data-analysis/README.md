* [ ] 

# US Regional Sales Analysis

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Analysis-4479A1?style=for-the-badge)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

An end-to-end sales data analytics project using Python, SQLite, SQL, and Power BI to investigate sales performance, profitability, discount risk, and fulfillment efficiency.

The project transforms raw transaction data into validated business metrics, detailed SQL analysis, and an interactive four-page Power BI report.

## Project Overview

Sales data can reveal more than total revenue. Understanding profitability, discounting, customer and product contribution, and fulfillment performance helps explain how sales are being generated and where potential risks exist.

This project analyzes the US Regional Sales dataset to answer business questions across four areas:

- **Sales Performance:** How are sales, profit, and order volume performing over time?
- **Sales & Profitability:** Which channels, warehouses, products, customers, teams, and stores contribute most to sales and profit?
- **Discount & Loss Analysis:** How are discount levels associated with profitability and loss-making orders?
- **Fulfillment Performance:** How long does order processing and shipping take, and how does fulfillment vary across channels and warehouses?

The focus is on building a reproducible analytical workflow and presenting findings through an interactive Power BI dashboard.

## Dataset

**Source:** [US Regional Sales Data — Kaggle](https://www.kaggle.com/datasets/talhabu/us-regional-sales-data)

The dataset contains transaction-level sales records with order dates, sales channels, warehouse codes, product/customer/store/team identifiers, quantities, discounts, unit costs, and unit prices.

| Dataset characteristic | Value |
| ---------------------- | ----: |
| Records                | 7,991 |
| Columns                |    16 |
| Unique order numbers   | 7,991 |
| Products               |    47 |
| Customers              |    50 |
| Sales teams            |    28 |
| Stores                 |   367 |
| Warehouses             |     6 |
| Currency               |   USD |

The dataset includes sales from 2018 to 2020. May 2018 contains only a small partial-month sample, so it is excluded from complete-month trend and month-over-month comparisons.

> **Data limitation:** The available dataset contains numeric IDs for products, customers, stores, and sales teams, but does not provide descriptive names or geographic region details for those entities. The analysis therefore uses the available IDs and warehouse codes without assigning unsupported names or locations.

## Tools & Technologies

| Tool             | Purpose                                                     |
| ---------------- | ----------------------------------------------------------- |
| Python           | Data inspection, preparation, and validation                |
| Pandas           | Data manipulation and analysis                              |
| Jupyter Notebook | Exploratory analysis and Python validation                  |
| SQLite           | Local analytical database                                   |
| SQL              | Business analysis, aggregations, CTEs, and window functions |
| Power BI         | Interactive dashboard and DAX measures                      |
| Git & GitHub     | Version control and project documentation                   |

## Analytical Workflow

```text
Raw Sales CSV
     │
     ▼
Data Inspection & Validation
     │
     ▼
Python Data Preparation
     │
     ▼
SQLite Database
     │
     ▼
SQL Business Analysis
     │
     ▼
Python / SQL Validation
     │
     ▼
Power BI Data Model & DAX
     │
     ▼
Interactive Sales Dashboard
     │
     ▼
Business Insights
```

### 1. Data Inspection & Preparation

- Inspected the raw dataset and its 16 columns.
- Reviewed data types, missing values, duplicate order numbers, and numerical fields.
- Standardized column names for consistent use across Python, SQL, and Power BI.
- Converted monetary fields containing comma-separated values into numeric types.
- Validated the imported data before analysis.

### 2. SQLite Database

The prepared sales data is stored in a local SQLite database.

A Python loading script creates and refreshes the `regional_sales` table using the project SQL schema.

### 3. SQL Business Analysis

The SQL analysis is organized into 13 modules covering:

1. Database Setup
2. Data Validation
3. Overall Performance
4. Sales Channel Analysis
5. Monthly Sales Analysis
6. Warehouse Analysis
7. Product Analysis
8. Customer Analysis
9. Sales Team Analysis
10. Store Analysis
11. Discount & Profitability Analysis
12. Fulfillment Analysis
13. Business Insights

The project uses **Common Table Expressions (CTEs)** to organize multi-step calculations and **window functions** for month-over-month comparisons and cumulative contribution analysis.

### 4. Power BI Dashboard

The Power BI report contains four interactive pages:

| Page                     | Focus                                                              |
| ------------------------ | ------------------------------------------------------------------ |
| Executive Overview       | KPI scorecard, monthly sales and growth, overall performance       |
| Sales & Profitability    | Channel, warehouse, product, customer, team, and store performance |
| Discount & Loss Analysis | Discount distribution, profitability, and loss-making orders       |
| Fulfillment Performance  | Processing, shipping, and total fulfillment duration               |

The report includes DAX measures and slicers for interactive filtering by year, sales channel, and warehouse.

## KPI Definitions

The following calculations are used throughout the project.

| KPI                       | Calculation                        |
| ------------------------- | ---------------------------------- |
| Gross Sales               | Order Quantity × Unit Price       |
| Discount Amount           | Gross Sales × Discount Applied    |
| Net Sales                 | Gross Sales − Discount Amount     |
| Total Cost                | Order Quantity × Unit Cost        |
| Profit                    | Net Sales − Total Cost            |
| Profit Margin             | Profit ÷ Net Sales                |
| Average Order Value       | Net Sales ÷ Orders                |
| Weighted Average Discount | Discount Amount ÷ Gross Sales     |
| Loss Order Rate           | Loss-Making Orders ÷ Total Orders |
| Total Fulfillment Time    | Delivery Date − Order Date        |

**Calculation assumption:** `DiscountApplied` is treated as a discount rate, and profit is calculated as net sales minus total cost. These are analytical assumptions based on the available fields, not verified accounting definitions from the dataset provider.

Fulfillment durations are measured in elapsed calendar days. Processing time and shipping duration are separate stages; procurement lead time overlaps with order processing and is not added to total fulfillment time.

## Key Findings

### Overall Performance

| Metric                    |      Result |
| ------------------------- | ----------: |
| Total Orders              |       7,991 |
| Total Quantity            |      36,162 |
| Gross Sales               |     $82.69M |
| Discount Amount           |      $9.55M |
| Net Sales                 |     $73.14M |
| Total Cost                |     $51.82M |
| Total Profit              |     $21.33M |
| Profit Margin             |      29.16% |
| Weighted Average Discount |      11.55% |
| Average Order Value       |   $9,153.22 |
| Loss-Making Orders        | 372 (4.66%) |
| Average Fulfillment Time  |  20.67 days |

### Sales Channel Performance

- **In-Store** generated the highest net sales and total profit, contributing approximately 41% of both.
- **Wholesale** recorded the highest profit margin at 30.26%.
- **Online** had the lowest channel margin at 28.42% and the highest weighted average discount at 11.90%.
- **Distributor** had the highest average order value at $9,577.56.

### Product & Entity Contribution

- Product 23 generated the highest product-level net sales: **$2.10M**.
- Customer 12 generated the highest customer-level net sales: **$2.01M**.
- Sales Team 26 generated the highest team-level net sales: **$2.98M**.
- Store 284 generated the highest store-level net sales: **$435.63K**.
- Product sales were broadly distributed: 36 of 47 products were needed to account for approximately 80% of product sales.

### Discount & Profitability

- Orders with discounts below 10% had a combined profit margin of **33.28%**.
- Orders discounted at 20–29.99% had a margin of **21.32%**.
- Orders discounted at 30% or more had a margin of only **4.64%**.
- The 30%+ discount group accounted for **94.40% of the total loss amount**.
- The 40% discount category had a negative overall profit margin of **−2.03%**.

Discount levels show a negative association with profitability in this dataset. This is an observed relationship and does not establish that discounts alone caused lower profit.

### Fulfillment Performance

| Fulfillment metric     |    Average |
| ---------------------- | ---------: |
| Order Processing Time  | 15.17 days |
| Shipping Duration      |  5.50 days |
| Total Fulfillment Time | 20.67 days |

Order processing accounts for approximately 73.38% of total fulfillment time, while shipping accounts for 26.62%.

## Project Structure

```text
sales-data-analysis/
│
├── data/
│   ├── raw/
│   │   └── US_Regional_Sales_Data.csv
│   ├── processed/
|   |	└── US_Regional_Sales_Analysis.xlsx
│   ├── database/
│   │   └── us_regional_sales.db
│   └── sql_results/
│       ├── discount_profitability.csv
│       ├── module_02_queries.csv
│       ├── module_03_queries.csv
│       ├── module_04_queries.csv
│       ├── ...
│       └── module_13_queries.csv
│
├── notebooks/
│   ├── 01_data_inspection.ipynb
│   └── 02_sales_analysis.ipynb
│
├── powerbi/
│   └── US_Regional_Sales_Analysis.pbix
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_data_validation.sql
│   ├── ...
│   ├── 13_business_insights.sql
│   └── test.sql
│
├── src/
│   └── load_data_to_sqlite.py
│
├── .gitignore
├── learning.ipynb
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- [ ] Python 3.12
- [ ] Git
- [ ] Power BI Desktop
- [ ] A SQLite-compatible SQL editor or the SQLite extension in VS Code

### 1. Clone the Repository

```bash
git clone https://github.com/silverbullet-ai/intelligent-systems.git
cd intelligent-systems/da/sales-data-analysis
```

### 2. Create a Python Environment

```bash
conda create -n data-ai python=3.12
conda activate data-ai
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Dataset

Download the dataset from Kaggle and place the CSV file in:

```text
data/raw/US_Regional_Sales_Data.csv
```

### 5. Load the Data into SQLite

From the project directory, run:

```bash
python src/load_data_to_sqlite.py
```

The script creates or refreshes the SQLite database using the project schema.

### 6. Run the Analysis

- Open the notebooks in Jupyter or VS Code and run them sequentially.
- Open the SQL modules and execute them against `data/database/us_regional_sales.db`.
- Open `powerbi/US_Regional_Sales_Analysis.pbix` in Power BI Desktop to explore the interactive report.

## Skills Demonstrated

- Data inspection and validation
- Data preparation with Pandas
- SQL querying and business analysis
- CTEs and window functions
- KPI development and financial metric calculations
- Trend and contribution analysis
- Profitability and discount-risk analysis
- DAX measures and Power BI data modeling
- Interactive dashboard design
- Cross-validation between Python, SQL, and Power BI
- Git and GitHub project organization

## Limitations & Notes

- The analysis is based on the fields available in the source dataset.
- Descriptive product, customer, sales team, store, and geographic metadata is not available in the supplied transaction file.
- Profit calculations depend on the stated analytical assumptions.
- Small differences of approximately one cent may occur between SQL and Python due to floating-point arithmetic.
- The project is descriptive and diagnostic; it does not claim causal effects or use predictive forecasting models.

## Author

**Aahish Aayan**
AIML Graduate | Aspiring Data Scientist & AI Engineer

GitHub: [silverbullet-ai](https://github.com/silverbullet-ai)
