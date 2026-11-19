
"""
CSV Cleaner & Report Generator
Author: Aahish Aayan (https://github.com/silverbullet-ai)
Version: 2.0.0

Streamlit application for CSV data-quality analysis,
configurable data cleaning, and report generation.
"""

from pathlib import Path
from io import BytesIO

import pandas as pd
import streamlit as st

from csv_cleaner import analyze, clean_dataframe
from report_generator import generate_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CSV Cleaner & Report Generator",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS
# ============================================================

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def read_uploaded_csv(uploaded_file):
    """Read and validate an uploaded CSV file."""

    if uploaded_file is None:
        raise ValueError("Please upload a CSV file.")

    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File exceeds the {MAX_FILE_SIZE_MB} MB upload limit."
        )

    try:
        uploaded_file.seek(0)

        df = pd.read_csv(uploaded_file)

    except pd.errors.EmptyDataError as error:
        raise ValueError(
            "The uploaded CSV file is empty or contains no columns."
        ) from error

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Unable to parse the CSV file: {error}"
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            "Unable to decode the CSV file. "
            "Please check its encoding."
        ) from error

    except Exception as error:
        raise ValueError(
            f"Unable to read the uploaded file: {error}"
        ) from error

    if len(df.columns) == 0:
        raise ValueError("The uploaded file contains no columns.")

    if df.columns.has_duplicates:
        raise ValueError(
            "The dataset contains duplicate column names."
        )

    return df


def format_number(value):
    """Format numbers for dashboard metrics."""
    return f"{value:,}"


def get_download_filename(filename, suffix):
    """Create a download filename from the uploaded file."""
    stem = Path(filename).stem
    return f"{stem}_{suffix}.csv"


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title("🧹 CSV Cleaner & Report Generator")

st.caption(
    "Analyze, clean, and transform your CSV datasets "
    "with automated data-quality reporting."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help=f"Maximum file size: {MAX_FILE_SIZE_MB} MB.",
    )

    st.divider()

    st.markdown("### About")

    st.caption(
        "CSV Cleaner & Report Generator helps identify "
        "data-quality issues, clean datasets, and generate "
        "downloadable reports."
    )

    st.markdown("---")

    st.caption(
        "Built by Aahish Aayan"
    )

    st.caption(
        "github.com/silverbullet-ai"
    )


# ============================================================
# FILE UPLOAD HANDLING
# ============================================================

if uploaded_file is None:

    st.info(
        "Upload a CSV file using the sidebar to begin."
    )

    st.markdown("### What you can do")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔍 Data Analysis")
        st.write(
            "Identify missing values, duplicate records, "
            "data types, and unique values."
        )

    with col2:
        st.markdown("#### 🧹 Data Cleaning")
        st.write(
            "Remove duplicates, trim whitespace, "
            "and handle missing values."
        )

    with col3:
        st.markdown("#### 📄 Report Generation")
        st.write(
            "Generate a detailed report and download "
            "your cleaned dataset."
        )

    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

try:

    df = read_uploaded_csv(uploaded_file)

except ValueError as error:

    st.error(str(error))
    st.stop()


if df.empty:

    st.warning(
        "The uploaded dataset contains no records."
    )

    st.stop()


st.success(
    f"Successfully loaded: {uploaded_file.name}"
)

st.caption(
    f"{len(df):,} rows · {len(df.columns):,} columns"
)


# ============================================================
# ORIGINAL DATASET PREVIEW
# ============================================================

st.subheader("📋 Dataset Preview")

with st.expander("View Uploaded Dataset", expanded=True):

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"Showing first 10 of {len(df):,} records."
    )


st.divider()


# ============================================================
# DATA QUALITY ANALYSIS
# ============================================================

st.subheader("🔍 Data Quality Analysis")

analysis = analyze(df)

# Overall metrics

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Total Rows",
    format_number(analysis["total_rows"]),
)

metric2.metric(
    "Total Columns",
    format_number(analysis["total_columns"]),
)

metric3.metric(
    "Duplicate Rows",
    format_number(analysis["duplicate_rows"]),
)

metric4.metric(
    "Missing Cells",
    format_number(analysis["total_missing_cells"]),
)


# Column-level analysis

st.markdown("#### Column-Level Analysis")

column_records = []

for column, details in analysis["columns"].items():

    column_records.append({
        "Column": column,
        "Data Type": details["dtype"],
        "Missing Values": details["missing"],
        "Missing (%)": details["missing_pct"],
        "Unique Values": details["unique_values"],
        "Status": details["status"],
    })


quality_df = pd.DataFrame(column_records)

