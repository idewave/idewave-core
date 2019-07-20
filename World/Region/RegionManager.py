import asyncio
from sqlalchemy.orm.exc import DetachedInstanceError

from World.Region.model import Region
from World.Object.Unit.model import Unit
from World.Object.Unit.UnitManager import UnitManager
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.PlayerManager import PlayerManager
from DB.Connection.WorldConnection import WorldConnection
from World.Object.Constants.UpdateObjectFields import ObjectField, UnitField, PlayerField
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from Utils.Debug.Logger import Logger
from Server.Registry.QueuesRegistry import QueuesRegistry

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
        self.regions_as_json = [region.to_json() for region in self.regions]
        Logger.debug(self.regions_as_json)

    def get_region(self, **kwargs):
        # TODO: fix args receiving
        region_id = kwargs.pop('region_id', None)
        try:
            region = self.session.query(Region).filter_by(region_id=region_id).first()
        except Exception as e:
            raise Exception('[Region Manager]: get_region exception "{}"'.format(e))
        else:
            return region

    def create(self, **kwargs):
        region_id = kwargs.pop('region_id', None)
        y1 = kwargs.pop('y1', None)
        y2 = kwargs.pop('y2', None)
        x1 = kwargs.pop('x1', None)
        x2 = kwargs.pop('x2', None)
        continent_id = kwargs.pop('continent_id', None)

        self.region = Region()
        self.region.region_id = region_id
        self.region.y1 = y1
        self.region.y2 = y2
        self.region.x1 = x1
        self.region.x2 = x2
        self.region.continent_id = continent_id

        return self

    def load_all(self):
        return self.session.query(Region).all()

    def save(self):
        self.session.add(self.region)
        self.session.commit()
        return self

    def flush(self):
        self.session.add(self.region)
        self.session.flush()
        return self

    async def refresh_players(self, current_player: Player):
        for region in self.regions:
            region.online_players = current_player

        current_region = next(region for region in self.regions if region.id == current_player.region.id)
        online_players = current_region.online_players

        players = [online_players[name] for name in online_players if not name == current_player.name]

        # finally building packet for player that contains player list
        movement_flags = (
                UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
                UpdateObjectFlags.UPDATEFLAG_LIVING.value |
                UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value
        )

        update_packets = []

        for player in players:
            with PlayerManager() as player_mgr:
                player_mgr.set(player)
                player_mgr.movement.set_update_flags(movement_flags)

                batch_builder = player_mgr.prepare() \
                    .build_update_packet(RegionManager.PLAYER_SPAWN_FIELDS)

                update_packets.append(batch_builder)

        asyncio.ensure_future(
            QueuesRegistry.update_packets_queue.put((current_player.name, update_packets))
        )

    async def refresh_creatures(self):
        for region in self.regions:
            try:
                region_units = region.units.copy()
            except DetachedInstanceError as e:
                Logger.error('[Region Manager]: {}'.format(e))
            else:
                units = region_units.copy()

                # finally building packet for player that contains unit list
                movement_flags = (
                        UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
                        UpdateObjectFlags.UPDATEFLAG_LIVING.value |
                        UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value
                )

                spawn_dist = Config.World.Gameplay.spawn_dist

                if not spawn_dist == 0:
                    for player_name in region.online_players:
                        player = region.online_players[player_name]

                        # list of unit managers each ready to build the update packet
                        update_packets = []

                        if spawn_dist > 0:
                            units = [unit for unit in units if RegionManager._is_unit_in_spawn_radius(unit, player)]

                        for unit in units:
                            with UnitManager() as unit_mgr:
                                unit_mgr.set(unit)
                                unit_mgr.movement.set_update_flags(movement_flags)

                                batch_builder = unit_mgr.prepare() \
                                    .build_update_packet(RegionManager.UNIT_SPAWN_FIELDS)

                                update_packets.append(batch_builder)

                        asyncio.ensure_future(
                            QueuesRegistry.update_packets_queue.put((player.name, update_packets))
                        )


    @staticmethod
    def _is_unit_in_spawn_radius(unit: Unit, player: Player):
        spawn_dist = Config.World.Gameplay.spawn_dist
        if spawn_dist > 0:
            return (player.x - spawn_dist <= unit.x <= player.x + spawn_dist + 1) and \
                   (player.y - spawn_dist <= unit.y <= player.y + spawn_dist + 1)
