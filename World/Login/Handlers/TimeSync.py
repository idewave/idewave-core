from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Utils.Debug.Logger import Logger


class TimeSync(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        # TODO: correctly evaluate value
        return WorldOpCode.SMSG_TIME_SYNC_REQ, b'\x00\x00\x00\x00'
