from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Region.Weather.Constants.WeatherType import WeatherType

from Server.Connection.Connection import Connection


class Weather(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        grade = 0.99999
        response = pack(
            '<IfB',
            WeatherType.STORM.value,
            grade,
            0   # 0 - smooth change, 1 - instant change
        )
        return WorldOpCode.SMSG_WEATHER, [response]
