from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
from World.Observer.Init.observers import world_observer


login_server = LoginServer.create()
world_server = WorldServer.create(world_observer=world_observer)
