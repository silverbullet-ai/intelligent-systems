
from pathlib import Path
from datetime import datetime
import os

try:
    from .config_manager import load_config
except ImportError:
    from config_manager import load_config


def format_file_size(size_bytes):
    """Convert bytes into a human-readable file size."""

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


def get_organizer_categories(config=None):
    """
    Return the folder names created by the organizer.

    Category names and the default category are loaded from rules.json.
    An optional config dictionary can be supplied for testing.
    """

    if config is None:
        config = load_config()

    categories = set(config["categories"].keys())
    categories.add(config["default_category"])

    return categories


def scan_folder(folder_path, recursive=False):
    """
    Scan a folder and collect metadata about its files.

    This function does not move, rename, or delete files.

    Args:
        folder_path: Folder selected by the user.
        recursive: Whether to include files in subfolders.

    Returns:
        files: List containing file metadata.
        summary: Dictionary containing scan statistics.
    """

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            "The selected folder does not exist."
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            "The selected path is not a folder."
        )

    folder = folder.resolve()

    organizer_categories = get_organizer_categories()

    files = []
    total_size = 0
    inaccessible_files = 0

    def process_file(file_path):
        """Collect metadata for an individual file."""

        nonlocal total_size, inaccessible_files

        try:
            if file_path.is_symlink() or not file_path.is_file():
                return

            file_stat = file_path.stat()

            file_size = file_stat.st_size
            extension = file_path.suffix.lower()

            file_info = {
                "name": file_path.name,
                "extension": (
                    extension if extension else "No extension"
                ),
                "size_bytes": file_size,
                "modified_timestamp": file_stat.st_mtime,
                "size": format_file_size(file_size),
                "path": str(file_path.resolve()),
                "category": "Uncategorized",
                "modified": datetime.fromtimestamp(
                    file_stat.st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S")
            }

            files.append(file_info)
            total_size += file_size

        except OSError:
            inaccessible_files += 1

    if recursive:

        def handle_walk_error(error):
            nonlocal inaccessible_files
            inaccessible_files += 1

        for current_folder, directories, filenames in os.walk(
            folder,
            topdown=True,
            followlinks=False,
            onerror=handle_walk_error
        ):

            current_path = Path(current_folder)

            # Exclude organizer category folders only at the
            # selected folder's root level.
            if current_path == folder:
                directories[:] = [
                    directory
                    for directory in directories
                    if directory not in organizer_categories
                    and not (
                        current_path / directory
                    ).is_symlink()
                ]
            else:
                # Continue scanning nested folders, while
                # preventing traversal through symbolic links.
                directories[:] = [
                    directory
                    for directory in directories
                    if not (
                        current_path / directory
                    ).is_symlink()
                ]

            for filename in filenames:
                process_file(current_path / filename)

    else:

        try:
            for file_path in folder.iterdir():
                process_file(file_path)

        except OSError:
            inaccessible_files += 1

    summary = {
        "folder": str(folder),
        "total_files": len(files),
        "total_size_bytes": total_size,
        "total_size": format_file_size(total_size),
        "inaccessible_files": inaccessible_files
    }

    return files, summary
