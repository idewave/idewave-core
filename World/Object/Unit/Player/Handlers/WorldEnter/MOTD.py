from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection
from Typings.Abstract import AbstractHandler
from Config.Mixins import ConfigurableMixin


class MOTD(AbstractHandler, ConfigurableMixin):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        motd_msg = MOTD.from_config('realm:settings:motd')
        motd_msg_bytes = motd_msg.encode('utf-8') + b'\x00'

        response = pack(
            '<I{msg_len}s'.format(msg_len=len(motd_msg_bytes)),
            1,
            motd_msg_bytes
        )

        return WorldOpCode.SMSG_MOTD, [response]
