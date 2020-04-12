from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Typings.Abstract import AbstractHandler


class PingHandler(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())

    async def process(self) -> tuple:
        response = self.data
        return WorldOpCode.SMSG_PONG, [response]
