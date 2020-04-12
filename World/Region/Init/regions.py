from World.Region.RegionManager import RegionManager
from World.Region.Octree.Builders.RegionOctreeMapBuilder import RegionOctreeMapBuilder


with RegionManager() as region_mgr:
    identifier_region_map = region_mgr.load_regions()
    region_octree_map = RegionOctreeMapBuilder(regions=identifier_region_map.values()).build()
