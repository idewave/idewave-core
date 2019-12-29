from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class AuraDuration(object):

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        response = b'\x00\xff\xff\xff\xff'
        return WorldOpCode.SMSG_UPDATE_AURA_DURATION, [response]
