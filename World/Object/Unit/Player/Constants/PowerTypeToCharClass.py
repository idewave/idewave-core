from World.Object.Unit.Constants.UnitPower import UnitPower
from World.Object.Unit.Player.Constants.CharacterClass import CharacterClass


POWER_TYPE = {
    CharacterClass.WARRIOR.value: UnitPower.RAGE.value,
    CharacterClass.PALADIN.value: UnitPower.MANA.value,
    CharacterClass.HUNTER.value: UnitPower.FOCUS.value,
    CharacterClass.ROGUE.value: UnitPower.ENERGY.value,
    CharacterClass.PRIEST.value: UnitPower.MANA.value,
    CharacterClass.SHAMAN.value: UnitPower.MANA.value,
    CharacterClass.MAGE.value: UnitPower.MANA.value,
    CharacterClass.WARLOCK.value: UnitPower.MANA.value,
    CharacterClass.DRUID.value: UnitPower.MANA.value,
}
