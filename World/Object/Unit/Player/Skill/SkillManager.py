from sqlalchemy import or_
from typing import List

from World.Object.Unit.Player.Skill.model import SkillTemplate, DefaultSkill
from World.Object.Unit.Player.model import Player, PlayerSkill
from Typings.Abstract import AbstractWorldManager
from Utils.Debug import Logger


class SkillManager(AbstractWorldManager):

    def __init__(self):
        self.skill_object = None

    def create(self, **kwargs):
        self.skill_object = SkillTemplate()
        self.skill_object.entry = kwargs.pop('entry')
        self.skill_object.name = kwargs.pop('name')
        self.skill_object.min = kwargs.pop('min')
        self.skill_object.max = kwargs.pop('max')

        return self

    def create_default_skill(self, **kwargs):
        race = kwargs.pop('race', None)
        char_class = kwargs.pop('char_class', None)
        entry = kwargs.pop('entry', None)

        skill_template = self.session.query(SkillTemplate).filter_by(entry=entry).first()

        if skill_template is None:
            raise Exception('Skill with entry {} not found'.format(entry))

        self.skill_object = DefaultSkill()
        self.skill_object.race = race
        self.skill_object.char_class = char_class
        self.skill_object.skill_template = skill_template

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
        self.session.add(self.skill_object)
        self.session.commit()
