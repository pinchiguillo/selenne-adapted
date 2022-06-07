import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b
    f bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
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
    bot.add_listener(on_message)

    bot.add_command(extension)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

version = 'Default: 1.1'
ename = 'Default'

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
async def on_message(message):
    print(message.content)

@commands.command()
async def ping(ctx):
    ctx.send('Pong')

@commands.command()
async def ex(ctx):
    if ctx.author.id in bot.developers:
        prt = None
        try:
            #

            await ctx.send('**Done**')
            if prt:
                await ctx.send(f'```{prt}```')
        except Exception as error:
            await ctx.send(f'```{error}```')


h = {
    "Extension":{
        "general_display": "cmd",
        "specific_display": {
            "cmd": "use"
        }
    }
}