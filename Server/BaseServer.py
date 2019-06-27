import asyncio
from asyncio.streams import StreamReader, StreamWriter


class BaseServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.instance = asyncio.start_server(self.handle_connection, host=host, port=port)

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        pass

    def get_instance(self):
        return self.instance

    def stop(self):
        self.instance.close()

    @staticmethod
    def create():
        return BaseServer(None, None)
