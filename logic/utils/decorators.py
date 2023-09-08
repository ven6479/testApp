import asyncio
from functools import wraps
from loguru import logger


def logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return _logging_async(func, *args, **kwargs)
        else:
            return _logging_sync(func, *args, **kwargs)

    return wrapper


def _logging_sync(func, *args, **kwargs):
    value = func(*args, **kwargs)
    if value.get('error'):
        logger.error(value)
    else:
        logger.info(value)
    return value


async def _logging_async(func, *args, **kwargs):
    value = await func(*args, **kwargs)
    if value.get('error'):
        logger.error(value)
    else:
        logger.info(value)
    return value
