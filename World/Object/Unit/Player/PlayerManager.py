from asyncio import ensure_future
from typing import List

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Unit.UnitManager import UnitManager
from World.Object.Unit.Player.Stats.Builders.PlayerStatsBuilder import PlayerStatsBuilder
from World.Object.Unit.Player.model import Player
from World.Object.Constants.UpdateObjectFields import UnitField, PlayerField
from World.Object.Unit.Player.Skill.SkillManager import SkillManager
from World.Object.Unit.Spell.SpellManager import SpellManager
from World.Object.Unit.Player.Inventory.Equipment.model import Equipment
from World.Object.Unit.Player.Inventory.Equipment.EquipmentManager import EquipmentManager

from World.Object.Unit.Player.Constants.CharacterRace import CharacterRace
from World.Object.Unit.Player.Constants.CharacterGender import CharacterGender
from World.Object.Unit.Player.Constants.CharacterEquipSlot import CharacterEquipSlot
from World.Object.Unit.Player.Constants.CharacterDisplayId import CHARACTER_DISPLAY_ID
from World.Object.Unit.Player.Constants.PowerTypeToCharClass import POWER_TYPE
from World.Region.model import DefaultLocation

from Server.Registry.QueuesRegistry import QueuesRegistry


class PlayerManager(UnitManager):

    __slots__ = ('world_object', 'equipment')

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
        player = self.player
        stats = self.stats

        self.set_object_field(PlayerField.FLAGS, 0)

        bytes0 = (
            player.race                             |
            player.char_class << 8                  |
            player.gender << 16                     |
            POWER_TYPE[player.char_class] << 24
        )

        bytes_1 = (
            player.skin                             |
            player.face << 8                        |
            player.hair_style << 16                 |
            player.hair_color << 24
        )

        bytes_2 = (
            player.facial_hair                      |
            # TODO: debug values below
            0x00 << 8                               |
            0x00 << 16                              |
            0x02 << 24
        )

        bytes_3 = player.gender

        self.set_object_field(UnitField.BYTES_0, bytes0)
        self.set_object_field(PlayerField.BYTES_1, bytes_1)
        self.set_object_field(PlayerField.BYTES_2, bytes_2)
        self.set_object_field(PlayerField.BYTES_3, bytes_3)

        self.set_object_field(PlayerField.XP, stats.xp)
        self.set_object_field(PlayerField.NEXT_LEVEL_XP, stats.next_level_xp)

        self.set_object_field(PlayerField.CHARACTER_POINTS1, stats.free_talent_points)
        self.set_object_field(PlayerField.CHARACTER_POINTS2, stats.free_primary_professions_points)

        self.set_object_field(PlayerField.BLOCK_PERCENTAGE, stats.block)
        self.set_object_field(PlayerField.DODGE_PERCENTAGE, stats.dodge)
        self.set_object_field(PlayerField.PARRY_PERCENTAGE, stats.parry)
        self.set_object_field(PlayerField.CRIT_PERCENTAGE, stats.melee_crit)
        # TODO: calculate ranged crit
        self.set_object_field(PlayerField.RANGED_CRIT_PERCENTAGE, stats.ranged_crit)

        self.set_object_field(PlayerField.REST_STATE_EXPERIENCE, stats.rest_state_exp)
        self.set_object_field(PlayerField.COINAGE, PlayerManager.from_config('player:default:start_money'))

        # TODO: set to actual
        self.set_object_field(PlayerField.WATCHED_FACTION_INDEX, -1)
        self.set_object_field(PlayerField.BYTES, 0)
        self.set_object_field(PlayerField.MAX_LEVEL, PlayerManager.from_config('player:default:max_level'))

        # equipment
        for slot in range(CharacterEquipSlot.HEAD.value, CharacterEquipSlot.BAG1.value):
            item = self.equipment[CharacterEquipSlot(slot)].item

            if item is not None:
                # TODO: fix magic numbers
                # set VISIBLE_ITEM_1_0 + offset
                visible_item_index = PlayerField.VISIBLE_ITEM_1_0.value + (slot * 16)
                self.set_object_field(PlayerField(visible_item_index), item.item_template.entry)
                # set INV_SLOT_HEAD + offset
                inv_slot_index = PlayerField.INV_SLOT_HEAD.value + (slot * 2)
                self.set_object_field(PlayerField(inv_slot_index), item.guid)

                self.set_object_field(PlayerField.MOD_DAMAGE_NORMAL_DONE_PCT, 1)

    def _set_display_id(self):
        player = self.player
        race = CharacterRace(player.race)
        gender = CharacterGender(player.gender)
        display_id = CHARACTER_DISPLAY_ID[race][gender]
        player.display_id = player.native_display_id = display_id

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
        player = self.player
        location: DefaultLocation = self.session.query(DefaultLocation).filter_by(race=player.race).first()

        player.x = location.x
        player.y = location.y
        player.z = location.z
        player.orientation = float(0)

        player.region = location.region
        player.map_id = location.map_id

    def _set_faction_template_id(self):
        player = self.player
        race = CharacterRace(player.race)
        player.faction_template = CHARACTER_DISPLAY_ID[race]['faction_template']

    def _init_stats(self) -> None:
        self.stats = PlayerStatsBuilder(world_object=self.player).build().get_stats()

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

        self.player.level = PlayerManager.from_config('player:default:min_level')

        self.player.account = self.session.merge(kwargs.pop('account'))

        self._set_start_location()
        self._set_display_id()
        self._set_faction_template_id()

        # save player for id generating
        self.session.add(self.player)
        self.session.flush()

        # self.stats_builder = StatsBuilder(self.player)

        # self.set_stats()
        self._set_stats()

        self.save()

        self.set_default_equipment()
        self.set_default_skills()
        self.set_default_spells()

        return self

    def prepare(self):
        super(PlayerManager, self).prepare()
        player = self.player

        with EquipmentManager() as equipment_mgr:
            self.equipment = equipment_mgr.get_equipment(player=player).get_items()
            self.add_player_fields()
            return self

    @staticmethod
    def send_packet_to_player(player: Player, opcode: WorldOpCode, data: bytes):
        ensure_future(QueuesRegistry.packets_queue.put((player.name, opcode, data)))

    @staticmethod
    def broadcast(opcode: WorldOpCode, data: bytes, targets: List[Player]) -> None:
        for player in targets:
            ensure_future(QueuesRegistry.packets_queue.put((player.name, opcode, data)))
