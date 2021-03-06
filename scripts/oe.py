#!/usr/bin/env python
import argparse
from odooenv import OdooEnv
from messages import Msg
from options import get_param

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""
==========================================================================
Odoo Environment Manager v0.7.4 - by jeo Software <jorge.obiols@gmail.com>
==========================================================================
""")

    parser.add_argument(
        '-i',
        '--install',
        action='store_true',
        help="Install, requires -c option. Creates dir structure, and pull "
             "repos")

    parser.add_argument(
        '-w', '--write-config',
        action='store_true',
        help="Write config file.")

    parser.add_argument(
        '-R', '--run-env',
        action='store_true',
        help="Run postgres and aeroo images.")

    parser.add_argument(
        '-r', '--run-cli',
        action='store_true',
        help="Run client odoo, requires -c option")

    parser.add_argument(
        '-S', '--stop-env',
        action='store_true',
        help="Stop postgres and aeroo images.")

    parser.add_argument(
        '-s', '--stop-cli',
        action='store_true',
        help="Stop client images, requires -c options.")

    parser.add_argument(
        '-u', '--update-all',
        action='store_true',
        help="Update all requires -d -c and -m options. "
             "Use --debug to force update with host sources")

    parser.add_argument(
        '-c',
        action='append',
        dest='client',
        help="Client name.")

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Go verbose mode. Prints every command")

    parser.add_argument(
        '--debug',
        action='store_true',
        help='This option has the following efects: '
             '1.- when doing an update all, (option -u) it forces debug '
             'mode. '
             '2.- When running environment (option -R) it opens port '
             '5432 to access postgres server databases. '
             '3.- when doing a pull (option -p) it clones the full repo i.e. '
             'does not issue --depth 1 to git ')

    parser.add_argument(
        '--no-repos',
        action='store_true',
        help='Does not clone or pull repos used with -i or -p')

    parser.add_argument(
        '-d',
        action='store',
        nargs=1,
        dest='database',
        help="Database name.")

    parser.add_argument(
        '-m',
        action='append',
        dest='module',
        help="Module to update or all for updating all the registered "
             "modules. You can specify multiple -m options. i.e. -m all for"
             "all modules -m sales stock for updating sales and stock modules")

    parser.add_argument(
        '--nginx',
        action='store_true',
        help='Add nginx to installation: With -i creates nginx dir w/ sample '
             'config file. with -r starts an nginx container linked to odoo'
             'with -s stops nginx containcer. You must add certificates and '
             'review nginx.conf file.')

    parser.add_argument(
        '-Q',
        action='store',
        metavar='repo',
        nargs=1,
        dest='quality_assurance',
        help="Perform QA running tests, argument are Repo to test. "
             "Need -d, -m and -c options Note: for the test to run in the"
             "database there must be an admin user with password admin")

    parser.add_argument(
        '--backup-list',
        action='store_true',
        help="List all backup files available for restore")

    parser.add_argument(
        '--restore',
        action='store_true',
        help="Restores a backup from backup_dir")

    parser.add_argument(
        '-f',
        action='append',
        dest='backup_file',
        help="Filename to restore used with --restore")

    parser.add_argument(
        '-H', '--server-help',
        action='store_true',
        help="List server help requires -c option ")

    args = parser.parse_args()
    options = {
        'verbose': args.verbose,
        'debug': args.debug,
        'no-repos': args.no_repos,
        'nginx': args.nginx,
        'postfix': False,
        'backup_file': args.backup_file
    }
    commands = []

    if args.write_config:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).write_config(client_name)

    if args.server_help:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).server_help(client_name)

    if args.backup_list:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).backup_list(client_name)

    if args.restore:
        client_name = get_param(args, 'client')
        database = get_param(args, 'database')
        backup_file = get_param(args, 'backup_file')
        commands += OdooEnv(options).restore(client_name,
                                             database,
                                             backup_file)

    if args.install:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).install(client_name)

    if args.stop_env:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).stop_environment(client_name)

    if args.run_env:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).run_environment(client_name)

    if args.stop_cli:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).stop_client(client_name)

    if args.run_cli:
        client_name = get_param(args, 'client')
        commands += OdooEnv(options).run_client(client_name)

    if args.update_all:
        client_name = get_param(args, 'client')
        database = get_param(args, 'database')
        modules = get_param(args, 'module')
        commands += OdooEnv(options).update_all(client_name, database, modules)

    if args.quality_assurance:
        client_name = get_param(args, 'client')
        database = get_param(args, 'database')
        commands += OdooEnv(options).qa(client_name, database, args.quality_assurance[0])

    # #####################################################################
    # ejecutar comandos
    # ######################################################################
    for command in commands:
        if command and command.check():
            Msg().inf(command.usr_msg)
            command.execute()
