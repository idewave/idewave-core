from enum import Enum


class UnitFlags(Enum):

    UNK_0                 = 0x00000001  # Movement checks disabled, likely paired with loss of client control packet.
    NON_ATTACKABLE        = 0x00000002  # not attackable
    CLIENT_CONTROL_LOST   = 0x00000004  # Generic unspecified loss of control initiated by server script,
                                        # movement checks disabled, paired with loss of client control packet.
    PLAYER_CONTROLLED     = 0x00000008  # players, pets, totems, guardians, companions,
                                        # charms, any units associated with players

    RENAME                = 0x00000010
    PREPARATION           = 0x00000020  # don't take reagents for spells with SPELL_ATTR_EX5_NO_REAGENT_WHILE_PREP
    UNK_6                 = 0x00000040
    NOT_ATTACKABLE_1      = 0x00000080  # ?? (PVP_ATTACKABLE | NOT_ATTACKABLE_1) is NON_PVP_ATTACKABLE
    IMMUNE_TO_PLAYER      = 0x00000100  # Target is immune to players
    IMMUNE_TO_NPC         = 0x00000200  # Target is immune to Non-Player Characters
    LOOTING               = 0x00000400  # loot animation
    PET_IN_COMBAT         = 0x00000800  # in combat?, 2.0.8
    PVP                   = 0x00001000
    SILENCED              = 0x00002000  # silenced, 2.1.1
    PERSUADED             = 0x00004000  # persuaded, 2.0.8
    SWIMMING              = 0x00008000  # controls water swimming animation - TODO: confirm whether dynamic or static
    NON_ATTACKABLE_2      = 0x00010000  # removes attackable icon, if on yourself, cannot assist self
                                        # but can cast TARGET_UNIT_CASTER spells - added by SPELL_AURA_MOD_UNATTACKABLE
    PACIFIED              = 0x00020000
    STUNNED               = 0x00040000  # Unit is a subject to stun, turn and strafe movement disabled
    IN_COMBAT             = 0x00080000
    TAXI_FLIGHT           = 0x00100000  # Unit is on taxi, paired with a duplicate loss of client control packet
                                        # (likely a legacy serverside hack).
                                        # Disables any spellcasts not allowed in taxi flight client-side.
    DISARMED              = 0x00200000  # disable melee spells casting...,
                                        # "Required melee weapon" added to melee spells tooltip.
    CONFUSED              = 0x00400000  # Unit is a subject to confused movement, movement checks disabled,
                                        # paired with loss of client control packet.
    FLEEING               = 0x00800000  # Unit is a subject to fleeing movement, movement checks disabled,
                                        # paired with loss of client control packet.
    POSSESSED             = 0x01000000  # Unit is under remote control by another unit, movement checks disabled,
                                        # paired with loss of client control packet.
                                        # New master is allowed to use melee attack and can't select this unit
                                        # via mouse in the world (as if it was own character).
    NOT_SELECTABLE        = 0x02000000
    SKINNABLE             = 0x04000000
    MOUNT                 = 0x08000000
    UNK_28                = 0x10000000
    UNK_29                = 0x20000000    # used in Feign Death spell
    SHEATHE               = 0x40000000
