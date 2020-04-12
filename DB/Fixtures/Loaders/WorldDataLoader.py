import subprocess
from os import walk, path

from Typings.Abstract import AbstractLoader
from Config.Mixins import ConfigurableMixin


class WorldDataLoader(AbstractLoader, ConfigurableMixin):

    def load(self, **kwargs):
        pass
