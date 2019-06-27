import argparse
from DB.CreateDB import create_db, create_tables
from DB.DropDB import drop_db
from DB.Fixtures.Loader.load_world_data import load_world_data
from Account.AccountManager import AccountManager
from World.Object.Item.ItemManager import ItemManager
from World.Object.Unit.Player.Inventory.Equipment import EquipmentManager
from World.Object.Unit.Spell.SpellManager import SpellManager
from World.Object.Unit.Player.Skill.SkillManager import SkillManager
from World.Region.RegionManager import RegionManager
from World.Object.Unit.UnitManager import UnitManager
from Utils.Debug.Logger import Logger


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
            Logger.warning('All db was dropped')

        elif subcommand == 'recreate':
            drop_db()
            create_db()
            create_tables()
            Logger.notify('DB was successfully re-created')

        elif subcommand == 'load_data':
            load_world_data()

        elif subcommand == 'recreate_with_load':
            drop_db()
            create_db()
            create_tables()
            Logger.notify('DB was successfully re-created')
            load_world_data()


    # accounts
    account_parser = commands.add_parser('account')
    account_parser.add_argument('-n', '--name')
    account_parser.add_argument('-p', '--password')

    args = account_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'account':
        if subcommand == 'create':
            AccountManager().create(name=args[0].name, password=args[0].password)
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
            ItemManager().create(
                display_id=args[0].display_id,
                item_type=args[0].item_type,
                entry=int(args[0].entry)
            ).save()

            Logger.success('Item "{}" created successfully!'.format(args[0].entry))

    # default equipment
    # default_equip_parser = commands.add_parser('default_equipment')
    # default_equip_parser.add_argument('-d', '--display_id')
    # default_equip_parser.add_argument('-i', '--item_type')
    # default_equip_parser.add_argument('-e', '--entry')
    # default_equip_parser.add_argument('-c', '--char_class')
    # default_equip_parser.add_argument('-r', '--race')
    # default_equip_parser.add_argument('-s', '--slot_id')
    #
    # args = default_equip_parser.parse_known_args()
    # parser_name = args[1][0]
    # subcommand = args[1].pop()

    # FIXME: currently method do not exists
    # if parser_name == 'default_equipment':
    #     if subcommand == 'create':
    #         EquipmentManager().create_default_equip(
    #             display_id=args[0].display_id,
    #             item_type=args[0].item_type,
    #             entry=int(args[0].entry),
    #             char_class=args[0].char_class,
    #             race=args[0].race,
    #             slot_id=args[0].slot_id,
    #         ).save()
    #
    #         Logger.success('Item "{}" created successfully!'.format(args[0].entry))

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
            SpellManager().create(
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
            SpellManager().create_default_spell(
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
    skill_parser = commands.add_parser('skill')
    skill_parser.add_argument('-e', '--entry')
    skill_parser.add_argument('-n', '--name')

    args = skill_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'skill':
        if subcommand == 'create':
            SkillManager().create(
                entry=args[0].entry,
                name=args[0].name
            ).save()

            Logger.test('Skill "{}" ({}) created successfully!'.format(args[0].name, args[0].entry))

    # regions
    region_parser = commands.add_parser('region')
    region_parser.add_argument('-r', '--region_id')
    region_parser.add_argument('--y1')
    region_parser.add_argument('--y2')
    region_parser.add_argument('--x1')
    region_parser.add_argument('--x2')
    region_parser.add_argument('-c', '--continent_id')

    # # arguments for region unit # #
    region_parser.add_argument('-u', '--unit_entry')
    region_parser.add_argument('-x')
    region_parser.add_argument('-y')
    region_parser.add_argument('-z')

    args = region_parser.parse_known_args()
    parser_name = args[1][0]
    subcommand = args[1].pop()

    if parser_name == 'region':
        if subcommand == 'create':
            RegionManager().create(
                region_id=args[0].region_id,
                y1=args[0].y1,
                y2=args[0].y2,
                x1=args[0].x1,
                x2=args[0].x2,
                continent_id=args[0].continent_id,
            ).save()

            Logger.notify('Region "{}" created successfully!'.format(args[0].region_id))

        elif subcommand == 'add_unit':
            unit = UnitManager().new(
                entry=args[0].unit_entry,
                region_id=args[0].region_id,
                x=args[0].x,
                y=args[0].y,
                z=args[0].z
            ).set_stats().save().unit

            Logger.notify(
                'Unit "{}" IN ({} - {} - {}) created successfully!'.format(
                    args[0].unit_entry,
                    args[0].x,
                    args[0].y,
                    args[0].z
                )
            )


process()
