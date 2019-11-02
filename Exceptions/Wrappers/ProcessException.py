from inspect import iscoroutinefunction

from asyncio import QueueEmpty, QueueFull
from concurrent.futures import TimeoutError


class ProcessException(object):

    __slots__ = ('func', 'handlers')

    def __init__(self, custom_handlers=None):
        self.func = None

        if isinstance(custom_handlers, property):
            custom_handlers = custom_handlers.__get__(self, self.__class__)

        exclude = {
            QueueEmpty: lambda: None,
            QueueFull: lambda: None,
            TimeoutError: lambda: None
        }

        self.handlers = {
            **exclude,
            **(custom_handlers or {})
        }

    def __call__(self, func):
        self.func = func

        if iscoroutinefunction(self.func):
            def wrapper(*args, **kwargs):
                return self._coroutine_exception_handler(*args, **kwargs)
        else:
            def wrapper(*args, **kwargs):
                return self._sync_exception_handler(*args, **kwargs)

        return wrapper

    async def _coroutine_exception_handler(self, *args, **kwargs):
        try:
            return await self.func(*args, **kwargs)
        except Exception as e:
            if e.__class__ in self.handlers:
                return self.handlers[e.__class__]()

            raise e

    def _sync_exception_handler(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            if e.__class__ in self.handlers:
                return self.handlers[e.__class__]()

            raise e
