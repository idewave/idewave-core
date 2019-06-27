from Utils.Debug.Logger import Logger


class SwapItem(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet

    async def process(self):
        return None, None
