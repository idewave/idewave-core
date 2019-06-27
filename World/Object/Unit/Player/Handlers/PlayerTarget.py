class PlayerTarget(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self):
        guid = int.from_bytes(self.packet[6:], 'little')
        if guid == 0:
            guid = None

        self.temp_ref.player.target = guid
        return None, None
