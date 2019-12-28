from asyncio import ensure_future
from typing import List

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Unit.UnitManager import UnitManager
from World.Object.Unit.Player.model import Player
from World.Object.Constants.UpdateObjectFields import PlayerField
from World.Object.Unit.Player.Inventory.Equipment.EquipmentManager import EquipmentManager
from World.Object.Unit.Player.Skill.SkillManager import SkillManager
from World.Object.Unit.Spell.SpellManager import SpellManager
from World.Object.Unit.Player.Inventory.Equipment.model import Equipment
from World.Object.Unit.Builders.StatsBuilder import StatsBuilder
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from World.Object.Unit.Player.Constants.PlayerSpawnFields import PLAYER_SPAWN_FIELDS
from World.Character.Constants.CharacterRace import CharacterRace
from World.Character.Constants.CharacterGender import CharacterGender
from World.Character.Constants.CharacterEquipSlot import CharacterEquipSlot
from World.Character.Constants.CharacterDisplayId import CHARACTER_DISPLAY_ID
from World.Region.model import DefaultLocation

from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType

from Utils.Debug.Logger import Logger

from Server.Registry.QueuesRegistry import QueuesRegistry

from Config.Run.config import Config


class PlayerManager(UnitManager):

    __slots__ = ('world_object', 'equipment', 'connection')

    MAX_INSPECTED_ENCHANTMENT_SLOT = 2

    NUM_SKILLS = 128

    def __init__(self, **kwargs):
        super(PlayerManager, self).__init__(**kwargs)
        self.world_object = Player()
        self.equipment = Equipment()

    @property
    def player(self):
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

    # def equip_item(self, slot: CharacterEquipSlot, item: Item):
    #     self.player.equipment.set_object_field(slot, item)

    def set_default_equipment(self):
        self.session.expunge(self.player.region)
        self.session.expunge(self.player.account)
        self.session.expunge(self.player)

        with EquipmentManager() as equipment_mgr:
            self.equipment = equipment_mgr.set_default_equipment(player=self.player).get_items()
            return self

    def set_default_skills(self):
        with SkillManager() as skill_mgr:
            skill_mgr.set_default_skills(player=self.player)

    def set_default_spells(self):
        with SpellManager() as spell_mgr:
            spell_mgr.set_default_spells(player=self.player)

    def _set_start_location(self):
        location: DefaultLocation = self.session.query(DefaultLocation).filter_by(race=self.player.race).first()

        self.player.x = location.x
        self.player.y = location.y
        self.player.z = location.z
        self.player.orientation = float(0)

        self.player.region = location.region
        self.player.map_id = location.map_id

    def _set_faction_template_id(self):
        race = CharacterRace(self.player.race)
        self.player.faction_template = CHARACTER_DISPLAY_ID[race]['faction_template']

    # overridable
    def load(self, **kwargs):
        # id = kwargs.pop('id')
        # self.world_object = self.session.query(Player).filter_by(id=id).first()
        self.world_object = self.session.query(Player).filter_by(**kwargs).first()
        return self

    # overridable
    def new(self, **kwargs):
        self.player.race = kwargs.pop('race', None)
        self.player.char_class = kwargs.pop('char_class', None)
        self.player.gender = kwargs.pop('gender', None)
        self.player.name = kwargs.pop('name')
        self.player.skin = kwargs.pop('skin')
        self.player.face = kwargs.pop('face')
        self.player.hair_style = kwargs.pop('hair_style')
        self.player.hair_color = kwargs.pop('hair_color')
        self.player.facial_hair = kwargs.pop('facial_hair')

        self.player.level = Config.World.Object.Unit.Player.Defaults.min_level

        self.player.account = self.session.merge(kwargs.pop('account'))

        self._set_start_location()
        self._set_display_id()
        self._set_faction_template_id()

        # save player for id generating
        self.session.add(self.player)
        self.session.flush()

        self.stats_builder = StatsBuilder(self.player)

        self.set_stats()

        self.save()

        self.set_default_equipment()
        self.set_default_skills()
        self.set_default_spells()

        return self

    def prepare(self):
        super(PlayerManager, self).prepare()

        with EquipmentManager() as equipment_mgr:
            self.equipment = equipment_mgr.get_equipment(player=self.player).get_items()
            self.add_player_fields()
            return self

    @staticmethod
    def send_packet_to_player(player: Player, opcode: WorldOpCode, data: bytes):
        ensure_future(QueuesRegistry.packets_queue.put((player.name, opcode, data)))

    @staticmethod
    def broadcast(opcode: WorldOpCode, data: bytes, targets: List[Player]) -> None:
        for player in targets:
            ensure_future(QueuesRegistry.packets_queue.put((player.name, opcode, data)))
