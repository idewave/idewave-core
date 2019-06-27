import time
from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode

from Config.Run.config import Config


class GameSpeed(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        data = pack(
            '<2f',
            self._secs_to_time_bit_fields(),        # game time (secs) to bit
            Config.World.Gameplay.game_speed        # game speed
        )
        return WorldOpCode.SMSG_LOGIN_SETTIMESPEED, data

    def _secs_to_time_bit_fields(self):
        local = time.localtime()
        return ((local.tm_year - 100) << 24 |
                local.tm_mon << 20 |
                (local.tm_mday -1) << 14 |
                local.tm_wday << 11 |
                (local.tm_hour-3) << 6 |
                local.tm_min)
