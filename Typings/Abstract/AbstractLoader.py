from abc import abstractmethod

from Typings.Abstract.AbstractBase import AbstractBase


class AbstractLoader(AbstractBase):

    @abstractmethod
    def load(self, **kwargs):
        pass
