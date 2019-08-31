from sqlalchemy import or_
from typing import List

from DB.Connection.WorldConnection import WorldConnection
from World.Object.Unit.Player.Skill.model import SkillTemplate, DefaultSkill
from World.Object.Unit.Player.model import Player, PlayerSkill

from Utils.Debug.Logger import Logger


class SkillManager(object):

    def __init__(self, **kwargs):
        connection = WorldConnection()
        self.session = connection.session
        self.world_object = None
        self.temp_ref = kwargs.pop('temp_ref', None)

    def create(self, **kwargs):
        entry = kwargs.pop('entry', None)
        name = kwargs.pop('name', None)
        min = kwargs.pop('min', None)
        max = kwargs.pop('max', None)

        self.world_object = SkillTemplate()
        self.world_object.entry = entry
        self.world_object.name = name
        self.world_object.min = min
        self.world_object.max = max

        return self

    def create_default_skill(self, **kwargs):
        race = kwargs.pop('race', None)
        char_class = kwargs.pop('char_class', None)
        entry = kwargs.pop('entry', None)

        skill_template = self.session.query(SkillTemplate).filter_by(entry=entry).first()

        if skill_template is None:
            raise Exception('Skill with entry {} not found'.format(entry))

        self.world_object = DefaultSkill()
        self.world_object.race = race
        self.world_object.char_class = char_class
        self.world_object.skill_template = skill_template

        return self

    def set_default_skills(self, player: Player):
        try:
            default_skills: List[DefaultSkill] = self.session\
                .query(DefaultSkill)\
                .filter(or_(DefaultSkill.race == player.race, DefaultSkill.char_class == player.char_class))\
                .all()

            skills = []

            for default_skill in default_skills:
                skill = PlayerSkill()
                skill.skill_template = default_skill.skill_template
                skill.player = self.session.merge(player)
                skills.append(skill)

            self.session.add_all(skills)
            self.session.commit()

        except Exception as e:
            Logger.error('[SkillMgr]: {}'.format(e))
        finally:
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
