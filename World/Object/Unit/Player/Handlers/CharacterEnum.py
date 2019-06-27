from struct import pack
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Character.Constants.CharacterEquipSlot import CharacterEquipSlot
from World.Region.Constants.Kalimdor import Kalimdor
from World.Object.Unit.Player.CharacterManager import CharacterManager


class CharacterEnum(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.num_chars = 0
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self):
        characters = self._get_characters()
        return WorldOpCode.SMSG_CHAR_ENUM, pack('<B', self.num_chars) + characters

    def _get_characters(self):
        characters = CharacterManager().get_characters(account=self.temp_ref.account)
        self.num_chars = len(characters)

        if self.num_chars > 10:
            raise Exception('Max characters count equals to 10')

        return b"".join(characters)

    @staticmethod
    def _get_test_character_data(name='Test'):
        name_bytes = name.encode('utf-8') + b'\x00'
        data = pack(
            '<Q{name_len}s3B5BB2I3f2IB3I'.format(name_len=len(name_bytes)),
            8,                                     # guid             0
            name_bytes,                            # name             1
            4,                                     # race             2
            11,                                    # class            3
            1,                                     # gender           4
            0,                                     # skin             5
            0,                                     # face             5
            0,                                     # hair style       5
            0,                                     # hair color       5
            0,                                     # facial hair      6
            61,                                    # level            7
            Kalimdor.TELDRASSIL.value,             # zone id          8
            0,                                     # map id           9
            10322.1,                               # x                10
            825.436,                               # y                11
            1326.37,                               # z                12
            0,                                     # guild            13
            0,                                     # char flags ?     14
            0,                                     # first login      15
            0,                                     # pet display id   16
            0,                                     # pet level        17
            0                                      # pet family       18
        )

        # Equipment: display_id - item_type - enchant
        char_equipment = [
            {CharacterEquipSlot.HEAD.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.NECK.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.SHOULDERS.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.BODY.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.CHEST.value: pack('<IBI', 12683, 20, 0)},
            {CharacterEquipSlot.WAIST.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.LEGS.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.FEET.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.WRISTS.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.HANDS.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.FINGER1.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.FINGER2.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.TRINKET1.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.TRINKET2.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.BACK.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.MAINHAND.value: pack('<IBI', 40371, 17, 0)},
            {CharacterEquipSlot.OFFHAND.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.RANGED.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.TABARD.value: pack('<IBI', 0, 0, 0)},
            {CharacterEquipSlot.BAG1.value: pack('<IBI', 0, 0, 0)}
        ]

        return data + b''.join([item[index] for index, item in enumerate(char_equipment)])
