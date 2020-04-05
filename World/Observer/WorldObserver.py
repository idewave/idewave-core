from typing import List, Dict, Any


class WorldObserver(object):

    def __init__(self, **kwargs):
        self.handlers_map: Dict[int, List[Any]] = kwargs.pop('handlers_map')
        self.subscribers: List[Any] = []

    def update(self, event_type: int, payload: Dict[str, Any]) -> None:
        handlers = self.handlers_map[event_type]
        for handler in handlers:
            handler(self.subscribers, payload)
