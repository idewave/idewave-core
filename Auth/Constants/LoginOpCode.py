from enum import Enum


class LoginOpCode(Enum):

    ''' Opcodes during login process '''

    LOGIN_CHALL = 0x00
    LOGIN_PROOF = 0x01
    RECON_CHALL = 0x02  # currently do not in use
    RECON_PROOF = 0x03  # currently do not in use
    REALMLIST   = 0x10


class LoginResult(Enum):
    ''' Error codes '''
    SUCCESS             = 0x00
    FAIL_UNKNOWN_ACCT   = 0x04
    FAIL_INCORRECT_PASS = 0X05
