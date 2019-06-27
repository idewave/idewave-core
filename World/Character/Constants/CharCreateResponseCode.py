from enum import Enum


class CharCreateResponseCode(Enum):

    CHAR_CREATE_SUCCESS       = 0x2F
    CHAR_CREATE_FAILED        = 0x31
    CHAR_CREATE_NAME_IN_USE   = 0x32
    CHAR_CREATE_SERVER_LIMIT  = 0x35
    CHAR_CREATE_ACCOUNT_LIMIT = 0x36
