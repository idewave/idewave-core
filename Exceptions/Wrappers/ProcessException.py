from inspect import iscoroutinefunction

from asyncio import QueueEmpty, QueueFull
from concurrent.futures import TimeoutError


class ProcessException(object):

    __slots__ = ('handlers',)

    def __init__(self, custom_handlers=None):
        if isinstance(custom_handlers, property):
            custom_handlers = custom_handlers.__get__(self, self.__class__)

        def raise_exception(e: Exception):
            raise e

        exclude = {
            QueueEmpty: lambda e: None,
            QueueFull: lambda e: None,
            TimeoutError: lambda e: None
        }

        self.handlers = {
            **exclude,
            **(custom_handlers or {}),
            Exception: raise_exception
        }

    def __call__(self, func):
        if iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    return self.handlers.get(e.__class__, self.handlers[Exception])(e)
        else:
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    return self.handlers.get(e.__class__, self.handlers[Exception])(e)

        return wrapper
