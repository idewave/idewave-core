import subprocess
from os import walk, path

from Utils.Debug.Logger import Logger

from Config.Run.config import Config

MAP_DIRNAME_TO_DBNAME = {
    0: {
        'dir_name': 'World',
        'db_name': Config.Database.DBNames.world_db
    },
    1: {
        'dir_name': 'Realm',
        'db_name': Config.Database.DBNames.realm_db
    }
}


def load_world_data():
    def get_command(db_name):
        return 'mysql -h{host} -u"{username}" -p"{password}" -D"{db_name}"'.format(
            host=Config.Database.Connection.host,
            username=Config.Database.Connection.username,
            password=Config.Database.Connection.password,
            db_name=db_name
        )

    for key in MAP_DIRNAME_TO_DBNAME.keys():

        files = []

        command = get_command(db_name=MAP_DIRNAME_TO_DBNAME[key]['db_name'])

        fixture_dir = MAP_DIRNAME_TO_DBNAME[key]['dir_name']

        for (dirpath, _, filenames) in walk('DB/Fixtures/{}'.format(fixture_dir)):
            filenames.sort()
            for file in filenames:
                files.append(path.join(dirpath, file))

        for file in files:
            Logger.notify('Start loading {}'.format(file))
            subprocess.run('{} < {}'.format(command, file), shell=True)
            Logger.success('{} successfully imported'.format(file))
