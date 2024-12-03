import logging
import logging.config
import os
from pythonjsonlogger import jsonlogger

def configure_logging():
    """Set up centralized logging with JSON formatting, sensitive data sanitization, and file directory validation."""
    # Ensure the logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_level = logging.DEBUG if os.getenv("DEBUG_MODE", "false").lower() == "true" else logging.INFO

    # Centralized logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            },
            "console": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json" if os.getenv("USE_JSON_LOGS", "true").lower() == "true" else "console",
                "level": log_level,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "json",
                "filename": os.getenv("LOG_FILE", f"{log_dir}/secure_app.log"),  # Logs directory path
                "level": logging.WARNING,  # Only log WARNING and higher to file
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True,
            },
            "uvicorn.access": {  # Suppress duplicate logs from Uvicorn
                "handlers": ["console"],
                "level": logging.WARNING,
                "propagate": False,
            },
        },
    }

    # Apply the logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    # Add a filter to sanitize sensitive data
    class SensitiveDataFilter(logging.Filter):
        """Sanitize sensitive data in logs."""

        def filter(self, record):
            if isinstance(record.msg, str) and "sensitive" in record.msg.lower():
                record.msg = record.msg.replace("sensitive", "[REDACTED]")
            return True

    # Apply the sensitive data filter
    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.addFilter(SensitiveDataFilter())

    logging.getLogger().info("Logging has been configured.")

# Expose the logger for application-wide use
logger = logging.getLogger("app")

# Initialize the logger when the module is imported
configure_logging()
