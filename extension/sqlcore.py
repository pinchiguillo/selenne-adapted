import discord
from discord.ext import commands
import json

import dcs.sqltools

#!
async def setup(b):
    global bot
    bot = b

    #! StartUp
    connect()

    #! Load Help
    #add_help()

    #! Add CMD
    #bot.add_command(extension)
    
    #! Add Listener
    #bot.add_listener(on_message)
    
    #Check Bot Version and Log
    bv = list(bot.version)
    b_v = list(bot_version)
    if b_v[8:11] != bv[8:11]: bot.log.warning(f'extension.{_version.lower()} outdated')
    bot.log.info(f'extension.{_version.lower()} loaded')
def teardown(bot):
    bot.log.info(f'extension.{_version.lower()} unloaded')
    remove_help()

    disconnect()

#! Extension Data
bot_version = 'Selenne 5.1'
version = 'Alfa'
name = 'SQL Core'

_version = name.replace(' ', '.')
_version = f'{name.lower()}: {version}'

#! Databases
db_type = '$json'
system_path = 'db/system/servers.json'
db_path = 'db/system/sql.json'
def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        global db
        db =  json.load(f)
def save_db():
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5, ensure_ascii = False)
def server_db(ctx, mode = 'load', database = None):
    if mode == 'load':
        with open(system_path, 'r', encoding='utf-8') as f:
            _db=  json.load(f)
            return _db[str(ctx.guid.id)]
    elif mode == 'unload':
        with open(system_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=5, ensure_ascii = False)

#! HELP
extension_help = {
    'general_display': 'cmd',
    'specific_display': {
        'cmd': 'use'
        }
    }
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[name] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[name]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5, ensure_ascii= False)

def connect():
    bot.database = dcs.sqltools.DataBase(file=db_path)
    try:
        bot.database.connect()
        bot.log.info('SQLCORE: Database connected')
    except Exception as error: bot.log.error(f'SQLCORE: {error}')
def disconnect():
    bot.database.disconnect()
    bot.log.info('SQLCORE: Database disconected')