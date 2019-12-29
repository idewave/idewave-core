from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Unit.Player.CharacterManager import CharacterManager
from World.Object.Unit.Player.Constants.CharDeleteResponseCode import CharDeleteResponseCode
from Server.Connection.Connection import Connection


class CharacterDelete(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        guid = int.from_bytes(self.data, 'little')
        CharacterManager().delete(id=guid)

        response = pack('<B', CharDeleteResponseCode.CHAR_DELETE_SUCCESS.value)
        return WorldOpCode.SMSG_CHAR_DELETE, [response]
