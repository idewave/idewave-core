class ActiveMover(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        # guid = int.from_bytes(self.packet[6:], 'little')
        return None, None
