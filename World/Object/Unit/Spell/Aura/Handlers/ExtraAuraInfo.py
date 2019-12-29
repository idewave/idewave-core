from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class ExtraAuraInfo(object):

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        response = b'\x01\x01\x00dP\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff'
        return WorldOpCode.SMSG_SET_EXTRA_AURA_INFO, [response]
