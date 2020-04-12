from typing import List

from World.Object.model import Object
from Typings.Abstract.AbstractHandler import AbstractHandler


class ChangeWeather(AbstractHandler):

    def __init__(self, **kwargs):
        self.subscribers: List[Object] = kwargs.pop('subscribers')

    async def process(self):
        pass
