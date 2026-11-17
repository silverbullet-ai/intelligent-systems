
"""
data_loader.py
--------------
Handles external dataset uploads for the Retail Sales Insights dashboard.

Supported formats:
    - CSV (.csv)
    - Excel (.xlsx)

Responsibilities:
    - Read uploaded files.
    - Normalize column names.
    - Validate the required schema.
    - Clean invalid records.
    - Generate a data-quality summary.

The output follows the same structure expected by analysis.py.
"""

import os
import re
import warnings

import pandas as pd

from analysis import validate_frame


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "quantity",
    "customer_id",
    "region",
    "segment",
    "signup_date",
    "category",
    "unit_cost",
    "unit_price",
]

SUPPORTED_FORMATS = {".csv", ".xlsx"}

MAX_FILE_SIZE_MB = 50


# ---------------------------------------------------------------------
# Column normalization
# ---------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to lowercase snake_case.

    Examples:
        Order ID       -> order_id
        Customer Name  -> customer_name
        Unit Price     -> unit_price
    """

    df = df.copy()

    normalized = [
        re.sub(
            r"_+",
            "_",
            re.sub(r"[^a-z0-9]+", "_", str(column).strip().lower())
        ).strip("_")
        for column in df.columns
    ]

    if len(normalized) != len(set(normalized)):
        raise ValueError(
            "Duplicate columns detected after normalization. "
            "Please rename the duplicate columns."
        )

    df.columns = normalized

    return df


# ---------------------------------------------------------------------
# File reading
# ---------------------------------------------------------------------

def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    """Read an uploaded CSV or Excel file."""

    if uploaded_file is None:
        raise ValueError("No file was provided.")

    filename = uploaded_file.name
    extension = os.path.splitext(filename)[1].lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Please upload a CSV or XLSX file."
        )

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(
            f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit."
        )

    uploaded_file.seek(0)

    try:
        if extension == ".csv":
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(
                uploaded_file,
                engine="openpyxl",
            )

    except ImportError as error:
        raise RuntimeError(
            "Excel support requires openpyxl. "
            "Install it using: pip install openpyxl"
        ) from error

    except (pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as error:
        raise ValueError(
            f"Unable to read the uploaded file: {error}"
        ) from error

    if df.empty:
        raise ValueError("The uploaded file contains no data.")

    return df


# ---------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------

def validate_schema(df: pd.DataFrame) -> None:
    """Check whether all required columns are present."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )


# ---------------------------------------------------------------------
# Main upload pipeline
# ---------------------------------------------------------------------

def load_uploaded_file(uploaded_file):
    """
    Load, normalize and validate an uploaded dataset.

    Returns:
        cleaned_df: Analysis-ready DataFrame.
        report: Dictionary containing data-quality information.
    """

    raw_df = read_uploaded_file(uploaded_file)

    normalized_df = normalize_columns(raw_df)

    validate_schema(normalized_df)

    total_rows = len(normalized_df)

    # Capture validation warnings for the quality report.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        cleaned_df = validate_frame(normalized_df)

    rejected_rows = total_rows - len(cleaned_df)

    report = {
        "file_name": uploaded_file.name,
        "total_rows": total_rows,
        "valid_rows": len(cleaned_df),
        "rejected_rows": rejected_rows,
        "columns": len(normalized_df.columns),
        "validation_warnings": [
            str(warning.message) for warning in caught
        ],
    }

    if cleaned_df.empty:
        raise ValueError(
            "No valid records remain after data validation. "
            "Please check the uploaded data."
        )

    return cleaned_df, report


# ---------------------------------------------------------------------
# Upload template
# ---------------------------------------------------------------------

def get_upload_template() -> pd.DataFrame:
    """Return an empty DataFrame with the required upload schema."""

    return pd.DataFrame(columns=REQUIRED_COLUMNS)
