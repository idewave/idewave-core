from typing import Dict, Any
from abc import abstractmethod

from Typings.Abstract.AbstractBase import AbstractBase


class AbstractObserver(AbstractBase):

    @abstractmethod
    def update(self, event_type: int, payload: Dict[str, Any]):
        pass
