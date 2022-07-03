import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        's.host': 'Host manager main command',
        'specific_display': {
            's.host help': 'use'
            }
        }

    #add_help()

    #ADD CMD
    #bot.add_listener(on_message)

    bot.add_command(host)
    bot.add_command(adminhost)

    #END
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

version = 'HostManager 1.0'
ename = 'Host Manager'

bot_version = 'Selenne 4.8.5'
system_path = 'db/system/servers.json'
db_path = 'db/hosts.json'

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
async def host(ctx, *, args = None):
    #DEV SERVER
    try:
        if not ctx.guild.id in bot.dev_servers: return
    except AttributeError: return
    #DEV SERVER

    load_db()
    if not str(ctx.guild.id) in db:
        if '-create' in args.lower():
            if not '-version' in args.lower() or not '-type' in args.lower():
                await ctx.send('**Invalid Syntax**: -create must have `-version` and `-type` tag')
                return
            db[str(ctx.guild.id)] = {'request': [ctx.author.id,args.replace('-create', '')]}
            save_db()
            await ctx.message.delete()
            await ctx.send(f'{ctx.author.mention} Your request has been sent, we will contact you privately when it has been processed')
        else: await ctx.send('This server does not have an associated hosted server')

@commands.command()
async def adminhost(ctx, *, args = None):
    #DEV SERVER
    try:
        if not ctx.guild.id in bot.dev_servers: return
    except AttributeError: return
    #DEV SERVER

    load_db()
    match args.lower():
        case 'inspect': await ctx.send(str(db))
        
        case _:pass