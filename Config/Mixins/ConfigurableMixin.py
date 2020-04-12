from typing import Any

from Config.Init.configs import main_config


class ConfigurableMixin(object):

    MIN_KEYS_AMOUNT = 3

    @classmethod
    def from_config(cls, composite_key: str) -> Any:
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

        config = main_config[config_name]

        for key in transition_keys:
            config = config[key]

        return config[destination_key]
