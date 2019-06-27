from Utils.Debug.Logger import Logger


class TextEmote(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):

        # response = pack(
        #     '<Q3IB',
        #     session.player.guid,
        #     0,
        #     int.from_bytes(self.packet[6:7], 'little'),
        #     0,
        #     0
        # )
        # response = pack(
        #     '<IQ',
        #     int.from_bytes(self.packet[6:7], 'little'),
        #     session.player.guid
        # )

        #Logger.test(response)
        #return WorldOpCode.SMSG_TEXT_EMOTE.value, response
        return None, None
        #return WorldOpCode.SMSG_EMOTE.value, response
