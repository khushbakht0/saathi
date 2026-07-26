from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "ai_student_assistant": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


def configure_logging() -> None:
    dictConfig(LOGGING_CONFIG)
