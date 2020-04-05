from abc import ABC, abstractmethod


class AbstractHandler(ABC):

    @abstractmethod
    async def process(self):
        pass
