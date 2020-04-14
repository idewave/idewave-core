from Typings.Abstract.AbstractLoader import AbstractLoader
from Init.Registry.InitRegistry import InitRegistry
from Config.Init.configs import main_config
from Server.Init.servers import login_server, world_server
from World.Observer.Init.observers import world_observer
from World.Region.Init.regions import identifier_region_map, region_octree_map


class InitLoader(AbstractLoader):

    @staticmethod
    def load(**kwargs):
        InitRegistry.main_config = main_config
        InitRegistry.login_server = login_server
        InitRegistry.world_server = world_server
        InitRegistry.world_observer = world_observer
        InitRegistry.identifier_region_map = identifier_region_map
        InitRegistry.region_octree_map = region_octree_map
