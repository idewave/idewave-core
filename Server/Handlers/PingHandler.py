from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class PingHandler(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())

    async def process(self) -> tuple:
        response = self.data
        return WorldOpCode.SMSG_PONG, [response]
