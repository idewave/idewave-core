from inspect import iscoroutinefunction
from asyncio import QueueEmpty, QueueFull
from concurrent.futures import TimeoutError


class HandleException(object):

    __slots__ = ('custom_handlers', 'handlers')

    exclude = {
        QueueEmpty: lambda e: None,
        QueueFull: lambda e: None,
        TimeoutError: lambda e: None,
    }

    def __init__(self, custom_handlers=None):
        self.custom_handlers: dict = custom_handlers

        self.handlers = {
            **HandleException.exclude,
            Exception: HandleException.raise_exception
        }

    def __call__(self, func):
        if iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                handlers = self.get_handlers(args[0])
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    return handlers.get(e.__class__, handlers[Exception])(e)
        else:
            def wrapper(*args, **kwargs):
                handlers = self.get_handlers(args[0])
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    return handlers.get(e.__class__, handlers[Exception])(e)

        return wrapper

    def get_handlers(self, *args):
        custom_handlers = self.custom_handlers

        if isinstance(custom_handlers, property):
            custom_handlers = custom_handlers.__get__(args[0], args[0].__class__)

        handlers = {
            **self.handlers,
            **(custom_handlers or {})
        }

        return handlers

    @staticmethod
    def raise_exception(e):
        raise e
