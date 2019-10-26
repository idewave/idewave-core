from enum import Enum


class BaseOpcode(Enum):

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in tuple(item.value for item in cls)

    @classmethod
    def get_opcode(cls, value: int):
        if cls.has_value(value):
            return cls(value)

        return None
