from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class RealmSplit(object):

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data')
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        split_date = '01/01/01'
        response = pack('<2I', 0, 0) + split_date.encode('utf-8')
        return WorldOpCode.SMSG_REALM_SPLIT, [response]
