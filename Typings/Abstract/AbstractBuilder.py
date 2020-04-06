from abc import ABC, abstractmethod


class AbstractBuilder(ABC):

    @abstractmethod
    def build(self, **kwargs):
        pass
