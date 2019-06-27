from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class SpellGo(object):

    def __init__(self, packet: bytes):
        self.packet = packet

    async def process(self):
        return WorldOpCode.SMSG_SPELL_GO.value, b'\x01\x01\x01\x01dP\x00\x00\x00\x01\xcb\xd0\xa4\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x01'
