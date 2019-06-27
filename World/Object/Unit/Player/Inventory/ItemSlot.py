from World.Object.Item.model import Item


class ItemSlot(object):

    def __init__(self, slot_id: int):
        self.slot_id = slot_id
        self.item = None

    def set_item(self, item: Item):
        self.item = Item

    def is_empty(self):
        return self.item is None
