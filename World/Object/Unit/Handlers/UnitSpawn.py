from World.Object.Constants.UpdateObjectFields import ObjectField, ItemField, UnitField


class UnitSpawn(object):

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
        UnitField.DISPLAYID,
        UnitField.NATIVEDISPLAYID,
        UnitField.BASE_HEALTH
    ]

    def __init__(self, packet: bytes, **kwargs):
        pass

    async def process(self):
        pass
