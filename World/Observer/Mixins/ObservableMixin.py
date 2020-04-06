from typing import List, Any, Dict

from World.Observer import WorldObserver


class ObservableMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriptions: List[WorldObserver] = []

    def subscribe(self, observer: WorldObserver) -> None:
        self.subscriptions.append(observer)

    def detach(self):
        pass

    def notify(self, event_type: int, payload: Dict[str, Any]) -> None:
        for observer in self.subscriptions:
            observer.update(event_type, payload)
