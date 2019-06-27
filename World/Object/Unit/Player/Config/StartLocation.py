from World.Character.Constants.CharacterRace import CharacterRace
from World.Region.Constants.Kalimdor import Kalimdor
from World.Region.Constants.EasternKingdoms import EasternKingdoms

# TODO: should be moved to DB
START_LOCATION = {
    CharacterRace.HUMAN: {
        'x': -8949.95,
        'y': -132.493,
        'z': 83.5312,
        'region_id': EasternKingdoms.ELWYNN_FOREST.value,
        'map_id': 0
    },

    CharacterRace.ORC: {
        'x': -618.518,
        'y': -4251.67,
        'z': 38.718,
        'region_id': Kalimdor.DUROTAR.value,
        'map_id': 1
    },

    CharacterRace.DWARF: {
        'x': -6240.32,
        'y': 331.033,
        'z': 382.758,
        'region_id': EasternKingdoms.DUN_MOROGH.value,
        'map_id': 0
    },

    CharacterRace.NIGHT_ELF: {
        'x': 10311.3,
        'y': 832.463,
        'z': 1326.41,
        'region_id': Kalimdor.TELDRASSIL.value,
        'map_id': 1
    },

    CharacterRace.UNDEAD: {
        'x': 1676.71,
        'y': 1678.31,
        'z': 121.67,
        'region_id': EasternKingdoms.TIRISFAL_GLADES.value,
        'map_id': 0
    },

    CharacterRace.TAUREN: {
        'x': -2917.58,
        'y': -257.98,
        'z': 52.9968,
        'region_id': Kalimdor.MULGORE.value,
        'map_id': 1
    },

    CharacterRace.GNOME: {
        'x': -6240.32,
        'y': 331.033,
        'z': 382.758,
        'region_id': EasternKingdoms.DUN_MOROGH.value,
        'map_id': 0
    },

    CharacterRace.TROLL: {
        'x': -618.518,
        'y': -4251.67,
        'z': 38.718,
        'region_id': Kalimdor.DUROTAR.value,
        'map_id': 1
    },

    CharacterRace.BLOOD_ELF: {
        'x': 10349.6,
        'y': -6357.29,
        'z': 33.4026,
        'region_id': EasternKingdoms.EVERSONG_WOODS.value,
        'map_id': 530
    },

    CharacterRace.DRAENEI: {
        'x': -3961.64,
        'y': -13931.2,
        'z': 100.615,
        'region_id': Kalimdor.AZUREMYST_ISLE.value,
        'map_id': 530
    }
}