from typing import Dict, Any
from abc import ABC, abstractmethod


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, event_type: int, payload: Dict[str, Any]):
        pass
