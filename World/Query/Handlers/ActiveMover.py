from Server.Connection.Connection import Connection


class ActiveMover(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        # guid = int.from_bytes(self.packet[6:], 'little')
        return None, None
