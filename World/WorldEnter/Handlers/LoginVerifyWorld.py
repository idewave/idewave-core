from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Exceptions.Wrappers.ProcessException import ProcessException


class LoginVerifyWorld(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        response = self._get_response()
        return WorldOpCode.SMSG_LOGIN_VERIFY_WORLD, [response]

    @ProcessException()
    def _get_response(self):
        player = self.connection.player

        return pack(
            '<I4f',
            player.map_id,            # map id
            player.x,                 # x
            player.y,                 # y
            player.z,                 # z
            player.orientation        # orientation
        )
