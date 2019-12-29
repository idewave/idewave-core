**Welcome** ! This is python wowcore for version 2.4.3. Developed for Linux, but I think you can run it on Windows too.

I'm very grateful to the Mangos community, in particular to Kyoril, for help and hints. 

## Before start
This works on Python v3.x.

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

**NOTICE: If you run the core on machine with different IP** be sure to replace '127.0.0.1' with destination IP for WorldServer in config !

## Already implemented
1. Login to the Server without extra checkings like incorrect password or account not exists and so on.
2. Create/Delete character
3. Enter the World
4. Show default equipment
5. Show another players
6. Broadcast movement
7. Broadcast chat (SAY and YELL)
8. Show MOTD (Message of the day)
9. Added dynamic weather


## Known issues
1. packet decryption not works correctly for some packets, so workaround was added (see WorldPacketManager)


## You want participate
You can add PR. To communicate join https://discord.gg/y6746sm
