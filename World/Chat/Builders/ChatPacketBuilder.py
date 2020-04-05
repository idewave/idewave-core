from struct import pack

from World.Chat.Constants.ChatMsgType import ChatMsgType
from World.Chat.Constants.ChatTag import ChatTag

from Utils.Debug import Logger


class ChatPacketBuilder(object):

    def __init__(self, **kwargs):
        self.message_type = kwargs.pop('message_type')
        self.message_language = kwargs.pop('message_language')
        self.message_bytes = kwargs.pop('message_bytes')

        self.sender_guid = kwargs.pop('sender_guid')

        self.response = None

    def build(self):
        data = bytes()

        data += pack(
            '<BIQI',
            self.message_type,
            self.message_language,
            self.sender_guid,
            0
        )

        if ChatMsgType(self.message_type) == ChatMsgType.CHANNEL:
            # add channel name
            pass

        # FIXME: target guid
        data += pack('<Q', 0)

        data += pack('<I', len(self.message_bytes) + 1)
        data += self.message_bytes

        # FIXME: set actual chat tag
        data += pack('<2B', ChatTag.NONE.value, 0)

        self.response = data

        return self

    def get_response(self):
        return self.response
