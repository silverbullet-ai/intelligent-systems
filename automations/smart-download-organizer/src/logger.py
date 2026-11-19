
import logging

try:
    from .app_paths import get_logs_dir, get_log_path
except ImportError:
    from app_paths import get_logs_dir, get_log_path


def get_logger(name="SmartDownloadOrganizer"):
    """
    Create and return the application logger.

    Logs are stored in the user's application data directory.
    """

    log_directory = get_logs_dir()
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = get_log_path()

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

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
