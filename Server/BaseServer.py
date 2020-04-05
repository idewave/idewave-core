import asyncio
from asyncio.streams import StreamReader, StreamWriter


class BaseServer(object):

    __slots__ = ('host', 'port', 'instance')

    def __init__(self, **kwargs):
        self.host: str = kwargs.pop('host')
        self.port: int = kwargs.pop('port')
        self.instance = asyncio.start_server(
            self.handle_connection,
            host=self.host,
            port=self.port
        )

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        pass

    def get_instance(self):
        return self.instance

    def stop(self):
        self.instance.close()

    @staticmethod
    def create():
        return BaseServer(host=None, port=None)
