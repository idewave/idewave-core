from World.WorldPacket.Constants.BaseOpCode import BaseOpcode


class LoginOpCode(BaseOpcode):

    LOGIN_CHALL     = 0x00
    LOGIN_PROOF     = 0x01
    RECON_CHALL     = 0x02  # currently do not in use
    RECON_PROOF     = 0x03  # currently do not in use
    REALMLIST       = 0x10
