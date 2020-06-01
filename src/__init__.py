import sys
import logging
import traceback


def log_except_hook(*exc_info):
    logger = logging.getLogger(__name__)
    text = "".join(traceback.format_exception(*exc_info))
    logger.critical(f"Unhandled exception:\n{text}")


sys.excepthook = log_except_hook
