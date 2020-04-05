import argparse
import json
from os import urandom
import traceback

from DB.CreateDB import create_db, create_tables
from DB.DropDB import drop_db
from DB.Fixtures.Loader.load_world_data import load_world_data

from Account.AccountManager import AccountManager
from World.Object.Item.ItemManager import ItemManager
from World.Object.Unit.Spell.SpellManager import SpellManager
from World.Object.Unit.Player.Skill.SkillManager import SkillManager
# from World.Region.RegionManager import RegionManager
# from World.Object.Unit.UnitManager import UnitManager

from Server.Auth.Crypto.SRP import SRP

from Utils.Debug import Logger


def process():
    parser = argparse.ArgumentParser(prog='cmd')
    commands = parser.add_subparsers(help='Available console commands')

    # database
    db_parser = commands.add_parser('db')

    args = db_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'db':
        if subcommand == 'create':
            create_db()
            Logger.success('All dbs was created')

        elif subcommand == 'create_tables':
            create_tables()
            Logger.success('All required tables was created')

        elif subcommand == 'drop':
            drop_db()
            Logger.warning('Databases were dropped')

        elif subcommand == 'recreate':
            drop_db()
            create_db()
            create_tables()
            Logger.notify('DB was successfully re-created')

        elif subcommand == 'load_data':
            load_world_data()

        elif subcommand == 'recreate_with_load':
            try:
                drop_db()
                create_db()
                create_tables()
                Logger.notify('DB was successfully re-created')
                load_world_data()
            except Exception as e:
                traceback.print_exc()
                Logger.error(f'[Recreate DB]: exception: {e}')


    # accounts
    account_parser = commands.add_parser('account')
    account_parser.add_argument('-n', '--name')
    account_parser.add_argument('-p', '--password')

    args = account_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'account':
        if subcommand == 'create':
            with AccountManager() as account_mgr:
                name = args[0].name
                password = args[0].password
                salt = urandom(32)
                verifier = SRP.generate_verifier(
                    username=name.upper(),
                    password=password.upper(),
                    salt=salt
                )
                account_mgr.create(
                    name=name,
                    salt=salt,
                    verifier=verifier
                )
                Logger.success('Account "{}" created successfully!'.format(args[0].name))

    # items
    item_parser = commands.add_parser('item')
    item_parser.add_argument('-d', '--display_id')
    item_parser.add_argument('-i', '--item_type')
    item_parser.add_argument('-e', '--entry')

    args = item_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'item':
        if subcommand == 'create':
            with ItemManager() as item_mgr:
                item_mgr.create(
                    display_id=args[0].display_id,
                    item_type=args[0].item_type,
                    entry=int(args[0].entry)
                ).save()

                Logger.success('Item "{}" created successfully!'.format(args[0].entry))

    # spells
    spell_parser = commands.add_parser('spell')
    spell_parser.add_argument('-e', '--entry')
    spell_parser.add_argument('-n', '--name')
    spell_parser.add_argument('-c', '--cost')
    spell_parser.add_argument('-s', '--school')
    spell_parser.add_argument('-r', '--range')

    args = spell_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'spell':
        if subcommand == 'create':
            with SpellManager() as spell_mgr:
                spell_mgr.create(
                    entry=args[0].entry,
                    name=args[0].name,
                    cost=args[0].cost,
                    school=args[0].school,
                    range=args[0].range
                ).save()

                Logger.test('Spell "{}" ({}) created successfully!'.format(args[0].name, args[0].entry))

    # default spells
    default_spell_parser = commands.add_parser('default_spell')
    default_spell_parser.add_argument('-e', '--entry')
    default_spell_parser.add_argument('-r', '--race')
    default_spell_parser.add_argument('-c', '--char_class')

    args = default_spell_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'default_spell':
        if subcommand == 'create':
            with SpellManager() as spell_mgr:
                spell_mgr.create_default_spell(
                    entry=args[0].entry,
                    race=args[0].race,
                    char_class=args[0].char_class
                ).save()

                Logger.test(
                    'Default spell "{}" ({}:{}) created successfully!'.format(
                        args[0].entry,
                        args[0].race,
                        args[0].char_class
                    )
                )


    # skills
    # skill_parser = commands.add_parser('skill')
    # skill_parser.add_argument('-e', '--entry')
    # skill_parser.add_argument('-n', '--name')
    #
    # args = skill_parser.parse_known_args()
    # parser_name = args[1][0]
    # subcommand = args[1].pop()
    #
    # if parser_name == 'skill':
    #     if subcommand == 'create':
    #         SkillManager().create(
    #             entry=args[0].entry,
    #             name=args[0].name
    #         ).save()
    #
    #         Logger.test('Skill "{}" ({}) created successfully!'.format(args[0].name, args[0].entry))

    # skills
    skill_parser = commands.add_parser('skill')
    skill_parser.add_argument('-e', '--entry')
    skill_parser.add_argument('-n', '--name')
    skill_parser.add_argument('--min')
    skill_parser.add_argument('--max')

    args = skill_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'skill':
        if subcommand == 'create':
            SkillManager().create(
                entry=args[0].entry,
                name=args[0].name,
                min=args[0].min,
                max=args[0].max
            ).save()

            Logger.success('Skill "{}" ({}) created successfully!'.format(args[0].name, args[0].entry))

    # default skills
    default_skill_parser = commands.add_parser('default_skill')
    default_skill_parser.add_argument('-e', '--entry')
    default_skill_parser.add_argument('-r', '--race')
    default_skill_parser.add_argument('-c', '--char_class')

    args = default_skill_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'default_skill':
        if subcommand == 'create':
            SkillManager().create_default_skill(
                entry=args[0].entry,
                race=args[0].race,
                char_class=args[0].char_class
            ).save()

            Logger.success(
                'Default skill "{}" ({}:{}) created successfully!'.format(
                    args[0].entry,
                    args[0].race,
                    args[0].char_class
                )
            )

    # regions
    # region_parser = commands.add_parser('region')
    # region_parser.add_argument('-i', '--identifier')
    # region_parser.add_argument('--y1')
    # region_parser.add_argument('--y2')
    # region_parser.add_argument('--x1')
    # region_parser.add_argument('--x2')
    # region_parser.add_argument('-c', '--continent_id')
    #
    # # # arguments for default region
    # region_parser.add_argument('-r', '--race')
    # region_parser.add_argument('-m', '--map_id')
    #
    # # # arguments for region unit # #
    # region_parser.add_argument('-u', '--unit_entry')
    #
    # # # arguments for both default region and region unit
    # region_parser.add_argument('-x')
    # region_parser.add_argument('-y')
    # region_parser.add_argument('-z')
    #
    # region_parser.add_argument('--file')
    #
    # args = region_parser.parse_known_args()
    # parser_name = args[1][0]
    # subcommand = args[1].pop()
    #
    # if parser_name == 'region':
    #     if subcommand == 'create':
    #         with RegionManager() as region_mgr:
    #             region_mgr.create(
    #                 identifier=args[0].identifier,
    #                 y1=args[0].y1,
    #                 y2=args[0].y2,
    #                 x1=args[0].x1,
    #                 x2=args[0].x2,
    #                 continent_id=args[0].continent_id,
    #             ).save()
    #
    #             Logger.notify('Region "{}" created successfully!'.format(args[0].identifier))
    #
    #     elif subcommand == 'add_default_location':
    #         with RegionManager() as region_mgr:
    #             region_mgr.create_default_location(
    #                 identifier=args[0].identifier,
    #                 x=args[0].x,
    #                 y=args[0].y,
    #                 z=args[0].z,
    #                 race=args[0].race,
    #                 map_id=args[0].map_id
    #             )
    #
    #             Logger.success('Default location ({}) for race "{}" successfully added'.format(
    #                 args[0].identifier, args[0].race
    #             ))
    #
    #     elif subcommand == 'add_units':
    #         with open(args[0].file, 'r') as myfile:
    #             data = myfile.read()
    #
    #         json_data = json.loads(data)
    #
    #         for item in json_data:
    #             with UnitManager() as unit_mgr:
    #                 unit_mgr.new(
    #                     entry=item['entry'],
    #                     identifier=item['identifier'],
    #                     x=item['position_x'],
    #                     y=item['position_y'],
    #                     z=item['position_z']
    #                 ).save()
    #
    #         Logger.success('Units successfully added')

process()
