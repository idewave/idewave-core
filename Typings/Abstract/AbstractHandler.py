from abc import abstractmethod

from Typings.Abstract.AbstractBase import AbstractBase


class AbstractHandler(AbstractBase):

    @abstractmethod
    async def process(self):
        pass
