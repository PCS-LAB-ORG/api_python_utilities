#!python

"""
My AI generated util for sending logs to a file and to console.
This is made to be simple and handle many simple uses and be built
upon as needed.
"""

import logging


def setup_logger():
    # Create a logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the minimum level for the logger

    # Create a file handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)  # Set the minimum level for the file handler

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        logging.INFO
    )  # Set the minimum level for the console handler

    # Define a formatter for the log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

    # Log messages at different levels
    # logger.debug('This is a debug message.')
    # logger.info('This is an info message.')
    # logger.warning('This is a warning message.')
    # logger.error('This is an error message.')
    # logger.critical('This is a critical message.')


logger = setup_logger()
