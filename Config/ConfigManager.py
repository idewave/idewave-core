import yaml
import json

from os import path
from collections import namedtuple

from Utils.Debug import Logger


class ConfigManager(object):

    def __init__(self):
        self.config = None

    def load(self):
        current_dir = path.dirname(__file__)
        main_config = 'Config.yml'

        with open(path.join(current_dir, main_config), 'r') as stream:
            try:
                data = yaml.load(stream, Loader=yaml.Loader)
                self.config = json.loads(
                    json.dumps(data), object_hook=lambda d: namedtuple('Configs', d.keys())(*d.values())
                )
            except yaml.YAMLError as error:
                Logger.error('[Config Manager]: {}'.format(error))
            else:
                return self
