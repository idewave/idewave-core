from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class AddonInfo(object):

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data')
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        # TODO: parse actual addons from CMSG_AUTH_SESSION
        response = b'\x02\x01\x00\x00\x00\x00\x00\x00' * 16
        return WorldOpCode.SMSG_ADDON_INFO, [response]
