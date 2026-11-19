
try:
    from .config_manager import (
        DEFAULT_RULES,
        load_config,
    )
except ImportError:
    from config_manager import (
        DEFAULT_RULES,
        load_config,
    )


def load_rules(config_path=None):
    """
    Load categorization rules through the configuration manager.

    Args:
        config_path: Optional custom JSON configuration path.

    Returns:
        Validated configuration dictionary.
    """

    return load_config(config_path)


def get_category(extension, rules=None):
    """
    Identify the category of a file using its extension.

    Args:
        extension: File extension, such as '.pdf'.
        rules: Optional categorization rules.

    Returns:
        Matching category or the default category.
    """

    if rules is None:
        rules = load_rules()

    extension = extension.lower().strip()

    for category, extensions in rules["categories"].items():

        normalized_extensions = [
            ext.lower() for ext in extensions
        ]

        if extension in normalized_extensions:
            return category

    return rules["default_category"]


def categorize_files(files, rules=None):
    """
    Assign categories to a list of scanned files.

    Args:
        files: List of file metadata dictionaries.
        rules: Optional categorization rules.

    Returns:
        Updated file list with assigned categories.
    """

    if rules is None:
        rules = load_rules()

    for file in files:
        file["category"] = get_category(
            file["extension"],
            rules
        )

    return files


def get_category_summary(files):
    """
    Generate a count of files belonging to each category.

    Args:
        files: List of categorized file dictionaries.

    Returns:
        Dictionary containing category-wise file counts.
    """

    summary = {}

    for file in files:
        category = file["category"]

        summary[category] = summary.get(category, 0) + 1

    return summary
