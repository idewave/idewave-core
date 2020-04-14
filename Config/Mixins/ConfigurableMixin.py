from typing import Any

from Init.Registry.InitRegistry import InitRegistry
from Cache.Mixins.CacheableMixin import CacheableMixin
from Cache.Constants.CacheKeys import MAIN_CONFIG


class ConfigurableMixin(CacheableMixin):

    MIN_KEYS_AMOUNT = 3

    @classmethod
    def from_config(cls, composite_key: str) -> Any:
        cached = cls.from_cache(MAIN_CONFIG, composite_key)
        if cached:
            return cached

        delimiter = ':'

        if delimiter not in composite_key:
            raise Exception(
                f'{composite_key} is incorrect format of key, '
                f'keys should be separated by {delimiter}.'
            )

        keys = composite_key.split(delimiter)

        if len(keys) < ConfigurableMixin.MIN_KEYS_AMOUNT:
            raise Exception(f'Minimal valid format is "config_name:top_key:destination_key"')

        config_name = keys[0]
        transition_keys = keys[1:-1]
        destination_key = keys[-1]

        try:
            config = InitRegistry.main_config[config_name]
        except TypeError:
            raise TypeError('You need to call InitLoader.load(), because main_config is not loaded')

        for key in transition_keys:
            config = config[key]

        value = config[destination_key]
        cls.to_cache(MAIN_CONFIG, composite_key, value)

        return value
