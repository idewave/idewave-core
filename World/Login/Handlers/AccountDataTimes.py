from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class AccountDataTimes(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        response = b'\x00' * 128
        return WorldOpCode.SMSG_ACCOUNT_DATA_TIMES, response
