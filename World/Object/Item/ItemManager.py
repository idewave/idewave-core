from World.Object.ObjectManager import ObjectManager
from World.Object.Item.model import Item
from World.Object.Constants.UpdateObjectFields import ItemField
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from World.Object.Item.model import ItemTemplate
from Utils.Debug.Logger import Logger


class ItemManager(ObjectManager):

    def __init__(self):
        super(ItemManager, self).__init__()
        self.world_object = Item()

    def get_item(self, guid):
        return self.world_object

    def create(self, **kwargs):
        display_id = kwargs.pop('display_id')
        item_type = kwargs.pop('item_type')
        entry = kwargs.pop('entry')

        self.world_object.display_id = display_id
        self.world_object.item_type = item_type
        self.world_object.entry = entry

        item_template = self.session\
            .query(ItemTemplate)\
            .filter_by(display_id=display_id, item_type=item_type, entry=entry)\
            .first()

        self.world_object.item_template = item_template

        return self

    def prepare(self, **kwargs):
        super(ItemManager, self).prepare()
        # actually item has no movement data but according to UpdatePacket structure this data should be set
        self._init_movement_data()
        self.add_item_fields()

        return self

    def add_item_fields(self):
        #self.set(ItemField.OWNER, self.world_object.owner.guid)
        self.set_object_field(ItemField.CONTAINED, self.world_object.guid)
        self.set_object_field(ItemField.STACK_COUNT, self.world_object.stack_count)
        #self.set(ItemField.DURABILITY, self.world_object.durability)
        self.set_object_field(ItemField.MAXDURABILITY, self.world_object.max_durability)
        self.set_object_field(ItemField.DURATION, self.world_object.duration)

    def _init_movement_data(self):
        self.world_object.movement.set_object_type(self.world_object.object_type)

        flags = (
                UpdateObjectFlags.UPDATEFLAG_LOWGUID.value |
                UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value
        )

        self.world_object.movement.set_update_flags(update_flags=flags)
        self.world_object.movement.set_guids(self.world_object.id, self.world_object.high_guid)

    # inheritable
    def load(self, id: int):
        self.world_object = self.session.query(Item).filter_by(id=id).first()
        return self

    # inheritable
    def new(self):
        self.add_object_fields()
        self.init_movement()
        return self
