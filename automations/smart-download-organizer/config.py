"""
File Organizer - Configuration
==============================
Settings used by organizer.py: which extensions go into which folder,
where uncategorised files end up, and where the log is written.

Author:   Aahish
GitHub:   silverbullet-ai
Version:  1.0.0
Created:  2026-10-08
License:  MIT

To add a new file type, append its extension (lowercase, with the dot)
to the matching list in CATEGORIES, or add a new category entirely.
"""

from pathlib import Path

__author__ = "Aahish"
__version__ = "1.0.0"

# --------------------------------------------------------------------------- #
# Categories: folder name -> list of file extensions
# --------------------------------------------------------------------------- #

CATEGORIES: dict[str, list[str]] = {
    "Images":        [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents":     [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Spreadsheets":  [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Videos":        [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Music":         [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "Archives":      [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Applications":  [".exe", ".msi", ".msix"],
    "Code": [
        ".py", ".java", ".js", ".ts", ".html", ".css",
        ".cpp", ".c", ".h", ".json", ".xml", ".yaml", ".yml",
    ],
}

# Folder for any file whose extension isn't listed above
MISCELLANEOUS_FOLDER = "Miscellaneous"

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #

# Stored next to this file, so the log lands in the same place
# no matter which directory the script is run from.
LOG_FILE = Path(__file__).resolve().parent / "logs" / "organizer.log"