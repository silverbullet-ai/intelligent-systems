# 📊 Retail Sales Performance & Business Insights Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

An interactive, business-analyst-style application that transforms raw retail transaction data into stakeholder-ready KPIs, performance trends, customer insights, and business recommendations.

The dashboard supports both a sample SQLite database and user-uploaded datasets, making retail performance analysis more flexible and accessible.

## Live Application

**[Open Retail Sales Insights Dashboard](https://retail-sales-insight.streamlit.app/)**

Explore the dashboard, upload your own retail dataset, and interact with business performance metrics.

## Project Overview

This project demonstrates how raw transactional data can be transformed into meaningful business intelligence through data processing, analytical modelling, KPI development, and interactive visualisation.

### What this project demonstrates

- **Business Requirements & KPI Definition:** Translated stakeholder questions into measurable business metrics and analytical requirements.
- **Data Modelling:** Designed and queried a normalized SQLite database containing customer, product, and order information.
- **Data Processing & Validation:** Implemented data cleaning, validation, transformation, and quality checks using Python and Pandas.
- **Dynamic Column Mapping:** Developed a flexible mapping system that allows users to upload datasets with different column names and map them to the dashboard's standard analytical schema.
- **Business Analytics:** Calculated revenue, profit, profit margin, average order value, customer activity, and segment performance.
- **Automated Business Insights:** Generated plain-English insights to help interpret analytical findings.
- **Interactive Reporting:** Built a Streamlit dashboard that allows stakeholders to explore business performance without writing SQL or Python queries.

## Key Features

### 1. Multiple Data Sources

- Analyse data from the integrated SQLite sample database.
- Upload custom CSV and Excel (`.xlsx`) datasets.
- Support for uploaded files up to 50 MB.

### 2. Dynamic Column Mapping

- Automatically suggests mappings based on recognised column names.
- Allows users to manually map mandatory and optional business fields.
- Supports datasets with different naming conventions.
- Validates mappings before processing.

### 3. Data Quality & Validation

- Checks required fields and data types.
- Handles missing and invalid transaction records.
- Identifies rejected records.
- Provides a data quality report after upload.

### 4. Business Performance KPIs

- Total Revenue
- Total Profit
- Profit Margin
- Average Order Value (AOV)
- Active Customers

### 5. Business Analytics

- Profit by Product Category
- Revenue by Region
- Monthly Revenue Trends
- Customer Churn-Risk Analysis
- Customer Segment Performance

### 6. Automated Business Insights

Generates written insights from analytical results to help stakeholders understand performance patterns and identify areas requiring attention.

### 7. Interactive Dashboard

- Region-based filtering
- Customer-segment filtering
- Reset filters functionality
- Interactive Plotly visualisations
- CSV upload template for custom datasets

## 🛠️ Technology Stack

| Technology   | Purpose                                     |
| ------------ | ------------------------------------------- |
| Python       | Core programming and business logic         |
| Pandas       | Data cleaning, transformation, and analysis |
| NumPy        | Numerical operations                        |
| SQLite       | Relational database management              |
| SQL          | Data querying and joins                     |
| Streamlit    | Interactive dashboard                       |
| Plotly       | Data visualisation                          |
| OpenPyXL     | Excel file processing                       |
| Git & GitHub | Version control and project management      |

## Project Structure

```text
retail-sales-insights/
│
├── app.py                  # Streamlit dashboard
├── analysis.py             # KPIs, analytics, and insight generation
├── data_loader.py          # CSV/Excel ingestion and validation
├── column_mapper.py        # Dynamic dataset column mapping
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
└── data/
    └── retail.db           # Sample SQLite database
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or later
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/silverbullet-ai/intelligent-systems/tree/main/ba/retail-sales-insights
```

### 2. Navigate to the project directory

```bash
cd retail-sales-insights
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Dependencies

```text
pandas>=2.0
numpy>=1.24
streamlit>=1.30
plotly>=5.18
openpyxl
```

## Sample Business Questions

The dashboard is designed to help answer questions such as:

1. Which product category generates the highest profit rather than simply the highest revenue?
2. Which customer segment has the highest proportion of customers at risk of churning?
3. Which regions contribute most to overall revenue?
4. Is average order value increasing or decreasing over time?
5. How is business performance changing month over month?
6. Which areas require further business investigation?

## Analytical Approach

The project follows an end-to-end analytical workflow:

```text
Raw Transaction Data
        |
        v
Data Ingestion
        |
        v
Column Mapping & Validation
        |
        v
Data Cleaning & Transformation
        |
        v
Database / Analytical Processing
        |
        v
KPI Calculation & Business Analysis
        |
        v
Automated Insight Generation
        |
        v
Interactive Streamlit Dashboard
```

## Project Objective

The primary objective is to demonstrate the practical application of data analytics and business analysis techniques in transforming raw retail transaction data into actionable business intelligence.

Rather than presenting isolated charts and metrics, the project focuses on connecting data, business questions, measurable KPIs, and stakeholder-facing insights.

---

👨‍💻 Author & Maintainer

Aahish Aayan
AI & Machine Learning Graduate | Aspiring Data Analyst / AI Engineer

GitHub: @silverbullet-ai

🤝 Contributions

Suggestions, bug reports, and improvements are welcome.

If you find an issue or have an idea to improve the project, feel free to open an issue or submit a pull request.

📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

---

**Built with Python, Pandas, SQL, Streamlit, and Plotly.**
