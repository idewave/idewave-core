from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class AuraDuration(object):

    def __init__(self, packet: bytes):
        self.packet = packet

    async def process(self):
        response = b'\x00\xff\xff\xff\xff'
        return WorldOpCode.SMSG_UPDATE_AURA_DURATION.value, response
