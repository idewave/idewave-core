from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Server.CustomExceptions.CharactersLimitError import CharactersLimitError
from World.Object.Unit.Player.CharacterManager import CharacterManager
from Typings.Abstract import AbstractHandler


class CharacterEnum(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')
        self.num_chars = 0

    async def process(self) -> tuple:
        characters = self._get_characters()
        response = pack('<B', self.num_chars) + characters
        return WorldOpCode.SMSG_CHAR_ENUM, [response]

    def _get_characters(self):
        characters = CharacterManager().get_characters(account=self.connection.account)
        self.num_chars = len(characters)

        if self.num_chars > 10:
            raise CharactersLimitError

        return b"".join(characters)
