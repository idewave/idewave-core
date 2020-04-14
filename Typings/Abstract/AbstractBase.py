from abc import ABCMeta

from Config.Mixins.ConfigurableMixin import ConfigurableMixin


class AbstractBase(ABCMeta, ConfigurableMixin):
    pass
