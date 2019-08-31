from enum import Enum


class ChatMsgType(Enum):

    ADDON                       = 0xFFFFFFFF
    SYSTEM                      = 0x00
    SAY                         = 0x01
    PARTY                       = 0x02
    RAID                        = 0x03
    GUILD                       = 0x04
    OFFICER                     = 0x05
    YELL                        = 0x06
    WHISPER                     = 0x07
    WHISPER_INFORM              = 0x08
    REPLY                       = 0x09
    EMOTE                       = 0x0A
    TEXT_EMOTE                  = 0x0B
    MONSTER_SAY                 = 0x0C
    MONSTER_PARTY               = 0x0D
    MONSTER_YELL                = 0x0E
    MONSTER_WHISPER             = 0x0F
    MONSTER_EMOTE               = 0x10
    CHANNEL                     = 0x11
    CHANNEL_JOIN                = 0x12
    CHANNEL_LEAVE               = 0x13
    CHANNEL_LIST                = 0x14
    CHANNEL_NOTICE              = 0x15
    CHANNEL_NOTICE_USER         = 0x16
    AFK                         = 0x17
    DND                         = 0x18
    IGNORED                     = 0x19
    SKILL                       = 0x1A
    LOOT                        = 0x1B
    MONEY                       = 0x1C
    OPENING                     = 0x1D
    TRADESKILLS                 = 0x1E
    PET_INFO                    = 0x1F
    COMBAT_MISC_INFO            = 0x20
    COMBAT_XP_GAIN              = 0x21
    COMBAT_HONOR_GAIN           = 0x22
    COMBAT_FACTION_CHANGE       = 0x23
    BG_SYSTEM_NEUTRAL           = 0x24
    BG_SYSTEM_ALLIANCE          = 0x25
    BG_SYSTEM_HORDE             = 0x26
    RAID_LEADER                 = 0x27
    RAID_WARNING                = 0x28
    RAID_BOSS_EMOTE             = 0x29
    RAID_BOSS_WHISPER           = 0x2A
    FILTERED                    = 0x2B
    BATTLEGROUND                = 0x2C
    BATTLEGROUND_LEADER         = 0x2D
    RESTRICTED                  = 0x2E
