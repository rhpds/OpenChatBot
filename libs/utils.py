import config as cfg
from loguru import logger
import sys

"""
Utilities such as logging
"""


def setup_logging(logging_level: str = "DEBUG"):
    """
    Setup the logging level, typically from the chat settings
    logging_level: str - The logging level to set: TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    """

    logger.remove()  # Remove default handler
    logger.add(sys.stdout, level=logging_level)
    logger.add(cfg.LOG_FILE, level=logging_level)
    logger.info(f"Logging level set to: {logging_level}")
