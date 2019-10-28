import io

from typing import Union

from World.Chat.Builders.ChatPacketBuilder import ChatPacketBuilder
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
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

        await QueuesRegistry.text_message_queue.put((self.connection.player, response))

        return WorldOpCode.SMSG_MESSAGECHAT, [response]

    def _init_chat_packet_builder(self):
        buf = io.BytesIO(self.data)
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
    def _parse_message(buffer: io.BytesIO):
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result
