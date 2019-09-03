import asyncio

from struct import pack
from typing import List

from World.Region.model import Region, DefaultLocation
from World.Object.Unit.model import Unit
from World.Object.Unit.Player.model import Player

from World.Object.ObjectManager import ObjectManager
from World.Object.Unit.Player.PlayerManager import PlayerManager

from World.Object.Constants.UpdateObjectFields import ObjectField, UnitField, PlayerField
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType

from DB.Connection.WorldConnection import WorldConnection
from Server.Registry.QueuesRegistry import QueuesRegistry

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode

from Utils.Debug.Logger import Logger

from Config.Run.config import Config


class RegionManager(object):

    PLAYER_SPAWN_FIELDS = [
        # Object fields
        ObjectField.GUID,
        ObjectField.TYPE,
        ObjectField.SCALE_X,

        # Unit fields
        UnitField.HEALTH,
        UnitField.MAXHEALTH,
        UnitField.LEVEL,
        UnitField.FACTIONTEMPLATE,
        UnitField.BYTES_0,
        UnitField.FLAGS,
        UnitField.DISPLAYID,
        UnitField.NATIVEDISPLAYID,
        UnitField.BASE_HEALTH,

        # Player fields
        PlayerField.FLAGS,
        PlayerField.BYTES_1,
        PlayerField.BYTES_2,

        PlayerField.VISIBLE_ITEM_1_0,
        PlayerField.VISIBLE_ITEM_2_0,
        PlayerField.VISIBLE_ITEM_3_0,
        PlayerField.VISIBLE_ITEM_4_0,
        PlayerField.VISIBLE_ITEM_5_0,
        PlayerField.VISIBLE_ITEM_6_0,
        PlayerField.VISIBLE_ITEM_7_0,
        PlayerField.VISIBLE_ITEM_8_0,
        PlayerField.VISIBLE_ITEM_9_0,
        PlayerField.VISIBLE_ITEM_10_0,
        PlayerField.VISIBLE_ITEM_11_0,
        PlayerField.VISIBLE_ITEM_12_0,
        PlayerField.VISIBLE_ITEM_13_0,
        PlayerField.VISIBLE_ITEM_14_0,
        PlayerField.VISIBLE_ITEM_15_0,
        PlayerField.VISIBLE_ITEM_16_0,
        PlayerField.VISIBLE_ITEM_17_0,

        PlayerField.INV_SLOT_HEAD,
        PlayerField.INV_SLOT_NECK,
        PlayerField.INV_SLOT_SHOULDERS,
        PlayerField.INV_SLOT_BODY,
        PlayerField.INV_SLOT_CHEST,
        PlayerField.INV_SLOT_WAIST,
        PlayerField.INV_SLOT_LEGS,
        PlayerField.INV_SLOT_FEET,
        PlayerField.INV_SLOT_WRISTS,
        PlayerField.INV_SLOT_HANDS,
        PlayerField.INV_SLOT_FINGER1,
        PlayerField.INV_SLOT_FINGER2,
        PlayerField.INV_SLOT_TRINKET1,
        PlayerField.INV_SLOT_TRINKET2,
        PlayerField.INV_SLOT_BACK,
        PlayerField.INV_SLOT_MAINHAND,
        PlayerField.INV_SLOT_OFFHAND,
        PlayerField.INV_SLOT_RANGED,
        PlayerField.INV_SLOT_TABARD
    ]

    UNIT_SPAWN_FIELDS = [
        # Object fields
        ObjectField.GUID,
        ObjectField.TYPE,
        ObjectField.ENTRY,
        ObjectField.SCALE_X,

        # Unit fields
        UnitField.HEALTH,
        UnitField.MAXHEALTH,
        UnitField.POWER1,
        UnitField.POWER2,
        UnitField.POWER3,
        UnitField.POWER4,
        UnitField.POWER5,
        UnitField.MAXPOWER1,
        UnitField.MAXPOWER2,
        UnitField.MAXPOWER3,
        UnitField.MAXPOWER4,
        UnitField.MAXPOWER5,
        UnitField.LEVEL,
        UnitField.FACTIONTEMPLATE,
        UnitField.DISPLAYID,
        UnitField.NATIVEDISPLAYID,
        UnitField.BASE_HEALTH,
        # UnitField.BASE_MANA,
        UnitField.BYTES_0,
        UnitField.FLAGS,
        UnitField.COMBATREACH,
        UnitField.BOUNDINGRADIUS,
        UnitField.NPC_FLAGS,
    ]

    def __init__(self, **kwargs):
        external_session = kwargs.pop('session', None)

        if external_session:
            self.session = external_session
        else:
            connection = WorldConnection()
            self.session = connection.session

        self.region = None
        self.regions = self.load_all()

    def get_regions_as_json(self):
        return [region.to_json() for region in self.regions];

    def get_region(self, **kwargs):
        # TODO: fix args receiving
        identifier = kwargs.pop('identifier', None)
        try:
            region = self.session.query(Region).filter_by(identifier=identifier).first()
        except Exception as e:
            raise Exception('[Region Manager]: get_region exception "{}"'.format(e))
        else:
            return region

    def create(self, **kwargs):
        identifier = kwargs.pop('identifier', None)
        y1 = kwargs.pop('y1', None)
        y2 = kwargs.pop('y2', None)
        x1 = kwargs.pop('x1', None)
        x2 = kwargs.pop('x2', None)
        continent_id = kwargs.pop('continent_id', None)

        self.region = Region()
        self.region.identifier = identifier
        self.region.y1 = y1
        self.region.y2 = y2
        self.region.x1 = x1
        self.region.x2 = x2
        self.region.continent_id = continent_id

        return self

    def create_default_location(self, **kwargs):
        identifier = kwargs.pop('identifier', None)
        x = kwargs.pop('x', None)
        y = kwargs.pop('y', None)
        z = kwargs.pop('z', None)
        map_id = kwargs.pop('map_id', None)
        race = kwargs.pop('race', None)

        region = self.session.query(Region).filter_by(identifier=identifier).first()

        default_location = DefaultLocation()
        default_location.region = region
        default_location.x = x
        default_location.y = y
        default_location.z = z
        default_location.map_id = map_id
        default_location.race = race

        self.session.add(default_location)
        self.session.commit()

    def load_all(self):
        return self.session.query(Region).all()

    def save(self):
        self.session.add(self.region)
        self.session.commit()
        return self

    def add_player(self, player: Player):
        current_region: Region = self._get_current_region(player)
        current_region.update_player(player)

        nearest_players = RegionManager._get_nearest_players(current_region, player)

        # notify player about players in region
        RegionManager._notify_nearest_players(player, nearest_players)

        # notify each player about new player
        for target in nearest_players:
            RegionManager._notify_nearest_players(target, [player])

    def update_player_movement(self, player: Player, opcode: WorldOpCode, packet: bytes):
        current_region: Region = self._get_current_region(player)
        current_region.update_player(player)

        nearest_players = RegionManager._get_nearest_players(current_region, player)

        for target in nearest_players:
            RegionManager._notify_nearest_players(
                target,
                [player],
                movement_packet=(opcode, packet),
            )

    def remove_player(self, player: Player):
        current_region: Region = self._get_current_region(player)
        current_region.remove_player(player)

        # notify nearest players that current player was disconnected
        nearest_players = RegionManager._get_nearest_players(current_region, player)

    def send_chat_message(self, sender: Unit, text_message_packet: bytes):
        current_region: Region = self._get_current_region(sender)

        # TODO: in future we can also notify nearest units about messages
        nearest_players = RegionManager._get_nearest_players(current_region, sender)

        for target in nearest_players:
            RegionManager._notify_nearest_players(
                target,
                None,
                text_message_packet=text_message_packet,
            )

    def send_name_query(self, requester: Player, target_guid: int):
        current_region: Region = self._get_current_region(requester)

        target = current_region.get_online_player_by_guid(target_guid)

        if target:
            name_bytes = target.name.encode('utf-8') + b'\x00'
            name_query_packet = pack(
                '<Q{name_len}sB3IB'.format(name_len=len(name_bytes)),
                target.guid,
                name_bytes,
                0,
                target.race,
                target.gender,
                target.char_class,
                0
            )

            asyncio.ensure_future(
                QueuesRegistry.name_query_packets_queue.put((requester.name, name_query_packet))
            )

    def _get_current_region(self, target: Unit):
        current_region = None

        for region in self.regions:
            if region.identifier == target.region.identifier:
                current_region = region
                break

        if current_region is None:
            raise Exception('[RegionMgr]: target has unknown region id')

        return current_region

    @staticmethod
    def _get_nearest_players(current_region: Region, unit: Unit):
        online_players = current_region.get_online_players()
        nearest_players = [
            online_players[name]
            for name in online_players
            if not name == unit.name and RegionManager._is_target_visible(unit, online_players[name])
        ]

        return nearest_players

    @staticmethod
    def _notify_nearest_players(player: Player, targets: List[Player] = None, **kwargs):

        opcode, packet = kwargs.pop('movement_packet', (None, None))

        text_message_packet = kwargs.pop('text_message_packet', None)

        if opcode and packet:
            packet = targets.pop(0).packed_guid + packet
            asyncio.ensure_future(
                QueuesRegistry.movement_packets_queue.put((player.name, packet, opcode))
            )

        elif text_message_packet:
            asyncio.ensure_future(
                QueuesRegistry.text_message_packets_queue.put((player.name, text_message_packet))
            )

        else:
            update_flags = (
                UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
                UpdateObjectFlags.UPDATEFLAG_LIVING.value |
                UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value
            )

            targets = targets.copy()

            object_update_type = kwargs.pop('object_update_type', ObjectUpdateType.CREATE_OBJECT2)

            with PlayerManager() as head_player_mgr:
                RegionManager._init_update_packet_builder(
                    head_player_mgr,
                    object_update_type=object_update_type,
                    update_flags=update_flags,
                    update_object=targets.pop(0)
                )

                batch = head_player_mgr.create_batch(RegionManager.PLAYER_SPAWN_FIELDS)
                head_player_mgr.add_batch(batch)

                if targets:
                    for target in targets:
                        with PlayerManager() as player_mgr:
                            RegionManager._init_update_packet_builder(
                                player_mgr,
                                object_update_type=ObjectUpdateType.CREATE_OBJECT2,
                                update_flags=update_flags,
                                update_object=target
                            )

                            batch = player_mgr.create_batch(RegionManager.PLAYER_SPAWN_FIELDS)
                            head_player_mgr.add_batch(batch)

                update_packets = head_player_mgr.build_update_packet().get_update_packets()

                asyncio.ensure_future(QueuesRegistry.update_packets_queue.put((player.name, update_packets)))

    @staticmethod
    def _init_update_packet_builder(mgr: ObjectManager, **kwargs):
        # initialize update packet builder in the mgr.prepare()
        object_update_type = kwargs.pop('object_update_type')
        update_flags = kwargs.pop('update_flags')
        update_object = kwargs.pop('update_object')

        mgr.set_object_update_type(object_update_type=object_update_type)
        mgr.set(update_object)
        mgr.prepare().set_update_flags(update_flags)

    # async def refresh_creatures(self):
    #     for region in self.regions:
    #         try:
    #             units = region.units.copy()
    #         except DetachedInstanceError as e:
    #             Logger.error('[Region Manager]: {}'.format(e))
    #         else:
    #             # finally building packet for player that contains unit list
    #             movement_flags = (
    #                     UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
    #                     UpdateObjectFlags.UPDATEFLAG_LIVING.value |
    #                     UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value
    #             )
    #
    #             spawn_dist = Configs.World.Gameplay.spawn_dist
    #
    #             online_players = region.get_online_players()
    #
    #             if not spawn_dist == 0:
    #                 for player_name in online_players:
    #                     player = online_players[player_name]
    #
    #                     # list of unit managers each ready to build the update packet
    #                     update_packets = []
    #
    #                     if spawn_dist > 0:
    #                         units = [unit for unit in units if RegionManager._is_unit_in_spawn_radius(unit, player)]
    #
    #                     for unit in units:
    #                         with UnitManager() as unit_mgr:
    #                             unit_mgr.set(unit)
    #                             unit_mgr.movement.set_update_flags(movement_flags)
    #
    #                             batch_builder = unit_mgr.prepare() \
    #                                 .build_update_packet(RegionManager.UNIT_SPAWN_FIELDS)
    #
    #                             update_packets.append(batch_builder)
    #
    #                     asyncio.ensure_future(
    #                         QueuesRegistry.update_packets_queue.put((player.name, update_packets))
    #                     )
    #
    #             del units


    @staticmethod
    def _is_target_visible(unit: Unit, target: Unit):
        update_dist = Config.World.Gameplay.update_dist
        if update_dist > 0:
            return (unit.x - update_dist <= target.x <= unit.x + update_dist + 1) and \
                   (unit.y - update_dist <= target.y <= unit.y + update_dist + 1)

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = WorldConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return True
