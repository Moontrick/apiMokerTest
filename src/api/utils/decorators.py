"""
Decorators module for API testing.
Provides utilities for retry logic, timing, and error handling.
"""
import time
from functools import wraps
from typing import Callable, Any
from .logger import get_logger

logger = get_logger(__name__)


def retry(max_attempts: int = 3, delay: int = 1, backoff: float = 1.0):
    """
    Retry decorator for handling transient failures.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for each retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(f"Attempt {attempt}/{max_attempts} for {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt} failed: {str(e)}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            raise last_exception
        
        return wrapper
    return decorator


def log_request(func: Callable) -> Callable:
    """
    Decorator to log API request details.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"{func.__name__} failed after {elapsed:.2f}s: {str(e)}")
            raise
    
    return wrapper


def timing(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.debug(f"{func.__name__} took {elapsed:.3f}s")
        return result
    
    return wrapper
