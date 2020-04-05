from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Typings.Abstract import AbstractHandler


class TimeSync(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        # TODO: correctly evaluate value
        response = bytes(4)
        return WorldOpCode.SMSG_TIME_SYNC_REQ, [response]
