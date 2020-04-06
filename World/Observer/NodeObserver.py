from World.Observer import BaseObserver
from Typings.Constants import ANY_NODE


class NodeObserver(BaseObserver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node: ANY_NODE = kwargs.pop('node')
