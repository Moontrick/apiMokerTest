"""
Logger utility module for API testing.
Provides centralized logging configuration using loguru.
"""
import sys
from pathlib import Path
from loguru import logger

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

# Remove default handler
logger.remove()

# Add console handler with formatting
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
)

# Add file handler
log_file = LOGS_DIR / "api_tests.log"
logger.add(
    str(log_file),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="500 MB",
    retention="7 days",
)

# Add error file handler
error_log_file = LOGS_DIR / "api_tests_errors.log"
logger.add(
    str(error_log_file),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="500 MB",
    retention="7 days",
)


def get_logger(name: str = __name__):
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name, typically __name__
        
    Returns:
        Logger instance from loguru
    """
    return logger.bind(name=name)
