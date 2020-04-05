from World.Object.Unit.Player.Constants.CharacterEquipSlot import CharacterEquipSlot
from World.Object.Unit.Player.Inventory.Equipment.Constants.InventoryType import InventoryType


INVENTORY_TYPE_ITEM_SLOT_MAP = {
    InventoryType.NOT_EQUIPABLE: [],
    InventoryType.HEAD: [CharacterEquipSlot.HEAD],
    InventoryType.NECK: [CharacterEquipSlot.NECK],
    InventoryType.SHOULDERS: [CharacterEquipSlot.SHOULDERS],
    InventoryType.BODY: [CharacterEquipSlot.BODY],
    InventoryType.CHEST: [CharacterEquipSlot.CHEST],
    InventoryType.WAIST: [CharacterEquipSlot.WAIST],
    InventoryType.LEGS: [CharacterEquipSlot.LEGS],
    InventoryType.FEET: [CharacterEquipSlot.FEET],
    InventoryType.WRISTS: [CharacterEquipSlot.WRISTS],
    InventoryType.HANDS: [CharacterEquipSlot.HANDS],
    InventoryType.FINGER: [CharacterEquipSlot.FINGER1, CharacterEquipSlot.FINGER2],
    InventoryType.TRINKET: [CharacterEquipSlot.TRINKET1, CharacterEquipSlot.TRINKET2],
    InventoryType.WEAPON: [CharacterEquipSlot.MAINHAND, CharacterEquipSlot.OFFHAND],
    InventoryType.SHIELD: [CharacterEquipSlot.OFFHAND],
    InventoryType.RANGED: [CharacterEquipSlot.RANGED],
    InventoryType.CLOAK: [CharacterEquipSlot.BACK],
    InventoryType.WEAPON_2H: [CharacterEquipSlot.MAINHAND],
    InventoryType.BAG: [
        CharacterEquipSlot.BAG1,
        CharacterEquipSlot.BAG2,
        CharacterEquipSlot.BAG3,
        CharacterEquipSlot.BAG4
    ],
    InventoryType.TABARD: [CharacterEquipSlot.TABARD],
    InventoryType.ROBE: [CharacterEquipSlot.CHEST],
    InventoryType.WEAPON_MAINHAND: [CharacterEquipSlot.MAINHAND],
    InventoryType.WEAPON_OFFHAND: [CharacterEquipSlot.OFFHAND],
    InventoryType.HOLDABLE: [CharacterEquipSlot.OFFHAND],
    InventoryType.AMMO: [],
    InventoryType.THROWN: [CharacterEquipSlot.RANGED],
    InventoryType.RANGED_RIGHT: [CharacterEquipSlot.RANGED],
    InventoryType.QUIVER: [
        CharacterEquipSlot.BAG1,
        CharacterEquipSlot.BAG2,
        CharacterEquipSlot.BAG3,
        CharacterEquipSlot.BAG4
    ],
    InventoryType.RELIC: [CharacterEquipSlot.OFFHAND]
}
