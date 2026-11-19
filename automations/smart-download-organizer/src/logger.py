
import logging
from pathlib import Path


def get_logger(name="SmartDownloadOrganizer"):
    """
    Create and return the application logger.

    Logs are stored in the project's logs directory.
    """

    project_root = Path(__file__).resolve().parent.parent
    log_directory = project_root / "logs"

    log_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    log_file = log_directory / "smart_organizer.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if called multiple times.
    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
