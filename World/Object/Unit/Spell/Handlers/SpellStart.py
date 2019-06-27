from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from struct import pack
from Login.SessionStorage import session
from io import BytesIO
from World.Object.Unit.Spell.Constants.SpellCastFlags import SpellCastFlags


class SpellStart(object):

    def __init__(self, packet: bytes):
        self.packet = packet

    async def process(self):
        buf = BytesIO(self.packet)

        castFlags = SpellCastFlags.CAST_FLAG_UNKNOWN2.value

        response = bytes()
        response += session.player.packed_guid
        response += session.player.packed_guid
        response += pack(
            '<IBHI',
            int.from_bytes(buf.read(4), 'little'),          # spell id
            1,                                              # cast count, currently 1 (for test)
            castFlags,
            0,                                              # timer
        )

        response += session.player.packed_guid

        return WorldOpCode.SMSG_SPELL_START.value, response #b'\x01\x01\x01\x01dP\x00\x00\x00\x02\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x01'
