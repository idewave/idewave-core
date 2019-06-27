import asyncio
from multiprocessing import Manager, cpu_count
from concurrent.futures import ProcessPoolExecutor


class MultiProcessQueue(object):

    def __init__(self, loop, maxsize, executor=ProcessPoolExecutor(max_workers=cpu_count())):
        self.instance = Manager().Queue(maxsize=maxsize)
        self.loop = loop
        self.executor = executor

    def __getattr__(self, item):
        if item in ['qsize', 'empty', 'full', 'close']:
            return getattr(self.instance, item)

    async def put(self, data):
        return await self.loop.run_in_executor(self.executor, self.instance.put, data)

    async def get(self):
        return await self.loop.run_in_executor(self.executor, self.instance.get)

    @staticmethod
    def get_instance():
        return MultiProcessQueue(loop=asyncio.get_event_loop(), maxsize=10)
