from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class TutorialFlags(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        response = TutorialFlags._get_tutorial_flags()
        return WorldOpCode.SMSG_TUTORIAL_FLAGS, [response]

    @staticmethod
    def _get_tutorial_flags():
        return b"\xff" * 32
