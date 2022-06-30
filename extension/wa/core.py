import discord
from discord.ext import commands
import json

import character

#?
async def setup(b):
    global bot
    bot = b
    
    #? StartUp

    #? Load Help
    #add_help()

    #? Add CMD
    #bot.add_command(extension)
    
    #? Add Listener
    #bot.add_listener(on_message)

    #Check Bot Version and Log
    bv = list(bot.version)
    b_v = list(bot_version)
    if b_v[8:11] != bv[8:11]: bot.log.warning(f'extension.{_version.lower()} outdated')
    bot.log.info(f'extension.{_version.lower()} loaded')
def teardown(bot):
    bot.log.info(f'extension.{_version.lower()} unloaded')
    remove_help()

#? Extension Data
bot_version = 'Selenne 5.0'
version = 'Alfa'
name = 'WA Project'

_version = name.replace(' ', '.')
_version = f'{name.lower()}: {version}'

#? Databases
db_type = '$json'
system_path = 'db/system/servers.json'
db_path = system_path #!PATH
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

#? HELP
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

#?Extension functions
def emoji(message):
    with open('data/emojis.json', 'r', encoding='utf-8') as f:
        emogis = json.load(f)
    
    for emoji in emogis.keys():
        message = message.replace(emoji, emogis[emoji])
    
    return message

# Commands
@commands.command()
async def wa(ctx, command = 'help', *, args = None):

    #?Check if player wants to delete message
    #await ctx.message.delete()

    #! Check if player registered

    match command.lower():
        #* Interacciones personaje
        case 'register': await character.register(bot,ctx,args)
        case 'delete_profile': await character.delete_profile(bot,ctx,args)
        case 'profile': await character.profile(bot, ctx,args)
        case 'inventory': await character.inventory(bot,ctx,args)
        case 'config': await character.config(bot,ctx,args)

        #* Interacciones mundo abierto
        case 'travel':pass
        case 'fight':pass

        #* Interacciones modos de juego
        case 'dungeons':pass
        case 'tower':pass
        case 'coliseum':pass

        #* Interacciones redes sociales
        case 'friends':pass
        case 'guild':pass
        case 'party':pass

        #* Interacciones trabajos
        case 'fish':pass
        case 'hunt':pass
        case 'mine':pass
        case 'crafting':pass
        case 'restore':pass

        #* Housing System
        case 'home':pass

        #* Interacciones Misiones
        case 'mission':pass
        case 'login':pass

        #* Interacciones Soporte
        case 'support':pass #Server sub
        case 'report':pass #Bug Sub
        case 'help':pass
        case 'wiki':pass

        #* Default
        case _:pass