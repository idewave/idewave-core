from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Utils.Debug.Logger import Logger


class ItemInfo(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        return WorldOpCode.SMSG_ITEM_QUERY_SINGLE_RESPONSE, None
