# from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
# from World.Object.Constants.UpdateObjectFields import ObjectField, ItemField
# from World.WorldPacket.UpdatePacket import UpdatePacket
# from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType
# from World.Object.Item.model import Item
# from World.Object.Item.ItemManager import ItemManager
# from World.Character.Constants.CharacterEquipSlot import CharacterEquipSlot
# from Utils.Debug.Logger import Logger
#
#
# class ItemSpawn(object):
#
#     SPAWN_FIELDS = [
#         # Object fields
#         ObjectField.GUID,
#         ObjectField.TYPE,
#         ObjectField.ENTRY,
#         ObjectField.SCALE_X,
#
#         # Item fields
#         ItemField.OWNER,
#         ItemField.CONTAINED,
#         ItemField.STACK_COUNT,
#         ItemField.MAXDURABILITY,
#         ItemField.DURABILITY,
#         ItemField.DURATION
#     ]
#
#     def __init__(self, packet: bytes):
#         self.packet = packet
#
#     async def process(self):
#         test_item1 = session.player.equipment.get_object_field(CharacterEquipSlot.BODY)
#         test_item2 = session.player.equipment.get_object_field(CharacterEquipSlot.CHEST)
#         test_item3 = session.player.equipment.get_object_field(CharacterEquipSlot.LEGS)
#         test_item4 = session.player.equipment.get_object_field(CharacterEquipSlot.FEET)
#
#         spawned_item = UpdatePacket(test_item1, ObjectUpdateType.CREATE_OBJECT.value, False)
#
#         for field in self.SPAWN_FIELDS:
#             spawned_item.add_field(field, test_item1.get_object_field(field))
#
#         response = spawned_item.generate(send_packed_guid=True)
#
#         Logger.error('[ItemSpawn]: {}'.format(response))
#
#         return WorldOpCode.SMSG_UPDATE_OBJECT, response
#
#     def _create_test_item(self, entry: int):
#         item = Item()
#         item.set_owner(owner=session.player)
#         item.set_entry(entry=entry)
#         item.set_low_guid(counter=1)
#
#         item = ItemManager().create_item(item_data=item)
#
#         return item