from Server.Connection.Connection import Connection


class PlayerTarget(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        guid = int.from_bytes(self.data, 'little')
        if guid == 0:
            guid = None

        self.connection.player.target = guid

        return None, None
