import discord
from discord.ext import commands
import json

import mysql.connector
import extension.wa.character as character

#?
async def setup(b):
    global bot
    bot = b
    
    #? StartUp

    #? Load Help
    #add_help()

    #? Add CMD
    bot.add_command(wa)
    
    #? Add Listener
    #bot.add_listener(on_message)

    #! LOAD DATABASE
    bot.db = DataBase(config={
        'host': 'localhost',
        'user': 'selenne_wa',
        'password': 'REDACTED_DB_PASSWORD',
        'database': 'selenne_wa'
    })
    bot.db.connect()

    #Check Bot Version and Log
    bv = list(bot.version)
    b_v = list(bot_version)
    if b_v[8:11] != bv[8:11]: bot.log.warning(f'extension.{_version.lower()} outdated')
    bot.log.info(f'extension.{_version.lower()} loaded')
def teardown(bot):
    bot.log.info(f'extension.{_version.lower()} unloaded')
    remove_help()
    
    del character
    
#? Extension Data
bot_version = 'Selenne 5.0'
version = 'Alfa'
name = 'WA Project'

_version = name.replace(' ', '.')
_version = f'{name.lower()}: {version}'

#? Databases
class DataBase():
    def __init__(self, config:dict = None, file:str = None):
        if not config and not file: raise ValueError('config dict or config file required')
        elif config: self.config = config
        elif file: 
            with open(file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)


    def connect(self, otp = False):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
            self.cursor_alt = self.conexion.cursor(buffered=True)
        except Exception as error:
            print(error)
        else:
            if otp: print('Connected to database')
        
    def disconnect(self, otp = False):
        self.conexion.close()
        if otp: print('Disconnected from database')

    def commit(self, sql):
        self.cursor.execute(sql)
        self.conexion.commit()

    def get(self, sql):

        self.cursor_alt.execute(sql)
        return self.cursor_alt.fetchall()

    #? PRIVATE FUNCTIONS
    def add_user(self, id):
        self.commit(fr"INSERT INTO `discord` (`index`, `id`, `character_id`, `delete_message`, `color`) VALUES (NULL, '{id}', NULL, '0', '$bot.color');")

    def check_user(self, id):
        if len(self.get(fr"SELECT * FROM `discord` WHERE `id` LIKE '{id}'")) > 0:
            return True
        else: return False
    
    def get_user(self, id): return self.get(fr"SELECT * FROM `discord` WHERE `id` LIKE '{id}'")

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

#? Commands
@commands.command()
async def wa(ctx, command = 'help', *, args = None):

    #?Check if discord user on database, if not add the user
    if not bot.db.check_user(ctx.author.id):
        bot.db.add_user(ctx.author.id)
    else: print('User in DB')
    #?Check if player wants to delete message
    if bot.db.get_user(ctx.author.id)[0][3] == 1: await ctx.message.delete()


    # SELECT * FROM `discord` WHERE `id` LIKE '000000000000000000'
    # INSERT INTO `discord` (`index`, `id`, `character_id`, `delete_message`, `color`) VALUES (NULL, '000000000000000000', NULL, '0', '$bot.color');

    match command.lower():
        #* Interacciones personaje
        case 'register': pass #await character.register(bot,ctx,args)
        case 'delete_profile': pass #await character.delete_profile(bot,ctx,args)
        case 'profile': pass #await character.profile(bot, ctx,args)
        case 'inventory': pass #await character.inventory(bot,ctx,args)
        case 'config': await character.config(bot, ctx, args)

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
        