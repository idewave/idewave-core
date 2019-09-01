import io

from World.Chat.Builders.ChatPacketBuilder import ChatPacketBuilder
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Registry.QueuesRegistry import QueuesRegistry


class MessageHandler(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Initial Spells]: temp_ref does not exists')

        self.player = self.temp_ref.player

        self.chat_packet_builder: ChatPacketBuilder = None

    async def process(self):
        self._init_chat_packet_builder()
        response = self.chat_packet_builder.build().get_response()

        await QueuesRegistry.text_message_queue.put((self.player, response))

        return WorldOpCode.SMSG_MESSAGECHAT, response

    def _init_chat_packet_builder(self):
        buf = io.BytesIO(self.packet[6:])
        message_type = int.from_bytes(buf.read(4), 'little')
        message_language = int.from_bytes(buf.read(4), 'little')
        message_bytes = self._parse_message(buf)

        self.chat_packet_builder = ChatPacketBuilder(
            message_type=message_type,
            message_language=message_language,
            message_bytes=message_bytes,
            sender_guid=self.player.guid
        )

    def _parse_message(self, buffer: io.BytesIO):
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result
