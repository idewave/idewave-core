from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Typings.Abstract.AbstractHandler import AbstractHandler


class ItemInfo(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        return WorldOpCode.SMSG_ITEM_QUERY_SINGLE_RESPONSE, None
