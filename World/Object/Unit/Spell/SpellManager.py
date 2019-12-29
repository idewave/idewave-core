from sqlalchemy import or_, and_
from typing import List

from DB.Connection.WorldConnection import WorldConnection
from World.Object.Unit.Spell.model import SpellTemplate, DefaultSpell
from World.Object.Unit.Player.model import Player, PlayerSpell


class SpellManager(object):

    __slots__ = ('session', 'spell_object')

    def __init__(self, **kwargs):
        self.spell_object = None

    def create(self, **kwargs):
        entry = kwargs.pop('entry', None)
        name = kwargs.pop('name', None)
        cost = kwargs.pop('cost', None)
        school = kwargs.pop('school', None)
        spell_range = kwargs.pop('range', None)

        self.spell_object = SpellTemplate()
        self.spell_object.entry = entry
        self.spell_object.name = name
        self.spell_object.cost = cost
        self.spell_object.school = school
        self.spell_object.range = spell_range

        return self

    def create_default_spell(self, **kwargs):
        race = kwargs.pop('race', None)
        char_class = kwargs.pop('char_class', None)
        entry = kwargs.pop('entry', None)

        spell_template = self.session.query(SpellTemplate).filter_by(entry=entry).first()

        if spell_template is None:
            raise Exception('Spell with entry {} not found'.format(entry))

        self.spell_object = DefaultSpell()
        self.spell_object.race = race
        self.spell_object.char_class = char_class
        self.spell_object.spell_template = spell_template

        return self

    def set_default_spells(self, player: Player):
        default_spells: List[DefaultSpell] = self.session \
            .query(DefaultSpell) \
            .filter(or_(
                or_(DefaultSpell.race == player.race, DefaultSpell.char_class == player.char_class),
                and_(DefaultSpell.race.is_(None), DefaultSpell.char_class.is_(None))
            )) \
            .all()

        # default_spells: List[DefaultSpell] = self.session \
        #     .query(DefaultSpell) \
        #     .filter(
        #     ((DefaultSpell.race == player.race) | (DefaultSpell.char_class == player.char_class)) |
        #     ((DefaultSpell.race is None) & (DefaultSpell.char_class is None))
        # ) \
        #     .all()

        spells = []

        for default_spell in default_spells:
            spell = PlayerSpell()
            spell.spell_template = default_spell.spell_template
            spell.player = self.session.merge(player)
            spells.append(spell)

        self.session.add_all(spells)
        self.session.commit()

        return self

    def save(self):
        self.session.add(self.spell_object)
        self.session.commit()

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = WorldConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return False
