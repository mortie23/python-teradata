"""Logging configuration using loguru for TPT operations."""

import sys
from pathlib import Path
from loguru import logger


def setup_logging(
    log_dir: str | Path = "logs",
    log_file: str = "pytpt.log",
    log_level: str = "INFO",
) -> None:
    """
    Configure loguru logging for TPT operations.

    Args:
        log_dir: Directory to store log files (default: "logs")
        log_file: Name of the log file to write to (default: "pytpt.log")
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Ensure log directory exists
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Full log file path
    full_log_path = log_path / log_file

    # Remove default handler
    logger.remove()

    # Add console handler with simpler format
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # Add file handler with detailed format
    logger.add(
        str(full_log_path),
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )

    logger.info(f"Logging configured - Console: {log_level}, File: {full_log_path}")


def get_logger(name: str = None):
    """Get a logger instance."""
    if name:
        return logger.bind(name=name)
    return logger
