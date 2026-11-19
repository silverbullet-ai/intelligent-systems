
import json

from pathlib import Path
from copy import deepcopy


DEFAULT_RULES = {
    "categories": {
        "Documents": [
            ".pdf", ".doc", ".docx", ".txt",
            ".xlsx", ".xls", ".ppt", ".pptx",
            ".csv", ".odt", ".rtf"
        ],
        "Images": [
            ".jpg", ".jpeg", ".png", ".gif",
            ".svg", ".webp", ".bmp", ".tiff",
            ".ico"
        ],
        "Videos": [
            ".mp4", ".mkv", ".mov", ".avi",
            ".wmv", ".flv", ".webm", ".m4v"
        ],
        "Audio": [
            ".mp3", ".wav", ".aac", ".flac",
            ".ogg", ".wma", ".m4a"
        ],
        "Archives": [
            ".zip", ".rar", ".7z", ".tar",
            ".gz", ".bz2"
        ],
        "Installers": [
            ".exe", ".msi", ".msix", ".appx"
        ],
        "Code": [
            ".py", ".java", ".cpp", ".c",
            ".js", ".html", ".css", ".sql",
            ".json", ".xml", ".ipynb",
            ".php", ".ts", ".jsx", ".tsx"
        ]
    },
    "default_category": "Miscellaneous"
}


def get_config_path():
    """Return the default configuration file path."""

    project_root = Path(__file__).resolve().parent.parent

    return project_root / "config" / "rules.json"


def validate_config(config):
    """
    Validate configuration structure and values.

    Rejects duplicate extensions across categories.
    """

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a JSON object.")

    categories = config.get("categories")
    default_category = config.get("default_category")

    if not isinstance(categories, dict):
        raise ValueError("Categories must be a JSON object.")

    if not isinstance(default_category, str) or not default_category.strip():
        raise ValueError("Default category must be a non-empty string.")

    if default_category.strip() in categories:
        raise ValueError(
            "Default category must not duplicate an existing category."
        )

    used_extensions = set()

    for category, extensions in categories.items():

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category names must be non-empty strings.")

        if category.strip() != category:
            raise ValueError("Category names cannot have surrounding spaces.")

        if not isinstance(extensions, list):
            raise ValueError(
                f"Extensions for {category} must be a list."
            )

        for extension in extensions:

            if not isinstance(extension, str):
                raise ValueError(
                    f"Invalid extension in category: {category}"
                )

            extension = extension.strip().lower()

            if (
                not extension.startswith(".")
                or extension == "."
                or "/" in extension
                or "\\" in extension
                or any(character.isspace() for character in extension)
            ):
                raise ValueError(
                    f"Invalid extension '{extension}' in {category}."
                )

            if extension in used_extensions:
                raise ValueError(
                    f"Extension '{extension}' is assigned more than once."
                )

            used_extensions.add(extension)

    return True


def load_config(config_path=None):
    """Load and validate configuration from JSON."""

    if config_path is None:
        config_path = get_config_path()

    config_path = Path(config_path)

    if not config_path.exists():
        return deepcopy(DEFAULT_RULES)

    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)

        validate_config(config)

        return config

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise ValueError(
            f"Could not load configuration: {error}"
        ) from error


def save_config(config, config_path=None):
    """Validate and safely save configuration to JSON."""

    if config_path is None:
        config_path = get_config_path()

    config_path = Path(config_path)

    validate_config(config)

    config_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary_path = config_path.with_suffix(".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(
                config,
                file,
                indent=4,
                ensure_ascii=False
            )

        temporary_path.replace(config_path)

    except OSError:
        if temporary_path.exists():
            temporary_path.unlink(missing_ok=True)

        raise


def add_category(category, config=None, config_path=None):
    """Add a new empty category."""

    if config is None:
        config = load_config(config_path)

    category = category.strip() if isinstance(category, str) else ""

    if not category:
        raise ValueError("Category name cannot be empty.")

    if category in config["categories"]:
        raise ValueError("Category already exists.")

    if category == config["default_category"]:
        raise ValueError("Category already exists as the default category.")

    updated_config = deepcopy(config)
    updated_config["categories"][category] = []

    save_config(updated_config, config_path)

    return updated_config


def remove_category(category, config=None, config_path=None):
    """Remove an existing category."""

    if config is None:
        config = load_config(config_path)

    if category not in config["categories"]:
        raise ValueError("Category does not exist.")

    if category == config["default_category"]:
        raise ValueError("Cannot remove the default category.")

    updated_config = deepcopy(config)
    del updated_config["categories"][category]

    save_config(updated_config, config_path)

    return updated_config


def add_extension(category, extension, config=None, config_path=None):
    """Add an extension to an existing category."""

    if config is None:
        config = load_config(config_path)

    if category not in config["categories"]:
        raise ValueError("Category does not exist.")

    if not isinstance(extension, str):
        raise ValueError("Extension must be a string.")

    extension = extension.strip().lower()

    if not extension.startswith("."):
        extension = "." + extension

    if (
        extension == "."
        or "/" in extension
        or "\\" in extension
        or any(character.isspace() for character in extension)
    ):
        raise ValueError("Invalid file extension.")

    for existing_category, extensions in config["categories"].items():
        if extension in extensions:
            raise ValueError(
                f"Extension already belongs to {existing_category}."
            )

    updated_config = deepcopy(config)
    updated_config["categories"][category].append(extension)

    save_config(updated_config, config_path)

    return updated_config


def remove_extension(category, extension, config=None, config_path=None):
    """Remove an extension from a category."""

    if config is None:
        config = load_config(config_path)

    if category not in config["categories"]:
        raise ValueError("Category does not exist.")

    extension = extension.strip().lower()

    if extension not in config["categories"][category]:
        raise ValueError("Extension does not exist in this category.")

    updated_config = deepcopy(config)
    updated_config["categories"][category].remove(extension)

    save_config(updated_config, config_path)

    return updated_config


def set_default_category(category, config=None, config_path=None):
    """Change the default category for unrecognized files."""

    if config is None:
        config = load_config(config_path)

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Default category cannot be empty.")

    category = category.strip()

    if category in config["categories"]:
        raise ValueError(
            "Default category must not duplicate an existing category."
        )

    updated_config = deepcopy(config)
    updated_config["default_category"] = category

    save_config(updated_config, config_path)

    return updated_config


def reset_config(config_path=None):
    """Restore the default configuration."""

    config = deepcopy(DEFAULT_RULES)

    save_config(config, config_path)

    return config
