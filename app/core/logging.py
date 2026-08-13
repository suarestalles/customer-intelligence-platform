import logging
import os
import sys


def setup_logging() -> None:
    """
    Configures application-wide logging.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=log_level,
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
        handlers=[logging.StreamHandler(sys.stdout)],
    )
