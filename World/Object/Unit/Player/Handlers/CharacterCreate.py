from io import BytesIO
from struct import pack, unpack
from sqlalchemy.exc import IntegrityError

from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Character.Constants.CharacterRace import CharacterRace
from World.Character.Constants.CharacterClass import CharacterClass
from World.Character.Constants.CharacterGender import CharacterGender
from World.Character.Constants.CharCreateResponseCode import CharCreateResponseCode
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Utils.Debug.Logger import Logger
from Utils.AccountNameParser import AccountNameParser

from Exceptions.Wrappers.ProcessException import ProcessException


class CharacterCreate(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    @property
    def exception_handlers(self) -> dict:
        return {
            IntegrityError: CharacterCreate.get_response_name_in_use
        }

    @ProcessException(exception_handlers)
    async def process(self) -> tuple:
        data = self._parse_packet()

        with PlayerManager() as player_mgr:
            player_mgr.new(
                name=data['name'],
                race=data['race'],
                char_class=data['char_class'],
                gender=data['gender'],
                skin=data['skin'],
                face=data['face'],
                hair_style=data['hair_style'],
                hair_color=data['hair_color'],
                facial_hair=data['facial_hair'],
                account=self.connection.account
            )

            Logger.notify('Character "{}" created'.format(data['name']))

            response = pack('<B', CharCreateResponseCode.CHAR_CREATE_SUCCESS.value)
            return WorldOpCode.SMSG_CHAR_CREATE, [response]

    @staticmethod
    def get_response_name_in_use():
        response = pack('<B', CharCreateResponseCode.CHAR_CREATE_NAME_IN_USE.value)
        return WorldOpCode.SMSG_CHAR_CREATE, [response]

    def _parse_packet(self) -> dict:
        # omit first 6 bytes, cause 01-02 = packet size, 03-04 = opcode (0x1ED), 05-06 - unknown null-bytes
        tmp_buf = BytesIO(self.data)

        result = dict()

        result['name'] = AccountNameParser.parse(tmp_buf)

        char_data = unpack('<9B', tmp_buf.read(9))
        result['race'] = CharacterRace(char_data[0]).value
        result['char_class'] = CharacterClass(char_data[1]).value
        result['gender'] = CharacterGender(char_data[2]).value

        features = char_data[3:8]
        result['skin'] = features[0]
        result['face'] = features[1]
        result['hair_style'] = features[2]
        result['hair_color'] = features[3]
        result['facial_hair'] = features[4]

        return result
