
import json
import shutil

from pathlib import Path
from datetime import datetime

try:
    from .logger import get_logger
except ImportError:
    from logger import get_logger


logger = get_logger()


def get_history_path():
    """Return the location of the persistent movement history."""

    project_root = Path(__file__).resolve().parent.parent
    logs_directory = project_root / "logs"

    logs_directory.mkdir(parents=True, exist_ok=True)

    return logs_directory / "organization_history.json"


def load_movement_history(history_path=None):
    """Load saved movement history from JSON."""

    if history_path is None:
        history_path = get_history_path()

    history_path = Path(history_path)

    if not history_path.exists():
        return []

    try:
        with history_path.open("r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            raise ValueError("History must contain a JSON list.")

        return history

    except (json.JSONDecodeError, OSError, ValueError) as error:
        logger.exception("Could not load movement history.")
        raise ValueError(
            f"Could not load movement history: {error}"
        ) from error


def save_movement_history(history, history_path=None):
    """Save movement history using a temporary file."""

    if history_path is None:
        history_path = get_history_path()

    history_path = Path(history_path)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = history_path.with_suffix(".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

        temporary_path.replace(history_path)

    except OSError:
        logger.exception("Could not save movement history.")

        if temporary_path.exists():
            temporary_path.unlink(missing_ok=True)

        raise


def get_unique_destination(destination):
    """Generate a unique destination path without overwriting files."""

    destination = Path(destination)

    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix

    counter = 1

    while True:
        new_destination = parent / f"{stem} ({counter}){suffix}"

        if not new_destination.exists():
            return new_destination

        counter += 1


def create_organization_plan(files, source_folder):
    """
    Generate a proposed file movement plan.

    Captures file metadata so changes can be detected
    before the file is moved.
    """

    source_folder = Path(source_folder).resolve()
    plan = []

    for file_info in files:

        source = Path(file_info["path"]).resolve()
        category = file_info["category"]

        if not source.is_file():
            continue

        try:
            file_stat = source.stat()

        except OSError:
            continue

        # Prevent moving a file into its own category folder.
        destination_folder = source_folder / category

        if (
            source == destination_folder
            or destination_folder in source.parents
        ):
            continue

        destination = get_unique_destination(
            destination_folder / source.name
        )

        plan.append({
            "name": source.name,
            "category": category,
            "source": str(source),
            "destination": str(destination),
            "expected_size_bytes": file_info.get(
                "size_bytes",
                file_stat.st_size
            ),
            "expected_modified_timestamp": file_info.get(
                "modified_timestamp",
                file_stat.st_mtime
            ),
            "status": "Pending"
        })

    return plan


def file_has_changed(source, item):
    """Check whether a file has changed since it was scanned."""

    try:
        current_stat = source.stat()

    except OSError:
        return True

    expected_size = item.get("expected_size_bytes")
    expected_modified = item.get("expected_modified_timestamp")

    if expected_size is None or expected_modified is None:
        return True

    return (
        current_stat.st_size != expected_size
        or current_stat.st_mtime != expected_modified
    )


def organize_files(plan, history_path=None):
    """
    Execute a previously generated organization plan.

    Files are checked before moving. Successful movements
    are saved to persistent history.
    """

    history = load_movement_history(history_path)

    for item in plan:

        source = Path(item["source"])
        destination = Path(item["destination"])

        try:

            # Check whether the source still exists.
            if not source.exists() or not source.is_file():

                item["status"] = "Skipped: Source unavailable"

                logger.warning(
                    "Source unavailable: %s",
                    source
                )
                continue

            # Check whether the file changed after scanning.
            if file_has_changed(source, item):

                item["status"] = "Skipped: File changed since scan"

                logger.warning(
                    "File changed since scan: %s",
                    source
                )
                continue

            # Avoid overwriting files that appeared after preview.
            destination = get_unique_destination(destination)

            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Move the file.
            shutil.move(
                str(source),
                str(destination)
            )

            movement = {
                "name": source.name,
                "source": str(source),
                "destination": str(destination),
                "moved_at": datetime.now().isoformat()
            }

            history.append(movement)

            try:
                # Persist history immediately after the move.
                save_movement_history(
                    history,
                    history_path
                )

            except OSError as save_error:

                # Remove the unsaved history entry.
                history.pop()

                # Attempt to restore the file.
                try:
                    if destination.exists() and not source.exists():

                        source.parent.mkdir(
                            parents=True,
                            exist_ok=True
                        )

                        shutil.move(
                            str(destination),
                            str(source)
                        )

                        item["status"] = (
                            "Failed: History save failed; "
                            "file restored"
                        )

                    else:
                        item["status"] = (
                            "Critical: History save failed; "
                            "automatic restoration was not possible"
                        )

                except (OSError, shutil.Error) as rollback_error:

                    item["status"] = (
                        "Critical: History save and restoration failed"
                    )

                    logger.exception(
                        "Could not restore %s after history save failure. "
                        "Original error: %s",
                        destination,
                        save_error
                    )

                logger.error(
                    "History save failed for %s: %s",
                    source,
                    save_error
                )

                continue

            item["destination"] = str(destination)
            item["status"] = "Moved"

            logger.info(
                "Moved %s to %s",
                source,
                destination
            )

        except (OSError, shutil.Error) as error:

            item["status"] = f"Failed: {error}"

            logger.exception(
                "Failed to move %s",
                source
            )

    return history


def undo_organization(history=None, history_path=None):
    """
    Reverse successful file movements.

    Restores files only when their original locations
    are available. Existing files are never overwritten.
    """

    if history is None:
        history = load_movement_history(history_path)

    remaining_history = []
    results = []

    for movement in reversed(history):

        source = Path(movement["source"])
        destination = Path(movement["destination"])

        try:

            if not destination.exists():

                results.append({
                    "file": movement.get("name", destination.name),
                    "status": "Failed: Organized file not found"
                })

                remaining_history.append(movement)
                continue

            if source.exists():

                results.append({
                    "file": movement.get("name", source.name),
                    "status": "Failed: Original location occupied"
                })

                remaining_history.append(movement)
                continue

            source.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.move(
                str(destination),
                str(source)
            )

            results.append({
                "file": movement.get("name", source.name),
                "status": "Restored"
            })

            logger.info(
                "Restored %s to %s",
                destination,
                source
            )

        except (OSError, shutil.Error) as error:

            results.append({
                "file": movement.get("name", destination.name),
                "status": f"Failed: {error}"
            })

            remaining_history.append(movement)

            logger.exception(
                "Failed to restore %s",
                destination
            )

    # Keep only movements that could not be undone.
    remaining_history.reverse()

    save_movement_history(
        remaining_history,
        history_path
    )

    return results
