#!python

"""
My AI generated util for sending logs to a file and to console.
This is made to be simple and handle many simple uses and be built
upon as needed.
"""

from datetime import datetime
from functools import partial
import inspect
import logging
import os
import re

from apu.utils import constants


def setup_logger(log_file_name="app.log"):
    # Define a formatter for the log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Create a logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the minimum level for the logger

    # Create a file handler
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)  # Set the minimum level for the file handler
    file_handler.setFormatter(formatter)
    file_handler.addFilter(MaskSensitiveDataFilter())  # Add the custom filter
    logger.addHandler(file_handler)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        logging.INFO
    )  # Set the minimum level for the console handler
    console_handler.addFilter(MaskSensitiveDataFilter())  # Add the custom filter
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


class MaskSensitiveDataFilter(logging.Filter):
    # Regex pattern for a simple credit card number (adjust as needed)
    CC_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")

    def filter(self, record):
        # Safely compute the message with args
        message = record.getMessage()
        masked_message = self.CC_RE.sub("[REDACTED-CC]", message)

        # Update the record's message and clear args to prevent re-processing
        record.msg = masked_message
        record.args = ()
        return True


class Logger:
    """General custom logger solution"""

    log_file_name = (
        f"{constants.script_dir}/output_{constants.date_time_format_w_seconds}.log"
    )

    def __init__(self, log_file_name):
        if log_file_name:
            self.log_file_name = log_file_name

    def log(self, line, exception="", level="INFO ") -> None:
        now = datetime.now()
        caller_frame = inspect.stack()[1]
        file_path = os.path.relpath(caller_frame.filename)
        with open(self.log_file_name, "+a", newline="") as log_file:
            # To File
            print(
                f"{level}{now} {file_path}:{caller_frame.lineno} {line}",
                exception,
                file=log_file,
            )

            # To Console
            print(f"{level}{now} {file_path}:{caller_frame.lineno} {line}", exception)

    debug = partial(log, level="DEBUG ")
    error = partial(log, level="ERROR ")
    warn = partial(log, level="WARN ")
