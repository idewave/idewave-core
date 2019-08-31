from io import BytesIO
from struct import pack, unpack
from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Character.Constants.CharacterRace import CharacterRace
from World.Character.Constants.CharacterClass import CharacterClass
from World.Character.Constants.CharacterGender import CharacterGender
from World.Character.Constants.CharCreateResponseCode import CharCreateResponseCode
from Utils.Debug.Logger import Logger
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class CharacterCreate(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self):
        data = self._parse_packet()

        with PlayerManager(temp_ref=self.temp_ref) as player_mgr:
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
            ).save()

            Logger.notify('Character "{}" created'.format(data['name']))

            return WorldOpCode.SMSG_CHAR_CREATE, pack('<B', CharCreateResponseCode.CHAR_CREATE_SUCCESS.value)

    def _parse_packet(self):
        # omit first 6 bytes, cause 01-02 = packet size, 03-04 = opcode (0x1ED), 05-06 - unknown null-bytes
        tmp_buf = BytesIO(self.packet[6:])

        result = dict()

        result['name'] = CharacterCreate._parse_account_name(tmp_buf)

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

    @staticmethod
    def _parse_account_name(buffer: BytesIO):
        Logger.info('[Character Create]: parsing account name')
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result.decode('utf-8')
