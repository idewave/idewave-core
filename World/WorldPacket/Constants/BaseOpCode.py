from enum import Enum

from Exceptions.Wrappers.ProcessException import ProcessException


class BaseOpcode(Enum):

    @classmethod
    @ProcessException
    def get_opcode(cls, value: int):
        return cls(value)
