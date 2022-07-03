import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b

    #? StartUp Functions
    
    # Load Help
    add_help()

    # Add CMD
    bot.add_command(em)
    
    #? Add Listener
    #bot.add_listener(on_message)

    #? Check Bot Version and Log
    bv = list(bot.version)
    b_v = list(bot_version)
    if b_v[8:11] != bv[8:11]: bot.log.warning(f'extension.{_version.lower()} outdated')
    bot.log.info(f'extension.{_version.lower()} loaded')
def teardown(bot):
    bot.log.info(f'extension.{_version.lower()} unloaded')
    remove_help()

# Extension Data
bot_version = 'Selenne 5.1-PRE'
version = '2.4.1'
name = 'Extensions Manager'

_version = name.replace(' ', '.')
_version = f'{name.lower()}: {version}'

# Databases
db_type = '$json'
system_path = 'db/system/servers.json'
db_path = 'db/system/startup.json'
def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        global db
        db =  json.load(f)
def save_db():
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5, ensure_ascii = False)

# HELP
extension_help = {
    'general_display': 's.em',
    'specific_display': {
        's.em reload [extension]': 'Reloads an extension, if use -last reloads the last extension loaded',
        's.em display': 'Displays all the active extensions',
        's.em load [extension]': 'Loads an extension',
        's.em unload [extension]': 'Unloads an extension',
        's.em version': 'Displays Extensions Manager Current Version',
        's.em startup -add [extension]': 'Adds the extension to the startup list',
        's.em startup -remove [extension]': 'Removes the extension to the startup list',
        's.em startup -display': 'Displays the startup list'
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
def server_db(ctx, mode = 'load', database = None):
    if mode == 'load':
        with open(system_path, 'r', encoding='utf-8') as f:
            _db=  json.load(f)
            return _db[str(ctx.guid.id)]
    elif mode == 'unload':
        with open(system_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=5, ensure_ascii = False)


# Commands
@commands.command()
async def em(ctx, mode = None, *, args = 'manager'):
    #Check if autoriced
    if not ctx.author.id in bot.developers:
        await ctx.send('You are not autoriced')
        return

    #Loads Startup Data
    load_db()

    #Pre preate embed
    embed = embed=discord.Embed(title = 'Extensions Manager', color=bot.color)

    #! Mode Selector
    match mode.lower():
        case 'reload':
            #Find last extension loaded
            if not args:
                args = 'manager'
            elif args in ['-last', 'last','-l', 'l']:
                if bot.last_load:
                    args = bot.last_load
                else: embed.description = 'No last load saved'

            #Main
            try:
                await bot.reload_extension(f'extension.{args}')
                bot.last_load = args
                embed.description = f'**{args}** reloaded'
            except Exception as error:
                embed.description = f'Error while reloading **{name}**\n```{error}```'

        case 'display':
            extensions = ''            
            for extension in list(bot.extensions):
                tmp = extension.removeprefix('extension.').capitalize()
                extensions += f'\n- {tmp}'
            
            embed.description = extensions
        
        case 'load':
            try:
                #Load Extension
                await bot.load_extension(f'extension.{args}')
                
                #Dysplay Msg
                embed.description = f'**{args}** loaded'
                
                bot.last_load = args
            except Exception as error:
                embed.description = f'Error while loading **{args}**\n```{error}```'

        case 'unload':
            if f'extension.{args}' in db['extensions']['systematic']:
                embed.description = f'***{args}*** **cant be unloaded**'
            else:
                try:
                    #Unload Extension
                    await bot.unload_extension(f'extension.{args}')

                    #Dysplay msg
                    embed.description = f'**{args}** unloaded'
                    
                except Exception as error:
                    embed.description = f'Error while unloading **{args}**\n```{error}```'

        case 'help': await ctx.send('ERROR While sending help, use `s.help Extensions Manager`') #! Requires extension.help update
        case 'version' | 'v': embed.description = f'Current version: **{name}: {version}**'
        case 'startup':
            args = list(args.split(' '))
            match args[0].removeprefix('-'):
                case 'add':
                    #Comprobar si exsite la extension
                    if not f'extension.{args[1]}' in db['extensions']['systematic'] and not f'extension.{args[1]}' in db['extensions']['normal']:
                        #Intentar cargar extension
                        try:
                            await bot.load_extension(f'extension.{args[1]}')
                            db['extensions']['normal'].append(f'extension.{args[1]}')
                            save_db()

                            #Dysplay msg and log
                            embed.description = f'**{args[1]}** successfully added to startup'
                            bot.log.info(f'extension.{args[1]} added to startup')
                        except Exception as error:
                            embed.description = f'**Unable to load extension**:\n```{error}```\nCheck if the extension is unloaded or if the extension loads via **s.em load**'
                            
                            bot.log.error(f'while adding extension.{args[1]} to startup ERROR: {error}')
                    else: 
                        embed.description = f'{args[1]} alrready in startup'
                    
                case 'remove':
                    #Comprobar si exsite la extension
                    if f'extension.{args[1]}' in db['extensions']['normal']:
                        #Intentar descargar cargar extension
                        try:
                            try:
                                await bot.unload_extension(f'extension.{args[1]}')
                            except:pass
                            
                            db['extensions']['normal'].pop(db['extensions']['normal'].index(f'extension.{args[1]}'))
                            save_db()

                            #Dysplay msg and log
                            embed.description = f'**{args[1]}** successfully removed from startup'
                            bot.log.info(f'extension.{args[1]} removed form startup')
                        except Exception as error:
                            embed.description = f'**Unable to remove extension from startup**:\n```{error}```'
                            
                            bot.log.error(f'while removing extension.{args[1]} to startup ERROR: {error}')
                    else: 
                        embed.description = f'{args[1]} not in startup'
                case _: embed.description = 'Wrong Syntax'

        case _: 
            embed.description = 'Wrong Syntax, try using `s.help Extensions Manager`'

    #Send embed to discord
    try:
        await ctx.send(embed=embed)
    except:
        bot.log.critical(f'WHILE GENERATING EMBED:{embed.description}')
        embed.description = 'Error while sending embed, content saved to log'
        await ctx.send(embed=embed)
