from DB.Connection.WorldConnection import WorldConnection
from World.Object.Unit.Spell.model import SpellTemplate, DefaultSpell


class SpellManager(object):

    def __init__(self, **kwargs):
        connection = WorldConnection()
        self.session = connection.session
        self.world_object = None
        self.temp_ref = kwargs.pop('temp_ref', None)

    def create(self, **kwargs):
        entry = kwargs.pop('entry', None)
        name = kwargs.pop('name', None)
        cost = kwargs.pop('cost', None)
        school = kwargs.pop('school', None)
        range = kwargs.pop('range', None)

        self.world_object = SpellTemplate(entry=entry, name=name, cost=cost, school=school, range=range)

        return self

    def create_default_spell(self, **kwargs):
        race = kwargs.pop('race', None)
        char_class = kwargs.pop('char_class', None)
        entry = kwargs.pop('entry', None)

        spell_template = self.session.query(SpellTemplate).filter_by(entry=entry).first()

        if spell_template is None:
            raise Exception('Spell with entry {} not found'.format(entry))

        self.world_object = DefaultSpell(race=race, char_class=char_class)
        self.world_object.spell_template = spell_template

        return self

    def save(self):
        self.session.add(self.world_object)
        self.session.commit()

    def __del__(self):
        self.session.close()
