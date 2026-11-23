
import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = PROJECT_ROOT / "data" / "raw" / "US_Regional_Sales_Data.csv"
SQL_PATH = PROJECT_ROOT / "sql" / "01_database_setup.sql"
DB_DIR = PROJECT_ROOT / "data" / "database"
DB_PATH = DB_DIR / "us_regional_sales.db"

DB_DIR.mkdir(parents=True, exist_ok=True)

# Validate files
if not CSV_PATH.exists():
    raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

if not SQL_PATH.exists():
    raise FileNotFoundError(f"SQL schema not found: {SQL_PATH}")

# Load CSV
df = pd.read_csv(CSV_PATH)

# Map original CSV column names to SQL column names
column_mapping = {
    "Sales Channel": "SalesChannel",
    "_SalesTeamID": "SalesTeamID",
    "_CustomerID": "CustomerID",
    "_StoreID": "StoreID",
    "_ProductID": "ProductID",
    "Order Quantity": "OrderQuantity",
    "Discount Applied": "DiscountApplied",
    "Unit Cost": "UnitCost",
    "Unit Price": "UnitPrice"
}

df.rename(columns=column_mapping, inplace=True)

# Convert monetary columns to numeric values
monetary_columns = ["UnitCost", "UnitPrice"]

for column in monetary_columns:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(",", "", regex=False),
        errors="raise"
    )

# Create database and import records
with sqlite3.connect(DB_PATH) as connection:

    # Create the table using our SQL schema
    schema = SQL_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)

    # Clear previous records to allow safe re-import
    connection.execute("DELETE FROM regional_sales")

    # Import CSV records into the existing table
    df.to_sql(
        "regional_sales",
        connection,
        if_exists="append",
        index=False
    )

    total_records = connection.execute(
        "SELECT COUNT(*) FROM regional_sales"
    ).fetchone()[0]

print("Database setup completed!")
print(f"Database: {DB_PATH}")
print(f"Imported records: {total_records:,}")
print(f"Columns: {len(df.columns)}")
