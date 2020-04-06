from typing import List, Dict, Any, Callable

from Typings.Abstract import AbstractObserver
from World.Observer.Mixins.ObservableMixin import ObservableMixin


class BaseObserver(AbstractObserver):

    def __init__(self, **kwargs):
        self.handlers_map: Dict[int, List[Callable]] = kwargs.pop('handlers_map')
        self.subscribers: List[ObservableMixin] = []

    def update(self, event_type: int, payload: Dict[str, Any]) -> None:
        handlers = self.handlers_map[event_type]
        for handler in handlers:
            handler(self.subscribers, **payload).process()
