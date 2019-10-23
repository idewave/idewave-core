from struct import pack

from World.Object.Unit.Player.PlayerManager import PlayerManager

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class Logout(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):

        with PlayerManager(connection=self.connection) as player_mgr:
            player_mgr.set(self.connection.player).save()

        response = pack(
            '<IB',
            0,
            0
        )
        return WorldOpCode.SMSG_LOGOUT_RESPONSE, [response]
