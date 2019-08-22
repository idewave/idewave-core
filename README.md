**Welcome** ! This is python wowcore for version 2.4.3. Developed for Linux, but I think you can run it on Windows too.

I'm very grateful to the Mangos community, in particular to Kyoril, for help and hints. 

## Before start
This works on Python v3.5 - v3.7. Not tested another versions yet.

## Installation

Install MySQL and create new user:

`CREATE USER 'user'@'localhost' IDENTIFIED BY 'password'`

And add to this user permissions:

`GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' IDENTIFIED BY 'password'; FLUSH PRIVILEGES;`

**Notice**: Giving all privileges to the user can be insecure, so after successfully creating databases you can reduce
privileges to only this databases.

Next install Python packets:

`pip3 install -r requirements.txt`

## Dependencies successfully installed
Well, now you are ready to start. You need to install DB, just run the command from console in the root of project:

`python3 console.py db recreate_with_load`

Next you can create test account:

`python3 console.py account create -n<username> -p<password>`

(Look into console.py for another commands).

Finally, you can run the server, just call from the root of project:

`python3 Run.py`

**For opening the core on vps or dedicated servers** be sure to set correct IP in config !

## How it works ?
OK, I promise, I will add the detailed documentation in nearest future. But, in short:

- Currently there are three servers: LoginServer, WorldServer and WebServer + WorldManager.
- Each of them communicates with others by queues or redis.
- There are exists three type of managers: EntityManager, StateManager, EventManager. In future I want to make this
differentiation more strictly and clearly.
- There are no global ObjectManager, on the contrary for each object exists separate manager. Thus, EntityManagers are:
ObjectManager, UnitManager, PlayerManager, ItemManager, RegionManager etc
- EventManager just gets request and returns response. The example of such manager: WorldPacketManager.
- StateManager not works with specific object, it affects all objects. Such manager is WorldManager.
- WebServer allows to get real-time data from server and pass it to any websocket client. This data can be: 
players/units/objects positions (movement), statistics (for example, ore spawn) and so on.


## Known issues
1. packet decryption not works correctly for some packets, so workaround was added (see WorldPacketManager)


## You want participate
You can add PR. To communicate join https://discord.gg/y6746sm
