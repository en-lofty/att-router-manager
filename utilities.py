from functools import wraps

from logzero import logger

from driver_singleton import DriverSingleton


def requires_url(required_url):
    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if DriverSingleton.get_driver().current_url != required_url:
                    DriverSingleton.get_driver().get(required_url)
            except Exception as e:
                logger.exception(e)
                DriverSingleton.get_driver().get(required_url)
            return func(*args, **kwargs)

        return wrapper

    return inner_function
