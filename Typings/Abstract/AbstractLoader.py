from abc import ABC, abstractmethod


class AbstractLoader(ABC):

    @abstractmethod
    def load(self, **kwargs):
        pass
