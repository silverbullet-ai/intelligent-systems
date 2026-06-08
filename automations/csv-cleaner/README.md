# CSV Cleaner & Report Generator

A Python-based utility that automates CSV data cleaning, analysis, and report generation.

This tool helps transform raw datasets into analysis-ready data by identifying data quality issues, handling missing values, removing duplicates, and generating summary reports.

---

## Features

- Load CSV files automatically
- Analyze dataset structure and quality
- Detect missing values
- Detect duplicate rows
- Remove duplicate records
- Fill missing numeric values using median
- Fill missing text values with "Unknown"
- Strip unnecessary whitespace from text columns
- Generate a detailed data quality report
- Export cleaned CSV files

---

## Project Structure

```text
csv-cleaner/
│
├── csv_cleaner.py
├── sample_sales.csv
├── sample_sales_cleaned.csv
├── sample_sales_report.txt
└── README.md
```

---

## How It Works

### Input

Raw CSV file:

```text
sample_sales.csv
```

Example issues:

- Missing values
- Duplicate rows
- Inconsistent formatting
- Extra whitespace

### Processing

The script performs:

1. Dataset Analysis
   - Row count
   - Column count
   - Missing values
   - Duplicate records
   - Data types
   - Unique value counts

2. Data Cleaning
   - Remove duplicate rows
   - Fill missing numeric values using median
   - Fill missing string values with "Unknown"
   - Strip whitespace from text columns

3. Report Generation
   - Dataset summary
   - Column-wise statistics
   - Missing value analysis
   - Data quality status

### Output

Cleaned Dataset:

```text
sample_sales_cleaned.csv
```

Analysis Report:

```text
sample_sales_report.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/csv-cleaner.git
cd csv-cleaner
```

Install dependencies:

```bash
pip install pandas
```

---

## Usage

Run the script:

```bash
python csv_cleaner.py sample_sales.csv
```

Example:

```bash
python csv_cleaner.py sales_data.csv
```

---

## Sample Output

```text
[✓] Loaded 'sales_data.csv'

Analyzing data...

Rows          : 1000
Columns       : 8
Duplicates    : 5
Missing cells : 24

Cleaning data...

[✓] Removed 5 duplicate row(s)
[✓] Missing values filled

[✓] Cleaned CSV saved
[✓] Report saved

[✓] All done!
```

---

## Technologies Used

- Python
- Pandas
- CSV Processing
- Data Cleaning
- Data Analysis

---

## Learning Outcomes

This project demonstrates:

- Data preprocessing
- Data quality assessment
- Handling missing values
- Duplicate detection
- Automated reporting
- Working with Pandas DataFrames

---

## Author

**Aahish Aayan (Silver Bullet)**

---