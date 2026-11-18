
"""
column_mapper.py
----------------
Dynamic column mapping for user-uploaded retail datasets.

Responsibilities:
    - Define the standard analytical schema.
    - Suggest mappings based on column names.
    - Validate user-selected mappings.
    - Transform uploaded datasets into a standardized DataFrame.
"""

import pandas as pd


# ---------------------------------------------------------------------
# Standard analytical schema
# ---------------------------------------------------------------------

REQUIRED_FIELDS = {
    "order_id": {
        "label": "Order ID",
        "aliases": ["order_id", "ordernumber", "order_number", "orderid"],
    },
    "order_date": {
        "label": "Order Date",
        "aliases": ["order_date", "orderdate", "transaction_date"],
    },
    "quantity": {
        "label": "Quantity",
        "aliases": ["quantity", "qty", "order_quantity", "units_sold"],
    },
    "customer_id": {
        "label": "Customer ID",
        "aliases": ["customer_id", "customerid", "customercode"],
    },
    "unit_cost": {
        "label": "Unit Cost",
        "aliases": ["unit_cost", "cost", "cost_price", "purchase_price"],
    },
    "unit_price": {
        "label": "Unit Price",
        "aliases": ["unit_price", "selling_price", "sale_price"],
    },
}

OPTIONAL_FIELDS = {
    "region": {
        "label": "Region",
        "aliases": ["region", "customer_region", "territory"],
    },
    "segment": {
        "label": "Customer Segment",
        "aliases": ["segment", "customer_segment"],
    },
    "signup_date": {
        "label": "Signup Date",
        "aliases": ["signup_date", "registration_date", "join_date"],
    },
    "category": {
        "label": "Product Category",
        "aliases": ["category", "product_category", "product_type"],
    },
}


# ---------------------------------------------------------------------
# Automatic mapping suggestions
# ---------------------------------------------------------------------

def normalize_name(name: str) -> str:
    """Normalize a column name for matching."""

    return "".join(
        character.lower()
        for character in str(name)
        if character.isalnum()
    )


def suggest_column_mapping(columns: list) -> dict:
    """
    Suggest source columns for each standard analytical field.

    Suggestions are based on exact normalized alias matches.
    Users can override these suggestions.
    """

    normalized_columns = {
        normalize_name(column): column
        for column in columns
    }

    mapping = {}

    all_fields = {
        **REQUIRED_FIELDS,
        **OPTIONAL_FIELDS,
    }

    for field, config in all_fields.items():

        suggestion = None

        for alias in config["aliases"]:
            normalized_alias = normalize_name(alias)

            if normalized_alias in normalized_columns:
                suggestion = normalized_columns[normalized_alias]
                break

        mapping[field] = suggestion or ""

    return mapping


# ---------------------------------------------------------------------
# Mapping validation
# ---------------------------------------------------------------------

def validate_mapping(
    mapping: dict,
    available_columns: list,
) -> tuple:
    """
    Validate the selected column mapping.

    Returns:
        is_valid: Boolean.
        errors: List of validation errors.
    """

    errors = []

    available_fields = {
        **REQUIRED_FIELDS,
        **OPTIONAL_FIELDS,
    }

    # Check mandatory mappings.
    for field, config in REQUIRED_FIELDS.items():

        selected = mapping.get(field, "")

        if not selected:
            errors.append(
                f"{config['label']} must be mapped."
            )

        elif selected not in available_columns:
            errors.append(
                f"Selected column for {config['label']} "
                "does not exist in the uploaded dataset."
            )

    # Check optional selections.
    for field in OPTIONAL_FIELDS:

        selected = mapping.get(field, "")

        if selected and selected not in available_columns:
            errors.append(
                f"Selected column for "
                f"{available_fields[field]['label']} "
                "does not exist."
            )

    # Check duplicate source selections.
    selected_columns = [
        mapping[field]
        for field in available_fields
        if mapping.get(field)
    ]

    if len(selected_columns) != len(set(selected_columns)):
        errors.append(
            "A source column cannot be assigned to multiple fields."
        )

    return len(errors) == 0, errors


# ---------------------------------------------------------------------
# Dataset transformation
# ---------------------------------------------------------------------

def transform_dataset(
    df: pd.DataFrame,
    mapping: dict,
) -> pd.DataFrame:
    """
    Transform an uploaded dataset into the standard analytical schema.

    Optional fields are filled with appropriate defaults when unmapped.
    """

    is_valid, errors = validate_mapping(
        mapping,
        df.columns.tolist(),
    )

    if not is_valid:
        raise ValueError(
            "Invalid column mapping: " + "; ".join(errors)
        )

    # Select mapped source columns.
    selected_columns = {
        source: target
        for target, source in mapping.items()
        if source
    }

    transformed = df[
        list(selected_columns.keys())
    ].copy()

    # Rename source columns to standard field names.
    transformed = transformed.rename(
        columns=selected_columns
    )

    # Populate missing optional dimensions.
    for field in OPTIONAL_FIELDS:

        if field not in transformed.columns:

            if field == "signup_date":
                transformed[field] = pd.NaT

            else:
                transformed[field] = "Unknown"

    # Ensure consistent output column order.
    standard_columns = [
        *REQUIRED_FIELDS.keys(),
        *OPTIONAL_FIELDS.keys(),
    ]

    return transformed[standard_columns]
