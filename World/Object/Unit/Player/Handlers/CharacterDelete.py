from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from struct import pack
from World.Object.Unit.Player.CharacterManager import CharacterManager
from World.Character.Constants.CharDeleteResponseCode import CharDeleteResponseCode


class CharacterDelete(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        guid = int.from_bytes(self.packet[6:], 'little')
        CharacterManager().delete(id=guid)
        return WorldOpCode.SMSG_CHAR_DELETE, pack('<B', CharDeleteResponseCode.CHAR_DELETE_SUCCESS.value)
