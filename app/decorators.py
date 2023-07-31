import logging
import functools
import os
import sqlalchemy

# Define the logger
logger = logging.getLogger(__name__)


# Create the decorator
def log_start_end(func=None, log=None):
    assert callable(func) or func is None

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.info(f"Function '{func.__name__}' started.")  # what if error?
            try:
                result = func(*args, **kwargs)
                log.info(f"Function '{func.__name__}' finished.")  # what if error?
                return result
            except KeyboardInterrupt:
                log.info(
                    "Interrupted by user",
                    extra={"func_name_override": func.__name__},
                )
                return []
            except sqlalchemy.exc.IntegrityError as error:
                log.exception(error)
            
            except Exception as e:
                log.exception(
                    "Exception: %s",
                    str(e),
                    extra={"func_name_override": func.__name__},
                )
                return []

        return wrapper

    return decorator(func) if callable(func) else decorator


def check_api_key(api_keys: list):
    """Function to check if the API key exists in the environment variables"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the API key is present in the environment variables
            for api_key in api_keys:
                if os.getenv(api_key) is None:
                    logger.error(
                        f"API key '{api_key}' not found in environment variables."
                    )
                    raise Exception(
                        f"API key '{api_key}' not found in environment variables."
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator
