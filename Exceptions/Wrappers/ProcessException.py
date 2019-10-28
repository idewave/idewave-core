import asyncio

from asyncio import QueueEmpty, QueueFull
from concurrent.futures import TimeoutError

from Utils.Debug.Logger import Logger


class ProcessException(object):

    __slots__ = ('func', 'custom_handlers', 'exclude')

    def __init__(self, custom_handlers=None):
        self.func = None
        self.custom_handlers = custom_handlers
        # TODO: this is temporary approach to avoid redundant output, should be removed
        self.exclude = [QueueEmpty, QueueFull, TimeoutError]

    async def _process_coroutine_exc(self, *args, **kwargs):
        try:
            return await self.func(*args, **kwargs)
        except Exception as e:
            if self.custom_handlers and e.__class__ in self.custom_handlers:
                return self.custom_handlers[e.__class__]()

            if e.__class__ not in self.exclude:
                Logger.error(e.__class__)
                # traceback.print_exc()
                raise e

    def _process_exc(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            if self.custom_handlers and e.__class__ in self.custom_handlers:
                return self.custom_handlers[e.__class__]()

            if e.__class__ not in self.exclude:
                Logger.critical(e.__class__)
                # traceback.print_exc()
                raise e

    def __call__(self, func):
        self.func = func

        def wrapper(*args, **kwargs):
            if self.custom_handlers:
                if isinstance(self.custom_handlers, property):
                    self.custom_handlers = self.custom_handlers.__get__(self, self.__class__)

            if asyncio.iscoroutinefunction(self.func):
                return self._process_coroutine_exc(*args, **kwargs)
            else:
                return self._process_exc(*args, **kwargs)

        return wrapper
