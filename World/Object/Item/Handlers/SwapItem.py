from Server.Connection.Connection import Connection
from Typings.Abstract.AbstractHandler import AbstractHandler


class SwapItem(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        return None, None
