from asyncio import ensure_future
from struct import pack
from typing import List, Dict

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.model import Region
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager
from World.Region.Octree.Node import ChildNode
from Server.Connection.Connection import Connection
from Server.Registry.QueuesRegistry import QueuesRegistry
from Typings.Abstract.AbstractHandler import AbstractHandler


class NameQuery(AbstractHandler):

    __slots__ = ('data', 'connection')

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        guid = int.from_bytes(self.data[:8], 'little')

        player = self.connection.player

        name_bytes = player.name.encode('utf-8') + b'\x00'
        response = pack(
            '<Q{name_len}sB3IB'.format(name_len=len(name_bytes)),
            player.guid,
            name_bytes,
            0,
            player.race,
            player.gender,
            player.char_class,
            0
        )

        ensure_future(QueuesRegistry.broadcast_callback_queue.put((
            WorldOpCode.SMSG_NAME_QUERY_RESPONSE,
            [response],
            self._broadcast,
        )))

        return WorldOpCode.SMSG_NAME_QUERY_RESPONSE, [response]

    def _broadcast(self, **kwargs) -> None:
        opcode: WorldOpCode = kwargs.pop('opcode')
        packets: List[bytes] = kwargs.pop('packets')
        regions: Dict[int, Region] = kwargs.pop('regions')

        player: Player = self.connection.player
        current_region: Region = regions.get(player.region.id)
        if current_region is None:
            return None

        current_node: ChildNode = player.get_current_node()
        if not current_node:
            return None

        # we get parent of parent because some of nearest nodes can lay in the another parent
        node_to_notify: ChildNode = current_node.parent_node.parent_node
        guids = OctreeNodeManager.get_guids(node_to_notify)
        guids: List[int] = [guid for guid in guids if not guid == player.guid]

        if not guids:
            return None

        targets_to_notify: List[Player] = [
            player
            for player in current_region.players
            if player.guid in guids
        ]

        if not targets_to_notify:
            return None

        for packet in packets:
            PlayerManager.broadcast(opcode, packet, targets_to_notify)
