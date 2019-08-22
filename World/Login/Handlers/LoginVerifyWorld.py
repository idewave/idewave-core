from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Utils.Debug.Logger import Logger


class LoginVerifyWorld(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self):
        response = self._get_verify_login_packet()
        return WorldOpCode.SMSG_LOGIN_VERIFY_WORLD, response

    def _get_verify_login_packet(self):
        player = self.temp_ref.player

        if not player:
            Logger.error('[Login Verify]: player not exists')
            return None

        return pack(
            '<I4f',
            player.map_id,            # map id
            player.x,                 # x
            player.y,                 # y
            player.z,                 # z
            player.orientation        # orientation
        )