st.dataframe(
    quality_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# CLEANING CONFIGURATION
# ============================================================

st.divider()

st.subheader("⚙️ Configure Data Cleaning")

st.write(
    "Choose how the application should handle missing values "
    "and duplicate records."
)


config_col1, config_col2 = st.columns(2)


with config_col1:

    st.markdown("#### Numeric Missing Values")

    numeric_strategy = st.selectbox(
        "Select numeric replacement strategy",
        options=["median", "mean", "zero", "none"],
        index=0,
        help=(
            "Median and mean use the column's existing "
            "valid numeric values."
        ),
    )


with config_col2:

    st.markdown("#### Text Missing Values")

    text_strategy = st.selectbox(
        "Select text replacement strategy",
        options=["unknown", "mode", "none"],
        index=0,
        help=(
            "Unknown replaces missing values with 'Unknown'. "
            "Mode uses the most frequent existing value."
        ),
    )


option_col1, option_col2 = st.columns(2)


with option_col1:

    remove_duplicates = st.checkbox(
        "Remove duplicate records",
        value=True,
    )


with option_col2:

    strip_whitespace = st.checkbox(
        "Trim leading and trailing whitespace",
        value=True,
    )


st.divider()


# ============================================================
# EXECUTE CLEANING
# ============================================================

st.subheader("🧹 Clean Dataset")

st.write(
    "Once you are satisfied with the configuration, "
    "run the cleaning process."
)


if st.button(
    "Run Data Cleaning",
    type="primary",
    use_container_width=True,
):

    try:

        with st.spinner("Cleaning your dataset..."):

            cleaned_df, cleaning_summary = clean_dataframe(
                df,
                numeric_strategy=numeric_strategy,
                text_strategy=text_strategy,
                remove_duplicates=remove_duplicates,
                strip_whitespace=strip_whitespace,
            )

            report_text = generate_report(
                analysis,
                cleaning_summary,
                filename=uploaded_file.name,
            )

            st.session_state["cleaned_df"] = cleaned_df
            st.session_state["cleaning_summary"] = cleaning_summary
            st.session_state["report_text"] = report_text
            st.session_state["processed_filename"] = uploaded_file.name
            st.session_state["processed_file_id"] = (
                uploaded_file.name,
                uploaded_file.size,
            )

        st.success("Dataset cleaning completed successfully!")

    except (ValueError, TypeError) as error:

        st.error(f"Cleaning failed: {error}")
        st.stop()


# ============================================================
# CLEANING RESULTS
# ============================================================

current_file_id = (
    uploaded_file.name,
    uploaded_file.size,
)

if st.session_state.get("processed_file_id") != current_file_id:
    st.info("Run data cleaning to view results and downloads.")
    st.stop()


if "cleaned_df" not in st.session_state:
    st.stop()


cleaned_df = st.session_state["cleaned_df"]

cleaning_summary = st.session_state["cleaning_summary"]

report_text = st.session_state["report_text"]


# ============================================================
# CLEANING SUMMARY
# ============================================================

st.divider()

st.subheader("📊 Cleaning Summary")

result1, result2, result3, result4 = st.columns(4)

result1.metric(
    "Original Rows",
    format_number(cleaning_summary["original_rows"]),
)

result2.metric(
    "Cleaned Rows",
    format_number(cleaning_summary["cleaned_rows"]),
    delta=(
        cleaning_summary["cleaned_rows"]
        - cleaning_summary["original_rows"]
    ),
)

result3.metric(
    "Duplicates Removed",
    format_number(cleaning_summary["duplicates_removed"]),
)

result4.metric(
    "Missing Cells Remaining",
    format_number(cleaning_summary["missing_cells_remaining"]),
)


# Additional cleaning statistics

st.markdown("#### Cleaning Operations")

operation_col1, operation_col2 = st.columns(2)

with operation_col1:

    st.write(
        f"**Numeric values filled:** "
        f"{cleaning_summary['numeric_missing_filled']:,}"
    )

    st.write(
        f"**Text values filled:** "
        f"{cleaning_summary['text_missing_filled']:,}"
    )

with operation_col2:

    st.write(
        f"**Whitespace cells trimmed:** "
        f"{cleaning_summary['whitespace_cells_trimmed']:,}"
    )

    st.write(
        f"**Duplicate rows found:** "
        f"{cleaning_summary['duplicates_found']:,}"
    )


if cleaning_summary["columns_without_numeric_values"]:

    st.warning(
        "Some numeric columns had no valid values "
        "available for calculating replacements: "
        + ", ".join(
            cleaning_summary["columns_without_numeric_values"]
        )
    )


# ============================================================
# CLEANED DATASET PREVIEW
# ============================================================

st.divider()

st.subheader("✨ Cleaned Dataset Preview")

st.dataframe(
    cleaned_df.head(20),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    f"Showing first 20 of {len(cleaned_df):,} cleaned records."
)


# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.divider()

st.subheader("📥 Download Results")

st.write(
    "Your cleaned dataset and data-quality report "
    "are ready for download."
)


download_col1, download_col2 = st.columns(2)


cleaned_csv = cleaned_df.to_csv(
    index=False
).encode("utf-8-sig")


with download_col1:

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=cleaned_csv,
        file_name=get_download_filename(
            uploaded_file.name,
            "cleaned",
        ),
        mime="text/csv",
        use_container_width=True,
    )


with download_col2:

    st.download_button(
        label="⬇️ Download Analysis Report",
        data=report_text.encode("utf-8"),
        file_name=(
            f"{Path(uploaded_file.name).stem}_report.txt"
        ),
        mime="text/plain",
        use_container_width=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CSV Cleaner & Report Generator v2.0 | "
    "Built with Python, Pandas and Streamlit."
)

st.caption(
    "© 2026 Silver Bullet | "
    "github.com/silverbullet-ai"
)
