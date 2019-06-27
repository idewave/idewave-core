from struct import pack
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
# from Login.SessionStorage import session


class LoginVerifyWorld(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self):
        response = self._get_verify_login_packet()
        return WorldOpCode.SMSG_LOGIN_VERIFY_WORLD, response

    def _get_verify_login_packet(self):
        player = self.temp_ref.player
        return pack(
            '<I4f',
            player.map_id,            # map id
            player.x,                 # x
            player.y,                 # y
            player.z,                 # z
            player.orientation        # orientation
        )
