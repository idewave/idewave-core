from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class ExtraAuraInfo(object):

    def __init__(self, packet: bytes):
        self.packet = packet

    async def process(self):
        response = b'\x01\x01\x00dP\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff'
        return WorldOpCode.SMSG_SET_EXTRA_AURA_INFO.value, response
