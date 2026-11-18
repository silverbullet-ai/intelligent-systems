
"""
data_loader.py
--------------
Handles external dataset uploads for the Retail Sales Insights dashboard.

Supported formats:
    - CSV (.csv)
    - Excel (.xlsx)

Responsibilities:
    - Read uploaded files.
    - Accept user-defined column mappings.
    - Transform datasets into the standard analytical schema.
    - Validate and clean records.
    - Generate a data-quality report.

The output follows the standardized structure expected by analysis.py.
"""

import os
import warnings

import pandas as pd

from analysis import (
    validate_frame,
    REQUIRED_COLUMNS,
    OPTIONAL_COLUMNS,
)

from column_mapper import transform_dataset


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SUPPORTED_FORMATS = {".csv", ".xlsx"}

MAX_FILE_SIZE_MB = 50


# ---------------------------------------------------------------------
# File reading
# ---------------------------------------------------------------------

def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    """
    Read an uploaded CSV or Excel file.

    Returns:
        Raw DataFrame containing the original column names.
    """

    if uploaded_file is None:
        raise ValueError("No file was provided.")

    filename = uploaded_file.name

    extension = os.path.splitext(filename)[1].lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Please upload a CSV or XLSX file."
        )

    # Check file size.
    file_size = getattr(uploaded_file, "size", None)

    if file_size is not None:
        file_size_mb = file_size / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(
                f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit."
            )

    uploaded_file.seek(0)

    try:

        if extension == ".csv":
            df = pd.read_csv(
                uploaded_file,
                encoding="utf-8-sig",
            )

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

    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        ValueError,
    ) as error:
        raise ValueError(
            f"Unable to read the uploaded file: {error}"
        ) from error

    except Exception as error:
        raise ValueError(
            f"An error occurred while reading the uploaded file: {error}"
        ) from error

    finally:
        uploaded_file.seek(0)

    if df.empty:
        raise ValueError(
            "The uploaded file contains no data."
        )

    if len(df.columns) != len(set(df.columns)):
        raise ValueError(
            "Duplicate column names detected. "
            "Please resolve duplicate columns before uploading."
        )

    return df


# ---------------------------------------------------------------------
# Main upload pipeline
# ---------------------------------------------------------------------

def load_uploaded_file(uploaded_file, mapping: dict):
    """
    Load, map, transform and validate an uploaded dataset.

    Args:
        uploaded_file: Streamlit UploadedFile object.
        mapping: User-defined mapping between source and standard columns.

    Returns:
        cleaned_df: Analysis-ready DataFrame.
        report: Dictionary containing data-quality information.
    """

    # Step 1: Read original dataset.
    raw_df = read_uploaded_file(uploaded_file)

    total_rows = len(raw_df)

    # Step 2: Transform using user-defined column mapping.
    mapped_df = transform_dataset(
        raw_df,
        mapping,
    )

    # Step 3: Validate and clean the transformed dataset.
    with warnings.catch_warnings(record=True) as caught:

        warnings.simplefilter("always")

        cleaned_df = validate_frame(mapped_df)

    # Step 4: Calculate data-quality statistics.
    valid_rows = len(cleaned_df)

    rejected_rows = total_rows - valid_rows

    # Step 5: Generate data-quality report.
    report = {
        "file_name": uploaded_file.name,
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "rejected_rows": rejected_rows,
        "columns": len(raw_df.columns),
        "validation_warnings": [
            str(warning.message)
            for warning in caught
        ],
        "mapped_columns": mapping.copy(),
    }

    # Step 6: Ensure valid records remain.
    if cleaned_df.empty:
        raise ValueError(
            "No valid records remain after data validation. "
            "Please review your uploaded dataset and column mappings."
        )

    return cleaned_df, report


# ---------------------------------------------------------------------
# Upload template
# ---------------------------------------------------------------------

def get_upload_template() -> pd.DataFrame:
    """
    Return an empty DataFrame containing all standard analytical fields.

    Users can download this template to understand the expected
    structure of the analytical dataset.
    """

    template_columns = [
        *REQUIRED_COLUMNS,
        *OPTIONAL_COLUMNS,
    ]

    return pd.DataFrame(columns=template_columns)
