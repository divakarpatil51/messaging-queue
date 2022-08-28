import logging
from enum import Enum
from time import time


class LogHandlerType(Enum):
    StreamHandler = 1
    FileHandler = 2


class LoggerConfig(object):
    """
    Logger config class.
    """

    @staticmethod
    def create_logger(log_type: LogHandlerType = LogHandlerType.StreamHandler, log_level="INFO"):
        custom_logger = logging.getLogger()
        # Removing existing handler
        if custom_logger.hasHandlers():
            custom_logger.handlers.pop()
        custom_logger.propagate = False
        custom_logger.setLevel(log_level)

        if log_type == LogHandlerType.StreamHandler:
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(f"logs/{int(time())}.log")
        handler.setLevel(log_level)
        handler.setFormatter(
            logging.Formatter("%(message)s")
        )
        custom_logger.addHandler(handler)
