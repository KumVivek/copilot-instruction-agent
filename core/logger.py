"""Logging configuration for RepoSentinel."""
import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

def setup_logger(name: str = "reposentinel", level: str = "INFO", use_rich: bool = True) -> logging.Logger:
    """Set up logger with optional rich formatting.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_rich: Whether to use rich formatting for better output
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    if use_rich:
        console = Console(stderr=True)
        handler = RichHandler(
            console=console,
            show_time=True,
            show_path=True,
            rich_tracebacks=True,
        )
        handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    else:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
    
    logger.addHandler(handler)
    return logger
