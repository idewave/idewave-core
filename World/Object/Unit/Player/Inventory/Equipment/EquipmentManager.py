from struct import pack

from World.Character.Constants.CharacterEquipSlot import CharacterEquipSlot
from World.Object.ObjectManager import ObjectManager
from World.Object.Unit.Player.Inventory.Equipment.model import Equipment, DefaultEquipment
from World.Object.Unit.Player.Inventory.ItemSlot import ItemSlot
from World.Object.Unit.Player.Inventory.Equipment.Constants.InventoryTypeItemSlotMap import INVENTORY_TYPE_ITEM_SLOT_MAP
from World.Object.Unit.Player.Inventory.Equipment.Constants.InventoryType import InventoryType
from World.Object.Item.model import Item
from World.Object.Unit.Player.model import Player


class EquipmentManager(ObjectManager):

    def __init__(self, **kwargs):
        super(EquipmentManager, self).__init__(**kwargs)
        self.slots = {}
        self._init_slots()
        self.world_object = Equipment()

    def get_equipment(self, player: Player):
        equipment = player.equipment
        items = [e.item for e in equipment]

        for item in items:
            inventory_type_id = InventoryType(item.item_template.item_type)

            available_slots = INVENTORY_TYPE_ITEM_SLOT_MAP[inventory_type_id]

            if len(available_slots) > 0:
                empty_slot = next((slot for slot in available_slots if self.slots[slot].is_empty()), None)
                if empty_slot is None:
                    self.slots[available_slots[0]].item = item
                else:
                    self.slots[empty_slot].item = item

        return self

    def get_items(self):
        return self.slots

    def get_item(self, slot: CharacterEquipSlot):
        return self.slots[slot]

    # this method using for Characters screen
    def to_bytes(self):
        result = bytes()

        for slot_id in range(CharacterEquipSlot.HEAD.value, CharacterEquipSlot.BAG1.value + 1):
            slot = self.slots[CharacterEquipSlot(slot_id)]

            if slot.is_empty():
                item_bytes = pack('<IBI', 0, 0, 0)
            else:
                item_bytes = pack(
                    '<IBI',
                    slot.item.item_template.display_id,
                    slot.item.item_template.item_type,
                    0,                                      # item.enchant_id
                )

            result += item_bytes

        return result

    def set_default_equipment(self, player: Player):
        default_equipment = self.session\
            .query(DefaultEquipment).filter_by(race=player.race, char_class=player.char_class).all()

        items = []

        for default_item in default_equipment:
            item = Item()
            item.item_template = default_item.item_template

            inventory_type_id = InventoryType(item.item_template.item_type)

            available_slots = INVENTORY_TYPE_ITEM_SLOT_MAP[inventory_type_id]

            if len(available_slots) > 0:
                empty_slot = next((slot for slot in available_slots if self.slots[slot].is_empty()), None)
                slot_id = available_slots[0].value
                if empty_slot is None:
                    # set item to the first not empty slot
                    # in case if multiple items with same inventoty_type was passed (for example, by mistake)
                    self.slots[available_slots[0]].item = item
                else:
                    self.slots[empty_slot].item = item
                    slot_id = empty_slot.value

                equipment = Equipment()
                equipment.item = item
                equipment.player = self.session.merge(player)
                equipment.slot_id = slot_id
                items.append(equipment)

        self.session.add_all(items)
        self.session.commit()
        return self

    def _init_slots(self):
        for slot_id in range(CharacterEquipSlot.HEAD.value, CharacterEquipSlot.BAG4.value + 1):
            self.slots[CharacterEquipSlot(slot_id)] = ItemSlot(slot_id)
