from struct import pack
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode

from Config.Run.config import Config


class MOTD(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        motd_msg = Config.Realm.General.motd
        motd_msg_bytes = motd_msg.encode('utf-8') + b'\x00'

        response = pack(
            '<I{msg_len}s'.format(msg_len=len(motd_msg_bytes)),
            1,
            motd_msg_bytes
        )

        return WorldOpCode.SMSG_MOTD, response
