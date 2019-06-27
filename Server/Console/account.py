import argparse
from Account.AccountManager import AccountManager
from Utils.Debug.Logger import Logger


def account_create():
    parser = argparse.ArgumentParser('Account create')
    parser.add_argument('-n', '--name', help='Account name, will be saved in upper case')
    parser.add_argument('-p', '--password', help='Account password, won\'t be saved to db')

    args = parser.parse_args()

    AccountManager().create(name=args.name, password=args.password)

    Logger.success('Account "{}" successfully created'.format(args.name))
