from typing import List, Any, Dict

from Typings.Abstract.AbstractObserver import AbstractObserver


class ObservableMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriptions: List[AbstractObserver] = []

    def subscribe(self, observer: AbstractObserver) -> None:
        self.subscriptions.append(observer)

    def detach(self):
        pass

    def notify(self, event_type: int, payload: Dict[str, Any]) -> None:
        for observer in self.subscriptions:
            observer.update(event_type, payload)
