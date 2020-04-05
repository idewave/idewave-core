from World.Object.Constants.UpdateObjectFields import ObjectField, UnitField
from World.WorldPacket.UpdatePacket.Builders.UpdatePacketBuilder import UpdatePacketBuilder
from World.Object.Unit.NPC.Beast.Beast import Beast
from Typings.Abstract import AbstractHandler


class NPCSpawn(AbstractHandler):

    SPAWN_FIELDS = [
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
        UnitField.AURA,
        UnitField.AURAFLAGS,
        UnitField.AURALEVELS,
        UnitField.BASEATTACKTIME,
        UnitField.OFFHANDATTACKTIME,
        UnitField.RANGEDATTACKTIME,
        UnitField.BOUNDINGRADIUS,
        UnitField.COMBATREACH,
        UnitField.DISPLAYID,
        UnitField.NATIVEDISPLAYID,
        UnitField.MINDAMAGE,
        UnitField.MAXDAMAGE,
        UnitField.MOD_CAST_SPEED,
        UnitField.STAT0,
        UnitField.STAT1,
        UnitField.STAT2,
        UnitField.STAT3,
        UnitField.STAT4,
        UnitField.RESISTANCE_NORMAL,
        UnitField.BASE_HEALTH,
        UnitField.BYTES_2,
        UnitField.ATTACK_POWER,
        UnitField.RANGED_ATTACK_POWER,
        UnitField.MINRANGEDDAMAGE,
        UnitField.MAXRANGEDDAMAGE,
    ]

    def __init__(self, packet: bytes):
        self.packet = packet
        self.update_packet_builder = UpdatePacketBuilder()

    async def process(self):
        beast = Beast()
