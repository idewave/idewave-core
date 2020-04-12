import yaml
from os import path

from Typings.Abstract import AbstractLoader
from Utils.Debug import Logger


class ConfigLoader(AbstractLoader):

    def load(self, **kwargs):
        current_dir = path.dirname(__file__)
        config_list = [
            'database',
            'object',
            'player',
            'realm',
            'region',
            'server',
            'unit',
            'world'
        ]

        main_config = {}

        for config in config_list:
            with open(path.join(current_dir, f'{config}.yml'), 'r') as stream:
                try:
                    data = yaml.load(stream, Loader=yaml.Loader)
                    main_config[config] = data
                except yaml.YAMLError as e:
                    Logger.error(f'[ConfigLoader]: error while parsing yml configs: {e}')
                    raise Exception(f'[ConfigLoader]: {e}')

        return main_config
