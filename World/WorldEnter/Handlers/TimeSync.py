from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class TimeSync(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        # TODO: correctly evaluate value
        response = b'\x00\x00\x00\x00'
        return WorldOpCode.SMSG_TIME_SYNC_REQ, [response]
