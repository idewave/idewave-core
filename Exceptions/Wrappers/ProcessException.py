import asyncio

from asyncio import QueueEmpty, QueueFull
from concurrent.futures import TimeoutError


class ProcessException(object):

    __slots__ = ('func', 'custom_handlers', 'exclude')

    def __init__(self, custom_handlers=None):
        self.func = None
        self.custom_handlers = custom_handlers
        self.exclude = [QueueEmpty, QueueFull, TimeoutError]

    def __call__(self, func, *a):
        self.func = func

        def wrapper(*args, **kwargs):
            if self.custom_handlers:
                if isinstance(self.custom_handlers, property):
                    self.custom_handlers = self.custom_handlers.__get__(self, self.__class__)

            if asyncio.iscoroutinefunction(self.func):
                return self._coroutine_exception_handler(*args, **kwargs)
            else:
                return self._sync_exception_handler(*args, **kwargs)

        return wrapper

    async def _coroutine_exception_handler(self, *args, **kwargs):
        try:
            return await self.func(*args, **kwargs)
        except Exception as e:
            if self.custom_handlers and e.__class__ in self.custom_handlers:
                return self.custom_handlers[e.__class__]()

            if e.__class__ not in self.exclude:
                raise e

    def _sync_exception_handler(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            if self.custom_handlers and e.__class__ in self.custom_handlers:
                return self.custom_handlers[e.__class__]()

            if e.__class__ not in self.exclude:
                raise e
