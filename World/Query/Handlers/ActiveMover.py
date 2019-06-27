from Utils.Debug.Logger import Logger


class ActiveMover(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        guid = int.from_bytes(self.packet[6:], 'little')
        Logger.error('[Active Mover]: guid = {}'.format(guid))
        return None, None
