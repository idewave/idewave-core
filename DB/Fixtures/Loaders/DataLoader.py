from os import walk, path

from Typings.Abstract.AbstractLoader import AbstractLoader
from Utils.Debug import Logger


class DataLoader(AbstractLoader):

    def load(self, **kwargs):
        db_name: str = kwargs.pop('db_name')
        db_name = DataLoader.from_config(f'database:names:{db_name}')
