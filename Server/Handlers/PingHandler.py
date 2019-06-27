from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class PingHandler(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        return WorldOpCode.SMSG_PONG, self.packet
