from World.Observer import BaseObserver
from Typings.Constants import REGIONS_MAP


class WorldObserver(BaseObserver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.regions: REGIONS_MAP = kwargs.pop('regions')
