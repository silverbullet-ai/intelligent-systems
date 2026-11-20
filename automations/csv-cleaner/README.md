# CSV Cleaner & Report Generator

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A Python-based data cleaning and reporting application that helps users inspect, clean, and improve the quality of CSV datasets. Upload a dataset, review its data quality, configure cleaning options, and download the cleaned dataset along with a detailed data quality report.

**Live Demo:** [Try the Application](https://csv-cleaner-report-generator.streamlit.app/)

---

## Overview

CSV Cleaner & Report Generator is a data preprocessing tool designed to simplify common dataset cleaning tasks.

The application analyzes uploaded CSV files to identify missing values, duplicate records, and column-level data quality issues. Users can then configure cleaning strategies, process their datasets, and generate a report summarizing the operations performed.

The project is designed with a modular architecture, separating data cleaning, report generation, and the user interface.

## Features

- **CSV Upload:** Upload CSV datasets directly through the application.
- **Data Quality Analysis:** Inspect dataset dimensions, missing values, duplicate records, and unique values.
- **Column-Level Analysis:** View data types, missing-value counts, missing percentages, and column statistics.
- **Configurable Data Cleaning:** Choose how missing values should be handled.
- **Duplicate Removal:** Identify and remove duplicate records.
- **Whitespace Handling:** Remove unnecessary whitespace from text columns.
- **Cleaning Summary:** Review the changes made during the cleaning process.
- **Automated Report Generation:** Generate a downloadable text report containing data quality findings and cleaning results.
- **Dataset Export:** Download the cleaned dataset as a CSV file.

## Data Cleaning Options

| Cleaning Operation     | Available Strategies     |
| ---------------------- | ------------------------ |
| Numeric Missing Values | Median, Mean, Zero, None |
| Text Missing Values    | Unknown, Mode, None      |
| Duplicate Records      | Remove / Keep            |
| Whitespace             | Trim / Keep              |

The application also reports missing values that remain after cleaning.

## Tech Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Web Framework:** Streamlit
- **File Handling:** Python Standard Library

## Project Structure

```text
CSV-Cleaner-Report-Generator/
│
├── app.py
├── csv_cleaner.py
├── report_generator.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

| File                    | Description                                 |
| ----------------------- | ------------------------------------------- |
| `app.py`              | Streamlit application and user interface    |
| `csv_cleaner.py`      | Dataset analysis and cleaning functions     |
| `report_generator.py` | Generates data quality and cleaning reports |
| `requirements.txt`    | Project dependencies                        |
| `LICENSE`             | MIT License                                 |
| `.gitignore`          | Files and directories excluded from Git     |

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/silverbullet-ai/intelligent-systems.git
```

### 2. Navigate to the Project Directory

```bash
cd intelligent-systems/automations/csv-cleaner
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Application Workflow

1. Upload a CSV dataset.
2. Review the dataset preview and initial data quality analysis.
3. Configure the cleaning strategies.
4. Run the data cleaning process.
5. Review the cleaning summary and cleaned dataset.
6. Download the cleaned CSV file.
7. Download the generated data quality report.

## Future Improvements

- Support for Excel datasets.
- Additional data validation and cleaning rules.
- Interactive data visualizations.
- Advanced outlier detection.
- Customizable report formats (PDF and Excel).
- Additional statistical analysis options.

## Author

**Aahish Aayan**

AI & Machine Learning Graduate | Aspiring Data Analyst / AI Engineer

GitHub: [Silver Bullet](https://github.com/silverbullet-ai)

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
