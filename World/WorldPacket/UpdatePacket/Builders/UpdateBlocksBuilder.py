import math
from enum import Enum
from struct import Struct, error as StructError

from World.Object.Constants.FieldType import FieldType, FIELD_TYPE_MAP
from Typings.Abstract import AbstractBuilder

from Utils.Debug import Logger


class UpdateBlocksBuilder(AbstractBuilder):

    FIELD_BIN_MAP = {
        FieldType.INT32.value:        Struct('<i'),
        FieldType.TWO_INT16.value:    Struct('<I'),
        FieldType.FLOAT.value:        Struct('<f'),
        FieldType.INT64.value:        Struct('<q'),
        FieldType.FOUR_BYTES.value:   Struct('<I')
    }

    def __init__(self):
        self.mask_blocks = []
        self.update_blocks = {}

    def add(self, field, value, offset=0):
        try:
            field_type = FIELD_TYPE_MAP[field]
        except KeyError:
            Logger.error('[UpdatePacket Block Builder]: no type associated with {}'.format(str(field)))
            return
        else:
            field_struct = self.FIELD_BIN_MAP[field_type]
            index = offset and (field.value + offset) or field
            field_index = UpdateBlocksBuilder._get_field_index(index)

            self._set_field_mask_bits(field_index, field_struct)
            try:
                self._set_field_value(field_index, field_struct, value)
            except StructError:
                Logger.warning('Field with index {} should be set'.format(field_index))
                pass

    @staticmethod
    def _get_field_index(field):
        if isinstance(field, Enum):
            return field.value
        else:
            return int(field)

    def _set_field_mask_bits(self, field_index, field_struct):
        num_mask_blocks = math.ceil(field_struct.size / 4)
        for index in range(field_index, field_index + num_mask_blocks):
            self._set_field_mask_bit(index)

    def _set_field_mask_bit(self, field_index):
        mask_block_index = field_index // 32
        bit_index = field_index % 32

        while len(self.mask_blocks) < mask_block_index + 1:
            self.mask_blocks.append(0)

        self.mask_blocks[mask_block_index] |= 1 << bit_index

    def _set_field_value(self, field_index, field_struct, value):
        update_block = field_struct.pack(value)
        self.update_blocks[field_index] = update_block

    def build(self):
        num_mask_blocks_bytes = int.to_bytes(len(self.mask_blocks), 1, 'little')
        mask_blocks = [int.to_bytes(b, 4, 'little') for b in self.mask_blocks]
        mask_bytes = b''.join(mask_blocks)
        sorted_blocks = [self.update_blocks[k] for k in sorted(self.update_blocks.keys())]
        update_data = b''.join(sorted_blocks)
        return num_mask_blocks_bytes + mask_bytes + update_data
