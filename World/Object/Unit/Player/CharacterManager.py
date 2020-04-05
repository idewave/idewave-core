from struct import pack

from DB.Connection.RealmConnection import RealmConnection
from Account.model import Account
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.Inventory.Equipment.EquipmentManager import EquipmentManager


class CharacterManager(object):

    def __init__(self):
        connection = RealmConnection()
        self.engine = connection.engine
        self.session = connection.session

    def get_characters(self, account: Account):
        players = self.session.query(Player).filter_by(account=account).all()
        return [CharacterManager.to_bytes(player) for player in players]

    @staticmethod
    def to_bytes(player: Player):
        name_bytes = player.name.encode('utf-8') + b'\x00'
        data = pack(
            '<Q{name_len}s3B5BB2I3f2IB3I'.format(name_len=len(name_bytes)),
            player.guid,                                # guid             0
            player.name.encode('utf-8') + b'\x00',      # name             1
            player.race,                                # race             2
            player.char_class,                          # class            3
            player.gender,                              # gender           4
            player.skin,                                # skin             5
            player.face,                                # face             5
            player.hair_style,                          # hair style       5
            player.hair_color,                          # hair color       5
            player.facial_hair,                         # facial hair      6
            player.level,                               # level            7
            player.region.identifier,                   # zone id          8
            player.map_id,                              # map id           9
            player.x,                                   # x                10
            player.y,                                   # y                11
            player.z,                                   # z                12
            0,                                          # guild            13
            0,                                          # char flags ?     14
            0,                                          # first login      15
            0,                                          # pet display id   16
            0,                                          # pet level        17
            0                                           # pet family       18
        )

        # Equipment: display_id - item_type - enchant
        with EquipmentManager() as equipment_mgr:
            equipment = equipment_mgr.get_equipment(player).to_bytes()
            return data + equipment

    def delete(self, **kwargs):
        self.session.query(Player).filter_by(**kwargs).delete()
        self.session.commit()
