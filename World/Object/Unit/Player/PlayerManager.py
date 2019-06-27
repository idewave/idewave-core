from World.Object.Unit.UnitManager import UnitManager
from World.Object.Unit.Player.model import Player
from World.Object.Constants.UpdateObjectFields import PlayerField
from World.Character.Constants.CharacterRace import CharacterRace
from World.Character.Constants.CharacterGender import CharacterGender
from World.Object.Item.model import Item
from World.Character.Constants.CharacterEquipSlot import CharacterEquipSlot
from World.Object.Unit.Player.Inventory.Equipment.EquipmentManager import EquipmentManager
from World.Object.Unit.Player.Inventory.Equipment.model import Equipment
from World.Object.Unit.Builders.StatsBuilder import StatsBuilder
from World.Object.Position import Position
from World.Character.Constants.CharacterDisplayId import CHARACTER_DISPLAY_ID
from World.Object.Unit.Player.Config.StartLocation import START_LOCATION
from World.Region.model import Region

from Utils.Debug.Logger import Logger

from Config.Run.config import Config


class PlayerManager(UnitManager):

    MAX_INSPECTED_ENCHANTMENT_SLOT = 2

    NUM_SKILLS = 128

    def __init__(self, **kwargs):
        super(PlayerManager, self).__init__(**kwargs)
        self.world_object = Player()
        self.equipment = Equipment()
        self.temp_ref = kwargs.pop('temp_ref', None)

    @property
    def player(self):
        if self.world_object is None:
            raise Exception('Player is None')
        return self.world_object

    def add_player_fields(self):
        stats = StatsBuilder(self.player).build().get_stats()

        self.set_object_field(PlayerField.FLAGS, stats.player_flags)

        bytes_1 = (
            self.player.skin                 |
            self.player.face << 8            |
            self.player.hair_style << 16     |
            self.player.hair_color << 24
        )

        bytes_2 = (
            self.player.facial_hair          |
            # TODO: debug values below
            0x00 << 8                            |
            0x00 << 16                           |
            0x02 << 24
        )

        bytes_3 = self.player.gender

        self.set_object_field(PlayerField.BYTES_1, bytes_1)
        self.set_object_field(PlayerField.BYTES_2, bytes_2)
        self.set_object_field(PlayerField.BYTES_3, bytes_3)

        self.set_object_field(PlayerField.XP, stats.xp)
        self.set_object_field(PlayerField.NEXT_LEVEL_XP, stats.next_level_xp)

        self.set_object_field(PlayerField.CHARACTER_POINTS1, stats.character_points_1)
        self.set_object_field(PlayerField.CHARACTER_POINTS2, stats.character_points_2)

        self.set_object_field(PlayerField.BLOCK_PERCENTAGE, stats.block)
        self.set_object_field(PlayerField.DODGE_PERCENTAGE, stats.dodge)
        self.set_object_field(PlayerField.PARRY_PERCENTAGE, stats.parry)
        self.set_object_field(PlayerField.CRIT_PERCENTAGE, stats.crit)
        # TODO: set to own param
        self.set_object_field(PlayerField.RANGED_CRIT_PERCENTAGE, stats.crit)

        self.set_object_field(PlayerField.REST_STATE_EXPERIENCE, stats.rest_state_exp)
        self.set_object_field(PlayerField.COINAGE, stats.money)

        # TODO: set to actual
        self.set_object_field(PlayerField.WATCHED_FACTION_INDEX, -1) # -1 is default (according to Mangos)
        self.set_object_field(PlayerField.BYTES, 0)
        self.set_object_field(PlayerField.MAX_LEVEL, Config.World.Object.Unit.Player.Defaults.max_level)

        # equipment
        for slot in range(CharacterEquipSlot.HEAD.value, CharacterEquipSlot.BAG1.value):
            # item = self.equipment.get_object_field(CharacterEquipSlot(slot))
            # item = self.equipment.get_item(CharacterEquipSlot(slot))
            item = self.equipment[CharacterEquipSlot(slot)].item

            if item is not None:
                # set VISIBLE_ITEM_1_0 + offset
                visible_item_index = PlayerField.VISIBLE_ITEM_1_0.value + (slot * 16)
                self.set_object_field(PlayerField(visible_item_index), item.item_template.entry)
                # set INV_SLOT_HEAD + offset
                inv_slot_index = PlayerField.INV_SLOT_HEAD.value + (slot * 2)
                self.set_object_field(PlayerField(inv_slot_index), item.guid)

                self.set_object_field(PlayerField.MOD_DAMAGE_NORMAL_DONE_PCT, 1)

    def _set_display_id(self):
        race = CharacterRace(self.player.race)
        gender = CharacterGender(self.player.gender)
        display_id = CHARACTER_DISPLAY_ID[race][gender]
        self.player.display_id = self.player.native_display_id = display_id

    # def add_skill(self, skill_id: int, min: int, max: int):
    #     skill = Skill(id=skill_id, min=min, max=max)
    #     self.player.skills.append(skill)
    #
    # def add_spell(self, spell_id: int):
    #     spell = Spell(id=spell_id)
    #     self.player.spells.append(spell)

    def equip_item(self, slot: CharacterEquipSlot, item: Item):
        self.player.equipment.set_object_field(slot, item)

    def _set_start_location(self):
        race = CharacterRace(self.player.race)
        coords = START_LOCATION[race]

        # position = Position(
        #     x=coords['x'],
        #     y=coords['y'],
        #     z=coords['z'],
        #     region_id=coords['region_id'],
        #     map_id=coords['map_id']
        # )

        self.player.x = coords['x']
        self.player.y = coords['y']
        self.player.z = coords['z']
        self.player.orientation = float(0)

        region = self.session.query(Region).filter_by(region_id=coords['region_id']).first()

        # self.player.region_id = position.region_id
        self.player.region = region
        self.player.map_id = coords['map_id']

        # initialize movement data for building update packets
        # self.movement.position = position

    def _set_default_equipment(self):
        self.equipment = EquipmentManager(session=self.session).set_default_equipment(player=self.player).get_items()

    def _set_faction_template_id(self):
        race = CharacterRace(self.player.race)
        self.player.faction_template = CHARACTER_DISPLAY_ID[race]['faction_template']

    # overridable
    def load(self, **kwargs):
        id = kwargs.pop('id')
        self.world_object = self.session.query(Player).filter_by(id=id).first()
        return self

    # overridable
    def new(self, **kwargs):
        self.player.race = kwargs.pop('race', None)
        self.player.char_class = kwargs.pop('char_class', None)
        self.player.gender = kwargs.pop('gender', None)
        self.player.name = kwargs.pop('name', None)
        self.player.skin = kwargs.pop('skin', None)
        self.player.face = kwargs.pop('face', None)
        self.player.hair_style = kwargs.pop('hair_style', None)
        self.player.hair_color = kwargs.pop('hair_color', None)
        self.player.facial_hair = kwargs.pop('facial_hair', None)

        self.player.level = Config.World.Object.Unit.Player.Defaults.min_level
        self.player.account = self.temp_ref.account

        self._set_start_location()
        self._set_display_id()
        self._set_faction_template_id()

        # save player for id generating
        self.session.add(self.player)
        self.session.flush()

        self._set_default_equipment()

        self.stats_builder = StatsBuilder(self.world_object)

        return self

    def prepare(self):
        super(PlayerManager, self).prepare()
        self.equipment = EquipmentManager(session=self.session).get_equipment(player=self.player).get_items()
        self.add_player_fields()
        return self

    def __del__(self):
        self.session.close()
