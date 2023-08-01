"""Logging Configuration"""
__docformat__ = "numpy"

# IMPORTATION STANDARD
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

# IMPORTATION INTERNAL
from app.core.log.generation.directories import get_log_dir
from app.core.session.current_system import get_current_system
from app.core.log.generation.settings import Settings, LogSettings

logging_verbosity = get_current_system().LOGGING_VERBOSITY

logger = logging.getLogger(__name__)

# logging.getLogger("requests").setLevel(logging_verbosity)
# logging.getLogger("urllib3").setLevel(logging_verbosity)
# logging.getLogger("sqlalchemy").setLevel(logging_verbosity)


def add_console_handler(settings: Settings):
    handler = logging.StreamHandler(level=settings.log_settings.verbosity)
    formatter = logging.Formatter(
        "%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(lineno)s|%(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


def add_noop_handler(settings: Settings):
    handler = logging.NullHandler(level=settings.log_settings.verbosity)
    formatter = logging.Formatter(
        "%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(lineno)s|%(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


def add_file_handler(settings: Settings):
    filename = settings.log_settings.directory / "app"

    handler = TimedRotatingFileHandler(filename=filename)
    formatter = logging.Formatter(
        "%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(lineno)s|%(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


def setup_handlers(settings: Settings):
    logging_settings = settings.log_settings
    handler_list = logging_settings.handler_list
    verbosity = logging_settings.verbosity

    logging.basicConfig(
        level=verbosity,
        format="%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(lineno)s|%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        handlers=[],
        encoding="utf-8-sig"
    )

    for handler_type in handler_list:
        if handler_type == "console":
            add_console_handler(settings=settings)
        elif handler_type == "noop":
            add_noop_handler(settings=settings)
        elif handler_type == "file":
            add_file_handler(settings=settings)
        else:
            logger.debug("Unknown log handler.")

    logger.info("Logging configuration finished")
    logger.info("Logging set to %s", handler_list)
    logger.info("Verbosity set to %s", verbosity)


def setup_logging(
    frequency: Optional[str] = None,
    verbosity: Optional[int] = None,
) -> None:
    """Setup Logging"""
    current_system = get_current_system()

    # LogSettings
    directory = get_log_dir()
    frequency = frequency or current_system.LOGGING_FREQUENCY
    handler_list = current_system.LOGGING_HANDLERS
    rolling_clock = current_system.LOGGING_ROLLING_CLOCK
    verbosity = verbosity or current_system.LOGGING_VERBOSITY

    settings = Settings(
        log_settings=LogSettings(
            directory=directory,
            frequency=frequency,
            handler_list=handler_list,
            rolling_clock=rolling_clock,
            verbosity=verbosity,
        ),
    )

    setup_handlers(settings=settings)
