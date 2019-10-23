from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Server.CustomExceptions.CharactersLimitError import CharactersLimitError
from World.Object.Unit.Player.CharacterManager import CharacterManager

from Exceptions.Wrappers.ProcessException import ProcessException


class CharacterEnum(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')
        self.num_chars = 0

    async def process(self):
        characters = self._get_characters()
        response = pack('<B', self.num_chars) + characters
        return WorldOpCode.SMSG_CHAR_ENUM, [response]

    @ProcessException
    def _get_characters(self):
        characters = CharacterManager().get_characters(account=self.connection.account)
        self.num_chars = len(characters)

        if self.num_chars > 10:
            raise CharactersLimitError

        return b"".join(characters)
