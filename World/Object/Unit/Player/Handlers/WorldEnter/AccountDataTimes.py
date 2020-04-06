from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Typings.Abstract import AbstractHandler


class AccountDataTimes(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        response = b'\x00' * 128
        return WorldOpCode.SMSG_ACCOUNT_DATA_TIMES, [response]
