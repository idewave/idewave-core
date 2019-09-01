from sqlalchemy import or_
from typing import List

from DB.Connection.WorldConnection import WorldConnection
from World.Object.Unit.Spell.model import SpellTemplate, DefaultSpell
from World.Object.Unit.Player.model import Player, PlayerSpell


class SpellManager(object):

    def __init__(self, **kwargs):
        # connection = WorldConnection()
        # self.session = connection.session
        self.world_object = None
        self.temp_ref = kwargs.pop('temp_ref', None)

    def create(self, **kwargs):
        entry = kwargs.pop('entry', None)
        name = kwargs.pop('name', None)
        cost = kwargs.pop('cost', None)
        school = kwargs.pop('school', None)
        spell_range = kwargs.pop('range', None)

        self.world_object = SpellTemplate()
        self.world_object.entry = entry
        self.world_object.name = name
        self.world_object.cost = cost
        self.world_object.school = school
        self.world_object.range = spell_range

        return self

    def create_default_spell(self, **kwargs):
        race = kwargs.pop('race', None)
        char_class = kwargs.pop('char_class', None)
        entry = kwargs.pop('entry', None)

        spell_template = self.session.query(SpellTemplate).filter_by(entry=entry).first()

        if spell_template is None:
            raise Exception('Spell with entry {} not found'.format(entry))

        self.world_object = DefaultSpell()
        self.world_object.race = race
        self.world_object.char_class = char_class
        self.world_object.spell_template = spell_template

        return self

    def set_default_spells(self, player: Player):
        default_spells: List[DefaultSpell] = self.session \
            .query(DefaultSpell) \
            .filter(or_(DefaultSpell.race == player.race, DefaultSpell.char_class == player.char_class)) \
            .all()

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
        self.session.add(self.world_object)
        self.session.commit()

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = WorldConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return True
