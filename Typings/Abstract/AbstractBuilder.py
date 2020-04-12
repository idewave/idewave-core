from abc import abstractmethod

from Typings.Abstract.AbstractBase import AbstractBase


class AbstractBuilder(AbstractBase):

    @abstractmethod
    def build(self, **kwargs):
        pass
