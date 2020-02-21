from World.Object.Unit.Player.Constants.CharacterClass import CharacterClass

ATTRIBUTES_PER_LEVEL = {
    CharacterClass.WARRIOR.value: {
        "strength": {
            "melee_attack_power": 2
        },
        "agility": {
            "range_attack_power": 2,
            "armor": 2
        },
        "stamina": {
            "health": 10
        }
    },

    CharacterClass.PALADIN.value: {
        "strength": {
            "melee_attack_power": 2
        },
        "agility": {
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    },

    CharacterClass.HUNTER.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "range_attack_power": 2,
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    },

    CharacterClass.ROGUE.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "range_attack_power": 2,
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
    },

    CharacterClass.PRIEST.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    },

    CharacterClass.SHAMAN.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    },

    CharacterClass.MAGE.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    },

    CharacterClass.WARLOCK.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    },

    CharacterClass.DRUID.value: {
        "strength": {
            "melee_attack_power": 1
        },
        "agility": {
            "range_attack_power": 2,
            "armor": 2
        },
        "stamina": {
            "health": 10
        },
        "intellect": {
            "mana": 15
        }
    }
}