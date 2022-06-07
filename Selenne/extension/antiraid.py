import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

    global extension_help
    
    extension_help = {
        'general_display': 'cmd',
        'specific_display': {
            'cmd': 'use'
            }
        }

    add_help()

    #ADD CMD

    bot.add_command(extension)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

bot_version = 'Selenne 4.8.5'
version = 'AntiRaid: Alfa'
ename = 'Anti Raid'

db_path = 'db/antiraid.json'

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)

def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)
def save_db(db:dict):
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5)

@commands.command()
async def extension(ctx, args = None):
    if ctx.author.id == bot.owner:
        if args == 'reload':
            try:
                await bot.reload_extension('')
                await ctx.send(f'**{ename}** reloaded')
            except:
                await ctx.send(f'Error while reloading {ename}. Try rebooting the whole bot')
        else:
            await ctx.send(f'Current Version: **{version}**')
    else:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')

@commands.Cog.listener()
async def on_guild_update(before, after):
    db = load_db()
@commands.Cog.listener()
async def on_guild_role_create(role):pass
@commands.Cog.listener()
async def on_guild_role_delete(role):pass
@commands.Cog.listener()
async def on_guild_role_update(before, after):pass
@commands.Cog.listener()
async def on_guild_channel_delete(channel):pass
@commands.Cog.listener()
async def on_guild_channel_create(channel):pass
@commands.Cog.listener()
async def on_guild_channel_update(before, after):pass


async def antiraid_core():
    pass

h = {
    "Extension":{
        "general_display": "cmd",
        "specific_display": {
            "cmd": "use"
        }
    }
}