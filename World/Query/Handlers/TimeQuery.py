from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection

from Utils.Timer import Timer


class TimeQuery(object):

    __slots__ = ('data', 'connection')

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        response = pack(
            '<2I',
            Timer.get_ms_time(),
            0
        )
        return WorldOpCode.SMSG_QUERY_TIME_RESPONSE, [response]
