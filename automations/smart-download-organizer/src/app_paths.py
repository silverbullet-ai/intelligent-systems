
import os
import sys

from pathlib import Path


APP_NAME = "SmartDownloadOrganizer"


def get_project_root():
    """Return the project root directory during development."""

    return Path(__file__).resolve().parent.parent


def get_resource_path(relative_path):
    """
    Resolve bundled resources in both development
    and PyInstaller environments.
    """

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = get_project_root()

    return base_path / relative_path


def get_user_data_dir():
    """
    Return the application's persistent user-data directory.

    Windows: %APPDATA%/SmartDownloadOrganizer
    macOS: ~/Library/Application Support/SmartDownloadOrganizer
    Linux: ~/.config/SmartDownloadOrganizer
    """

    if sys.platform == "win32":
        base_path = Path(
            os.environ.get(
                "APPDATA",
                Path.home() / "AppData" / "Roaming"
            )
        )

    elif sys.platform == "darwin":
        base_path = Path.home() / "Library" / "Application Support"

    else:
        base_path = Path(
            os.environ.get(
                "XDG_CONFIG_HOME",
                Path.home() / ".config"
            )
        )

    return base_path / APP_NAME


def get_config_dir():
    """Return the user configuration directory."""

    return get_user_data_dir() / "config"


def get_config_path():
    """Return the user's configuration file path."""

    return get_config_dir() / "rules.json"


def get_logs_dir():
    """Return the application logs directory."""

    return get_user_data_dir() / "logs"


def get_log_path():
    """Return the application log file path."""

    return get_logs_dir() / "smart_organizer.log"


def get_history_path():
    """Return the organization history file path."""

    return get_logs_dir() / "organization_history.json"
