import asyncio
import traceback
import functools

from asyncio import QueueEmpty, QueueFull
from concurrent.futures import TimeoutError

from Utils.Debug.Logger import Logger


class ProcessException(object):

    __slots__ = ('func',)

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)

    async def _process_coroutine_exc(self, *args, **kwargs):
        try:
            return await self.func(*args, **kwargs)
        except TimeoutError:
            pass
        except BrokenPipeError:
            pass
        except QueueEmpty:
            pass
        except QueueFull:
            pass
        except Exception as e:
            Logger.error('[{}]: {}'.format([*args], e))
            traceback.print_exc()
            pass

    def _process_exc(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except KeyError:
            pass
        except KeyboardInterrupt:
            pass
        except ValueError:
            pass
        except Exception as e:
            Logger.error('[{}]: {}'.format(self.func, e))
            traceback.print_exc()
            pass

    def __call__(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.func):
            return self._process_coroutine_exc(*args, **kwargs)
        else:
            return self._process_exc(*args, **kwargs)
