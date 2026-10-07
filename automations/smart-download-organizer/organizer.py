"""
File Organizer
==============
Sorts the files in a folder into sub-folders by file type
(Images, Documents, Videos, etc., as defined in config.py).

Author:   Aahish
GitHub:   silverbullet-ai
Version:  1.0.0
Created:  2026-10-08
License:  MIT

Usage:
    python organizer.py                          # organize ~/Downloads
    python organizer.py --folder ~/Desktop       # organize a specific folder
    python organizer.py --dry-run                # preview without moving files

Requires:
    Python 3.9+ and a config.py defining CATEGORIES, MISCELLANEOUS_FOLDER, LOG_FILE.
"""

__author__ = "Aahish"
__version__ = "1.0.0"

import argparse
import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from config import CATEGORIES, LOG_FILE, MISCELLANEOUS_FOLDER


# --------------------------------------------------------------------------- #
# Setup
# --------------------------------------------------------------------------- #

def setup_logging() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def build_extension_map() -> dict[str, str]:
    """Flatten CATEGORIES into {'.ext': 'Folder'} for O(1) lookups."""
    return {
        ext.lower(): folder
        for folder, extensions in CATEGORIES.items()
        for ext in extensions
    }


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def get_category(file_path: Path, extension_map: dict[str, str]) -> str:
    return extension_map.get(file_path.suffix.lower(), MISCELLANEOUS_FOLDER)


def get_unique_destination(destination: Path) -> Path:
    """Return a path that doesn't exist yet: name.ext -> name_1.ext -> name_2.ext ..."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def validate_folder(folder: str) -> Path:
    path = Path(folder).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Folder does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    return path


def iter_files(folder: Path):
    """Yield top-level files only, skipping the log file and sub-folders."""
    log_path = LOG_FILE.resolve()
    for item in sorted(folder.iterdir()):
        if item.is_file() and item.resolve() != log_path:
            yield item


# --------------------------------------------------------------------------- #
# Core logic
# --------------------------------------------------------------------------- #

@dataclass
class Summary:
    moved: int = 0
    skipped: int = 0


def move_file(item: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(item), str(destination))


def organize(folder: str, dry_run: bool = False) -> Summary:
    root = validate_folder(folder)
    extension_map = build_extension_map()
    summary = Summary()

    for item in iter_files(root):
        category = get_category(item, extension_map)
        destination = get_unique_destination(root / category / item.name)

        if dry_run:
            print(f"[DRY RUN] {item.name} -> {category}/{destination.name}")
            continue

        try:
            move_file(item, destination)
        except OSError as error:
            logging.error("Failed to move '%s': %s", item, error)
            print(f"Skipped: {item.name} | Error: {error}")
            summary.skipped += 1
        else:
            logging.info("Moved '%s' -> '%s'", item, destination)
            print(f"Moved: {item.name} -> {category}/")
            summary.moved += 1

    return summary


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organize files in a folder by file type."
    )
    parser.add_argument(
        "--folder",
        default=str(Path.home() / "Downloads"),
        help="Folder to organize. Defaults to Downloads.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    setup_logging()

    try:
        summary = organize(args.folder, args.dry_run)
    except (FileNotFoundError, NotADirectoryError) as error:
        logging.error(str(error))
        print(f"Error: {error}")
        return 1

    if args.dry_run:
        print("\nDry run complete. No files were moved.")
    else:
        print(f"\nOrganization complete. Moved: {summary.moved}, Skipped: {summary.skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())