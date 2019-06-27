from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class TutorialFlags(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        return WorldOpCode.SMSG_TUTORIAL_FLAGS, self._get_tutorial_flags()

    def _get_tutorial_flags(self):
        return b"\xff" * 32
