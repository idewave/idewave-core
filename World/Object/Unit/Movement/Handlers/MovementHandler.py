from io import BytesIO
from asyncio import ensure_future
from struct import unpack
from typing import List, Dict

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Unit.Movement.Constants.MovementFlags import MovementFlags
from World.Object.Position import Position
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.model import Region
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager
from World.Region.Octree.Node import ChildNode
from Server.Registry.QueuesRegistry import QueuesRegistry
from Typings.Abstract import AbstractHandler
from Server.Connection.Connection import Connection


class MovementHandler(AbstractHandler):

    def __init__(self, **kwargs):
        self.opcode: WorldOpCode = kwargs.pop('opcode')
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

        self.movement_flags: int = MovementFlags.NONE.value
        self.movement_flags2 = 0
        self.time = 0
        self.position: Position = Position()
        self.transport_guid = 0
        self.transport_position = Position()
        self.transport_time = 0
        self.swim_pitch = float(0)
        self.fall_time = 0
        self.jump_velocity = float(0)
        self.jump_sin_angle = float(0)
        self.jump_cos_angle = float(0)
        self.jump_x_y_speed = float(0)

    async def process(self) -> tuple:
        self._parse_packet()

        if self._is_movement_valid():
            player: Player = self.connection.player
            player.position = self.position

            # ensure_future(QueuesRegistry.broadcast_callback_queue.put((
            #     self.opcode,
            #     [self.data],
            #     self._broadcast,
            # )))

        return None, None

    # def _broadcast(self, **kwargs) -> None:
    #     opcode: WorldOpCode = kwargs.pop('opcode')
    #     packets: List[bytes] = kwargs.pop('packets')
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
    #     for packet in packets:
    #         PlayerManager.broadcast(opcode, player.packed_guid + packet, targets_to_notify)

    def _is_movement_valid(self):
        return True

    def _parse_packet(self):
        buf = BytesIO(self.data)

        self.movement_flags = MovementHandler._set_movement_flags(buf.read(4))
        self.movement_flags2 = int.from_bytes(buf.read(1), 'little')

        self.time = buf.read(4)

        self.position.x = unpack('<f', buf.read(4))[0]
        self.position.y = unpack('<f', buf.read(4))[0]
        self.position.z = unpack('<f', buf.read(4))[0]
        self.position.orientation = unpack('<f', buf.read(4))[0]

        if self.movement_flags & MovementFlags.ONTRANSPORT.value:
            self.transport_guid = buf.read(8)
            self.transport_position.x = unpack('<f', buf.read(4))[0]
            self.transport_position.y = unpack('<f', buf.read(4))[0]
            self.transport_position.z = unpack('<f', buf.read(4))[0]
            self.transport_time = buf.read(4)

        if self.movement_flags & MovementFlags.SWIMMING.value:
            self.swim_pitch = unpack('<f', buf.read(4))[0]

        if self.movement_flags & MovementFlags.FALLING.value:
            self.jump_velocity = unpack('<f', buf.read(4))[0]
            self.jump_sin_angle = unpack('<f', buf.read(4))[0]
            self.jump_cos_angle = unpack('<f', buf.read(4))[0]
            self.jump_x_y_speed = unpack('<f', buf.read(4))[0]

        self.fall_time = unpack('<f', buf.read(4))[0]

    @staticmethod
    def _set_movement_flags(value):
        data = int.from_bytes(value, 'little')
        if MovementFlags.has_value(data):
            return MovementFlags(data).value
        else:
            return MovementFlags.NONE.value
