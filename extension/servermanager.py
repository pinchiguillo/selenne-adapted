import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b

    #! StartUp
    
    # Load Help
    add_help()

    # Add CMD
    bot.add_command(config)
    
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

# Extension Data
bot_version = 'Selenne 5.0'
version = '1.0.3'
name = 'ServerManager'

_version = name.replace(' ', '.')
_version = f'{name.lower()}: {version}'

# Databases
db_type = '$sql'
system_path = 'db/system/servers.json'
db_path = system_path
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

# HELP
extension_help = {
    'general_display': 's.config',
    'specific_display': {
        's.config': 'Displays current server config',
        's.config channel [channel]': 'Sets up the current channel as [channel]'
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

# Commands
@commands.command()
@commands.has_permissions(administrator=True)
async def config(ctx, *, args = 'display'):
    await ctx.message.delete()
    
    #Get data from DB
    print('PRE DATA')
    print(bot.database)
    bot.database.insert({'id': 913949547514974249, 'channels': {}, 'settings': {}}, otp=True)
    print(config)

    if not config:
        bot.database.insert({'id': ctx.guild.id, "channels": {"news": False,"reports": False,"suggestions": False,"logs": False}, "settings": {"color": False}}, otp=True)

    match args.split(' ')[0]:
        case 'display':
            embed = discord.Embed(title = 'Actual Selenne Config', color=bot.color)
            for channel in db["channels"]:
                if not db["channels"][channel]:
                    v = f'Use **s.config channel {channel}** to setup this channel'
                else:
                    
                    v = f'<#{db["channels"][channel]}>'
                
                embed.add_field(name = f'{channel.capitalize()} channel', value = v, inline=False)
            await ctx.send(embed=embed)
        case 'channel':
            db["channels"][args[2]] = ctx.channel.id
            await ctx.send(f'This channel has been setted up as {args} channel', delete_after = 5)
        
        case _:
            await ctx.send('**WRONG SYNTAX**', delete_after = 5)

    #Save
    with open(db_path, 'w') as f:
        json.dump(full_db, f, indent=5)
