"""
CSV Cleaner & Report Generator
Author: Aahish Aayan (https://github.com/silverbullet-ai)
Version: 2.0.0

Reusable CSV loading, data-quality analysis, and cleaning functions.
The Streamlit interface will be implemented separately in app.py.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype

NUMERIC_STRATEGIES = {"median", "mean", "zero", "none"}
TEXT_STRATEGIES = {"unknown", "mode", "none"}


def load_csv(filepath: str | Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame with clear validation errors."""
    path = Path(filepath).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    if path.stat().st_size == 0:
        raise ValueError("The CSV file is empty.")

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The CSV file contains no columns or data.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(f"Unable to parse the CSV file: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError("Unable to decode the CSV file. Check its text encoding.") from exc

    if df.columns.has_duplicates:
        duplicates = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate column names found: {duplicates}")

    print(f"[✓] Loaded '{path.name}' — {len(df):,} rows, {len(df.columns):,} columns\n")
    return df


def analyze(df: pd.DataFrame) -> dict[str, Any]:
    """Return a data-quality summary without modifying the input DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("analyze() expects a pandas DataFrame.")

    columns: dict[str, dict[str, Any]] = {}
    for col in df.columns:
        series = df[col]
        missing = int(series.isna().sum())
        missing_pct = round(missing / len(df) * 100, 1) if len(df) else 0.0
        if missing_pct == 0:
            status = "Clean"
        elif missing_pct < 20:
            status = f"Low missing ({missing_pct}%)"
        else:
            status = f"High missing ({missing_pct}%)"

        columns[str(col)] = {
            "dtype": str(series.dtype),
            "missing": missing,
            "missing_pct": missing_pct,
            "unique_values": int(series.nunique(dropna=True)),
            "status": status,
        }

    return {
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_cells": int(df.isna().sum().sum()),
        "columns": columns,
    }


def _fill_text_values(series: pd.Series, strategy: str) -> pd.Series:
    """Fill missing values in non-numeric, non-datetime columns."""
    if strategy == "none" or not series.isna().any():
        return series
    if strategy == "unknown":
        fill_value = "Unknown"
    elif strategy == "mode":
        modes = series.mode(dropna=True)
        if modes.empty:
            return series
        fill_value = modes.iloc[0]
    else:
        raise ValueError(f"Unsupported text strategy: {strategy}")

    if isinstance(series.dtype, pd.CategoricalDtype):
        if fill_value not in series.cat.categories:
            series = series.cat.add_categories([fill_value])
    return series.fillna(fill_value)


def clean_dataframe(
    df: pd.DataFrame,
    *,
    numeric_strategy: str = "median",
    text_strategy: str = "unknown",
    remove_duplicates: bool = True,
    strip_whitespace: bool = True,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Clean a DataFrame and return (cleaned_dataframe, cleaning_summary).

    Numeric strategies: median, mean, zero, none.
    Text strategies: unknown, mode, none.
    Datetime and boolean columns are left unchanged when values are missing.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("clean_dataframe() expects a pandas DataFrame.")
    if df.columns.has_duplicates:
        raise ValueError("The dataset contains duplicate column names.")
    if numeric_strategy not in NUMERIC_STRATEGIES:
        raise ValueError(f"numeric_strategy must be one of {sorted(NUMERIC_STRATEGIES)}")
    if text_strategy not in TEXT_STRATEGIES:
        raise ValueError(f"text_strategy must be one of {sorted(TEXT_STRATEGIES)}")

    cleaned = df.copy()
    original_rows = len(cleaned)
    missing_before = int(cleaned.isna().sum().sum())
    duplicates_before = int(cleaned.duplicated().sum())
    whitespace_cells_trimmed = 0

    if strip_whitespace:
        for col in cleaned.select_dtypes(include=["object", "string"]).columns:
            original = cleaned[col]
            trimmed = original.str.strip()
            whitespace_cells_trimmed += int((original.notna() & original.ne(trimmed)).sum())
            cleaned[col] = trimmed.replace("", pd.NA)

    if remove_duplicates:
        cleaned = cleaned.drop_duplicates().copy()
    duplicates_removed = original_rows - len(cleaned) if remove_duplicates else 0

    numeric_filled = 0
    text_filled = 0
    columns_without_numeric_values: list[str] = []

    for col in cleaned.columns:
        series = cleaned[col]
        missing_count = int(series.isna().sum())
        if missing_count == 0:
            continue

        if is_datetime64_any_dtype(series.dtype) or is_bool_dtype(series.dtype):
            continue

        if is_numeric_dtype(series.dtype):
            if numeric_strategy == "none":
                continue
            if numeric_strategy == "zero":
                fill_value = 0
            elif numeric_strategy == "median":
                fill_value = series.median()
            else:
                fill_value = series.mean()

            if pd.isna(fill_value):
                columns_without_numeric_values.append(str(col))
                continue
            cleaned[col] = series.fillna(fill_value)
            numeric_filled += missing_count
        else:
            before = missing_count
            cleaned[col] = _fill_text_values(series, text_strategy)
            text_filled += before - int(cleaned[col].isna().sum())

    summary = {
        "original_rows": int(original_rows),
        "cleaned_rows": int(len(cleaned)),
        "original_columns": int(len(df.columns)),
        "duplicates_found": int(duplicates_before),
        "duplicates_removed": int(duplicates_removed),
        "missing_cells_before": int(missing_before),
        "numeric_missing_filled": int(numeric_filled),
        "text_missing_filled": int(text_filled),
        "missing_cells_remaining": int(cleaned.isna().sum().sum()),
        "whitespace_cells_trimmed": int(whitespace_cells_trimmed),
        "numeric_strategy": numeric_strategy,
        "text_strategy": text_strategy,
        "duplicate_removal_enabled": bool(remove_duplicates),
        "whitespace_trimming_enabled": bool(strip_whitespace),
        "columns_without_numeric_values": columns_without_numeric_values,
    }
    return cleaned, summary


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Backward-compatible default cleaner; use clean_dataframe for options and summary."""
    cleaned, _ = clean_dataframe(df)
    return cleaned


def save_cleaned(
    df: pd.DataFrame,
    original_path: str | Path,
    output_path: str | Path | None = None,
) -> str:
    """Save cleaned data without overwriting the original input."""
    original = Path(original_path)
    destination = Path(output_path) if output_path else original.with_name(f"{original.stem}_cleaned.csv")
    if destination.resolve() == original.resolve():
        raise ValueError("Output path must not overwrite the original CSV.")
    df.to_csv(destination, index=False)
    print(f"[✓] Cleaned CSV saved → {destination}")
    return str(destination)


def print_report(report: dict[str, Any]) -> None:
    """Print a readable data-quality report to the terminal."""
    print("=" * 72)
    print("  CSV DATA QUALITY REPORT")
    print("=" * 72)
    print(f"  Rows          : {report['total_rows']:,}")
    print(f"  Columns       : {report['total_columns']:,}")
    print(f"  Duplicates    : {report['duplicate_rows']:,}")
    print(f"  Missing cells : {report['total_missing_cells']:,}\n")
    print(f"  {'Column':<24} {'Type':<16} {'Missing':<10} {'Unique':<10} Status")
    print("  " + "-" * 88)
    for col, info in report["columns"].items():
        print(
            f"  {col[:22]:<24} {info['dtype'][:14]:<16} "
            f"{info['missing']:<10} {info['unique_values']:<10} {info['status']}"
        )
    print()


def run(filepath: str | Path) -> None:
    """Run the default command-line pipeline."""
    df = load_csv(filepath)
    print("Analyzing data...")
    report = analyze(df)
    print_report(report)

    print("Cleaning data...")
    cleaned, summary = clean_dataframe(df)
    save_cleaned(cleaned, filepath)

    print("\nCLEANING SUMMARY")
    print("-" * 30)
    print(f"  Duplicate rows removed : {summary['duplicates_removed']:,}")
    print(f"  Numeric missing filled : {summary['numeric_missing_filled']:,}")
    print(f"  Text missing filled    : {summary['text_missing_filled']:,}")
    print(f"  Missing cells remaining: {summary['missing_cells_remaining']:,}")
    print("\n[✓] All done!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze and clean a CSV file.")
    parser.add_argument("filepath", help="Path to the input CSV file")
    args = parser.parse_args()
    try:
        run(args.filepath)
    except (FileNotFoundError, ValueError, PermissionError) as exc:
        parser.exit(status=1, message=f"[!] Error: {exc}\n")


if __name__ == "__main__":
    main()
