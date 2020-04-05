from struct import pack
from io import BytesIO

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Unit.Spell.Constants.SpellCastFlags import SpellCastFlags
from Server.Connection.Connection import Connection
from Typings.Abstract import AbstractHandler


class SpellStart(AbstractHandler):

    __slots__ = ('data', 'connection')

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        buf = BytesIO(self.data)
        player = self.connection.player
        cast_flags = SpellCastFlags.CAST_FLAG_UNKNOWN2.value

        spell_id = int.from_bytes(buf.read(4), 'little')

        response = bytes()
        response += player.packed_guid
        response += player.packed_guid
        response += pack(
            '<IBHI',
            spell_id,                               # spell id
            1,                                      # cast count, currently 1 (for test)
            cast_flags,
            0,                                      # timer
        )

        response += player.packed_guid

        return WorldOpCode.SMSG_SPELL_START, [response]
