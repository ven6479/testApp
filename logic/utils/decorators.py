import asyncio
from functools import wraps
from loguru import logger


def logging(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await _logging_async(func, *args, **kwargs)

        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return _logging_sync(func, *args, **kwargs)

        return sync_wrapper


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
