from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Region.Constants.WeatherType import WeatherType


class Weather(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self):
        grade = 0.99999
        response = pack(
            '<IfB',
            WeatherType.STORM.value,
            grade,
            0   # 0 - smooth change, 1 - instant change
        )
        return WorldOpCode.SMSG_WEATHER, response
