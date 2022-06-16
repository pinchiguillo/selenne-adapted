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
    bot.add_command(help)
    bot.add_command(dhelp)
    
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
bot_version = 'Selenne 5.1'
version = '1.1'
name = 'Help'

_version = name.replace(' ', '.')
_version = f'{name.lower()}: {version}'

# Databases
db_type = '$json'
system_path = 'db/system/servers.json'
db_path = 'db/system/help.json'
def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        global db
        db =  json.load(f)
def save_db():
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5, ensure_ascii = False)

# HELP
extension_help = {
    'general_display': 's.help',
    'specific_display': {
        's.help [extension]': 'Displays specific help'
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
async def help(ctx, *, args = None):
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)
    
    #Load Help File
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)

    if not args:
        
        for key in db.keys():
            helpembed.add_field(name=key, value = db[key]['general_display'], inline=False)
        
    else:
        if db[args]['specific_display']:
            try:
                for key in db[args]['specific_display'].keys():
                    helpembed.add_field(name=key, value = db[args]['specific_display'][key], inline=False)
            
            except:
                helpembed.description = 'Cant found that extension'
        else: helpembed.description = f'{args} Doesnt have specific help'


    await ctx.send(embed=helpembed)

@commands.command()
async def dhelp(ctx, args = None):
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)
    if ctx.author.id in bot.developers:
        if not args:
            helpembed.add_field(name = 'Docs', value = '[CLick on me!](https://discordpy.readthedocs.io/en/stable/)', inline=False)
            helpembed.add_field(name = 'Install', value = 'pip install -U git+https://github.com/Rapptz/discord.py', inline=False)
            helpembed.add_field(name = 'Required Extensions', value = 'discord.py 2.0, youtube_dl, PyNaCl', inline=False)
            helpembed.add_field(name = 'Commands Build-In Checks', value = '[CLick on me!](https://discordpy.readthedocs.io/en/stable/)', inline=False)
            helpembed.add_field(name = 'Mentions', value = 'nickname: `<@​​!{id}>`\nrole: `<@​&{id}>`\nchannel: `<#{id}}`\n`@​everyone`\n`@​here`', inline=False)
            helpembed.add_field(name = 'HyperLiks', value = '''"`[Text To Click](https://www.youtube.com/ \"Hovertext\")`"
- Needs to be a full url (http/https)
- Hovertext is optional
- If sent by a bot/user it needs to be in an embed
- If sent in a webhook you can hyperlink raw text cuz fuck being consistent amirite discord
- This only works in the embed description and field value
If you want to hyperlink a title or set_author, you can use the url kwarg''', inline=False)
            helpembed.add_field(name = 'Text Formats', value = '[CLick on me!](https://wikitechnews.net/una-guia-completa-sobre-el-formato-de-texto-de-discord-tachado-negrita-y-mas/)', inline=False)
            helpembed.add_field(name = 'Custom Emogi', value = '```\[custom emogi]```', inline=False)
            helpembed.add_field(name = 'Snowflake Date', value = '[Creation Date](https://snowsta.mp/)', inline=False)
            helpembed.add_field(name = 'Extra', value = '```exec(\'print Hello World\')\neval(\'1 + 1\')```', inline=False)
    else:
        helpembed.description = 'Only Verifyed Selenne Developers Commands'

    await ctx.send(embed=helpembed)


#! HELP NOT ADDED

'https://www.youtube.com/c/TechWithTim/playlists'
'https://www.upgrad.com/blog/how-to-make-chatbot-in-python/'
'https://www.youtube.com/watch?v=c_gXrw1RoKo'
