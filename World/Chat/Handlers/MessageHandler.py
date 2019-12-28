from asyncio import ensure_future
from io import BytesIO
from typing import Union, List, Dict

from World.Chat.Builders.ChatPacketBuilder import ChatPacketBuilder
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Region.model import Region
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager
from World.Region.Octree.OctreeNode import OctreeNode
from Server.Registry.QueuesRegistry import QueuesRegistry

from Server.Connection.Connection import Connection


class MessageHandler(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

        self.chat_packet_builder: Union[ChatPacketBuilder, None] = None

    async def process(self) -> tuple:
        self._init_chat_packet_builder()
        response = self.chat_packet_builder.build().get_response()

        ensure_future(QueuesRegistry.broadcast_callback_queue.put((
            WorldOpCode.SMSG_MESSAGECHAT,
            [response],
            self._broadcast,
        )))

        return WorldOpCode.SMSG_MESSAGECHAT, [response]

    def _broadcast(self, **kwargs) -> None:
        opcode: WorldOpCode = kwargs.pop('opcode')
        packets: List[bytes] = kwargs.pop('packets')
        regions: Dict[int, Region] = kwargs.pop('regions')

        player: Player = self.connection.player
        current_region: Region = regions.get(player.region.id)
        if current_region is None:
            return None

        current_node: OctreeNode = player.get_current_node()
        if not current_node:
            return None

        # we get parent of parent because some of nearest nodes can lay in the another parent
        node_to_notify: OctreeNode = current_node.parent_node.parent_node
        guids = OctreeNodeManager.get_guids(node_to_notify)
        guids = [guid for guid in guids if not guid == player.guid]

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

    def _init_chat_packet_builder(self):
        buf = BytesIO(self.data)
        message_type = int.from_bytes(buf.read(4), 'little')
        message_language = int.from_bytes(buf.read(4), 'little')
        message_bytes = MessageHandler._parse_message(buf)

        self.chat_packet_builder = ChatPacketBuilder(
            message_type=message_type,
            message_language=message_language,
            message_bytes=message_bytes,
            sender_guid=self.connection.player.guid
        )

    # TODO: refactor Utils/AccountNameParser
    @staticmethod
    def _parse_message(buffer: BytesIO):
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result
