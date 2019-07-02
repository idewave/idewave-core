from struct import pack

from World.Object.Unit.Player.PlayerManager import PlayerManager

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class Logout(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Logout]: temp_ref is not exists')

    async def process(self):

        with PlayerManager() as player_mgr:
            player_mgr.set(self.temp_ref.player).save()

        response = pack(
            '<IB',
            0,
            0
        )
        return WorldOpCode.SMSG_LOGOUT_RESPONSE, response
