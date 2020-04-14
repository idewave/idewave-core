from Typings.Abstract.AbstractRegistry import AbstractRegistry
from Cache.Constants.CacheKeys import MAIN_CONFIG


class CacheRegistry(AbstractRegistry):
    keys = (
        MAIN_CONFIG,
    )
