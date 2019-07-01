from sqlalchemy.orm.exc import DetachedInstanceError

from World.Region.model import Region
from World.Object.Unit.model import Unit
from World.Object.Unit.UnitManager import UnitManager
from World.Object.Unit.Player.model import Player
from DB.Connection.WorldConnection import WorldConnection
from World.Object.Constants.UpdateObjectFields import ObjectField, UnitField
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from Utils.Debug.Logger import Logger
from Server.Registry.QueuesRegistry import QueuesRegistry

from Config.Run.config import Config


class RegionManager(object):

    UNITS_PLAYER_FIELDS = [
        # Object fields
        ObjectField.GUID,
        ObjectField.TYPE,
        ObjectField.SCALE_X,
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

    async def refresh(self):
        for region in self.regions:
            try:
                region_units = region.units.copy()
            except DetachedInstanceError as e:
                Logger.error('[Region Manager]: {}'.format(e))
            except Exception as e:
                Logger.error('[Region Manager]: another exception {}'.format(e))
            else:
                units = region_units.copy()

                # finally building packet for player that contains unit list
                movement_flags = (
                        UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
                        UpdateObjectFlags.UPDATEFLAG_LIVING.value |
                        UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value
                )

                # list of unit managers each ready to build the update packet
                update_packets = []

                spawn_dist = Config.World.Gameplay.spawn_dist

                if not spawn_dist == 0:
                    for player in region.players:
                        if spawn_dist > 0:
                            units = [unit for unit in units if RegionManager._is_unit_in_spawn_radius(unit, player)]

                        for unit in units:
                            unit_mgr = UnitManager()
                            unit_mgr.set(unit)
                            unit_mgr.movement.set_update_flags(movement_flags)

                            batch_builder = unit_mgr.prepare().build_update_packet(RegionManager.UNIT_SPAWN_FIELDS)

                            update_packets.append(batch_builder)
                            await QueuesRegistry.update_packets_queue.put((player.name, update_packets))

    @staticmethod
    def _is_unit_in_spawn_radius(unit: Unit, player: Player):
        spawn_dist = Config.World.Gameplay.spawn_dist
        if spawn_dist > 0:
            return (player.x - spawn_dist <= unit.x <= player.x + spawn_dist + 1) and \
                   (player.y - spawn_dist <= unit.y <= player.y + spawn_dist + 1)
