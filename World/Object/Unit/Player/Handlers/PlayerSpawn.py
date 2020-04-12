from asyncio import ensure_future
from typing import List, Dict

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Constants.UpdateObjectFields import UnitField, PlayerField
from World.Region.model import Region
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager
from World.Region.Octree.Node import ChildNode
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Object.Unit.Player.model import PlayerSkill
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType
from World.Object.Unit.Player.Constants.CharacterClass import CharacterClass
from Server.Connection.Connection import Connection
from Server.Registry.QueuesRegistry import QueuesRegistry
from World.Object.Unit.Player.Constants.PlayerSpawnFields import PLAYER_SPAWN_FIELDS
from Typings.Abstract.AbstractHandler import AbstractHandler


class PlayerSpawn(AbstractHandler):

    __slots__ = ('data', 'connection', 'spawn_fields', 'update_flags')

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

        self.spawn_fields = PLAYER_SPAWN_FIELDS

        self.update_flags = (
            UpdateObjectFlags.UPDATEFLAG_LIVING.value |
            UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value |
            UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
            UpdateObjectFlags.UPDATEFLAG_SELF.value
        )

        self._set_player_power()

    async def process(self) -> tuple:
        with PlayerManager() as player_mgr:
            player_mgr.init_update_packet_builder(
                object_update_type=ObjectUpdateType.CREATE_OBJECT2,
                update_flags=self.update_flags,
                update_object=self.connection.player
            )

            # add fields with offset before create update packet
            skills_count = len(self.connection.player.skills)
            for skill_index in range(skills_count):
                offset = skill_index * 3
                skill: PlayerSkill = self.connection.player.skills[skill_index]

                player_mgr.add_field(
                    PlayerField.SKILL_INFO_1_ID,
                    skill.skill_template.entry,
                    offset=offset
                )
                player_mgr.add_field(
                    PlayerField.SKILL_INFO_1_LEVEL,
                    skill.skill_template.min,
                    offset=offset + 1
                )
                player_mgr.add_field(
                    PlayerField.SKILL_INFO_1_STAT_LEVEL,
                    skill.skill_template.max,
                    offset=offset + 2
                )

            batch: bytes = player_mgr.create_batch(self.spawn_fields)
            packets: List[bytes] = player_mgr\
                .add_batch(batch)\
                .build_update_packet()\
                .get_update_packets()

            # ensure_future(QueuesRegistry.broadcast_callback_queue.put((
            #     WorldOpCode.SMSG_UPDATE_OBJECT,
            #     packets,
            #     self._broadcast,
            # )))

            return WorldOpCode.SMSG_UPDATE_OBJECT, packets

    # def _broadcast(self, **kwargs) -> None:
    #     opcode: WorldOpCode = kwargs.pop('opcode')
    #     regions: Dict[int, Region] = kwargs.pop('regions')
    #
    #     player: Player = self.connection.player
    #     current_region: Region = regions.get(player.region.id)
    #     if current_region is None:
    #         return None
    #
    #     root_node: ChildNode = current_region.get_octree()
    #     OctreeNodeManager.set_object(root_node, player)
    #
    #     current_node: ChildNode = player.get_current_node()
    #     if not current_node:
    #         return None
    #
    #     # we get parent of parent because some of nearest nodes can lay in the another parent
    #     node_to_notify: ChildNode = current_node.parent_node.parent_node
    #     guids = OctreeNodeManager.get_guids(node_to_notify)
    #     guids: List[int] = [guid for guid in guids if not guid == player.guid]
    #
    #     if not guids:
    #         return None
    #
    #     targets_to_notify: List[Player] = [
    #         player
    #         for player in current_region.players
    #         if player.guid in guids
    #     ]
    #
    #     if not targets_to_notify:
    #         return None
    #
    #     target_packets: List[bytes] = PlayerSpawn.create_target_packets(targets=targets_to_notify)
    #     for packet in target_packets:
    #         PlayerManager.send_packet_to_player(player, opcode, packet)
    #
    #     player_packets: List[bytes] = PlayerSpawn.create_target_packets(targets=[player])
    #     for packet in player_packets:
    #         PlayerManager.broadcast(opcode, packet, targets_to_notify)

    @staticmethod
    def create_target_packets(targets: List[Player]) -> List[bytes]:
        update_flags = (
            UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
            UpdateObjectFlags.UPDATEFLAG_LIVING.value |
            UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value
        )

        targets = targets.copy()

        with PlayerManager() as head_player_mgr:
            head_player_mgr.init_update_packet_builder(
                object_update_type=ObjectUpdateType.CREATE_OBJECT2,
                update_flags=update_flags,
                update_object=targets.pop(0)
            )

            batch = head_player_mgr.create_batch(PLAYER_SPAWN_FIELDS)
            head_player_mgr.add_batch(batch)

            if targets:
                for target in targets:
                    with PlayerManager() as player_mgr:
                        player_mgr.init_update_packet_builder(
                            object_update_type=ObjectUpdateType.CREATE_OBJECT2,
                            update_flags=update_flags,
                            update_object=target
                        )

                        batch = player_mgr.create_batch(PLAYER_SPAWN_FIELDS)
                        head_player_mgr.add_batch(batch)

            return head_player_mgr.build_update_packet().get_update_packets()

    def _set_player_power(self) -> None:
        char_class = CharacterClass(
            self.connection.player.char_class
        )

        mana_classes = [
            CharacterClass.WARLOCK,
            CharacterClass.SHAMAN,
            CharacterClass.MAGE,
            CharacterClass.PRIEST,
            CharacterClass.DRUID,
            CharacterClass.PALADIN
        ]

        rage_classes = [
            CharacterClass.WARRIOR
        ]

        energy_classes = [
            CharacterClass.ROGUE
        ]

        if char_class in mana_classes:
            self.spawn_fields.append(UnitField.POWER_MANA)
            self.spawn_fields.append(UnitField.MAXPOWER_MANA)

        elif char_class in rage_classes:
            self.spawn_fields.append(UnitField.POWER_RAGE)
            self.spawn_fields.append(UnitField.MAXPOWER_RAGE)

        elif char_class in energy_classes:
            self.spawn_fields.append(UnitField.POWER_ENERGY)
            self.spawn_fields.append(UnitField.MAXPOWER_ENERGY)

        elif char_class == CharacterClass.HUNTER:
            self.spawn_fields.append(UnitField.POWER_MANA)
            self.spawn_fields.append(UnitField.MAXPOWER_MANA)
            self.spawn_fields.append(UnitField.POWER_FOCUS)
            self.spawn_fields.append(UnitField.MAXPOWER_FOCUS)
