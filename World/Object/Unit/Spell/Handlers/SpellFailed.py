from World.Object.Unit.Spell.Constants.SpellCastResult import SpellCastResult
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class SpellFailed(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        pass
