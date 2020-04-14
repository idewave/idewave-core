from typing import Any

from Cache.Registry.CacheRegistry import CacheRegistry


class CacheableMixin(object):

    @classmethod
    def is_cached(cls, storage_key: str, key: str) -> bool:
        cache = CacheRegistry
        return storage_key in cache.__dict__ and key in cache.__dict__[storage_key]

    @classmethod
    def to_cache(cls, storage_key: str, key: str, value: Any) -> None:
        cache = CacheRegistry
        if storage_key in cache.__dict__:
            cache.__dict__[storage_key][key] = value

    @classmethod
    def from_cache(cls, storage_key: str, key: str) -> Any:
        cache = CacheRegistry
        if storage_key in cache.__dict__:
            return cache.__dict__[key]
