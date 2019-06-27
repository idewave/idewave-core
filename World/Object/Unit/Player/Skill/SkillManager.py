from DB.Connection.WorldConnection import WorldConnection
from World.Object.Unit.Player.Skill.model import SkillTemplate


class SkillManager(object):

    def __init__(self):
        connection = WorldConnection()
        self.session = connection.session
        self.skill_template = None

    def create(self, **kwargs):
        entry = kwargs.pop('entry', None)
        name = kwargs.pop('name', None)

        self.skill_template = SkillTemplate(entry=entry, name=name)
        self.session.add(self.skill_template)

        return self

    def save(self):
        self.session.commit()

    def __del__(self):
        self.session.close()
