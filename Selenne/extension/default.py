import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': 'cmd',
        'specific_display': {
            'cmd': 'use'
            }
        }

    #add_help()

    #ADD CMD
    #bot.add_listener(on_message)

    #bot.add_command(extension)

    #END
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

version = 'servertools: Alfa'
ename = 'Server Tools'

bot_version = 'Selenne 4.8.5'
system_path = 'db/system/servers.json'
db_path = system_path

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
        json.dump(help_list, f, indent=5, ensure_ascii= False)

def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        global db
        db =  json.load(f)
def save_db():
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5, ensure_ascii = False)

@commands.command()
async def extension(ctx, args = None):
    #DEV SERVER
    try:
        if not ctx.guild.id in bot.dev_servers: return
    except AttributeError: return
    #DEV SERVER

@commands.Cog.listener()
async def on_message(message):
    #DEV SERVER
    try:
        if not message.guild.id in bot.dev_servers: return
    except AttributeError: return
    #DEV SERVER
