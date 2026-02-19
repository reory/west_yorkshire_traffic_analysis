import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(
    log_level=logging.INFO,
    log_file="app.log",
    max_bytes=5_000_000,   # 5 MB
    backup_count=3
):
    # Create logs directory if missing
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)

    # Formatter: timestamp + level + module + message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
