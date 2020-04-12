from World.Observer import BaseObserver
from Typings.Constants import REGIONS_MAP


class WorldObserver(BaseObserver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.region_octree_map: REGIONS_MAP = kwargs.pop('regions')
