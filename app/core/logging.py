"""Structured logging configuration."""

import logging
import sys
from typing import Any

import json_logging

from app.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application.
    
    Sets up JSON logging when log_format is 'json',
    otherwise uses standard text format.
    """
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    if settings.log_format == "json":
        # Enable JSON logging
        json_logging.init_fastapi(enable_json=True)

        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(log_level)
        logger.addHandler(logging.StreamHandler(sys.stdout))
    else:
        # Standard text logging
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
