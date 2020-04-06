from World.Observer import BaseObserver
from World.Region.model import Region


class RegionObserver(BaseObserver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.regions: Region = kwargs.pop('region')
