import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b
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

version = 'AntiSpam: 1.1'
ename = 'Anti Spam'
db_path = 'db/antispam.json'

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
    content = message.content
    guild = message.guild #.id
    channel = message.channel #.id
    author = message.author #.id

    if message.author.bot:return
    if message.content.lower() in ['s.em']:return
    if message.author.id in bot.developers: return

    #Load DB
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    try:
        if message.content.lower() in db['last_message'][str(message.author.id)]["message"]:
            db['last_message'][str(message.author.id)]["times"] += 1
            if db['last_message'][str(message.author.id)]["times"] >= 5:
                await message.delete()
                await message.channel.send(f'{message.author.mention} Cuidado con el spam, te vigilo 👀', delete_after=30)
        else:
            db['last_message'][str(message.author.id)]["times"] = 1
            db['last_message'][str(message.author.id)]["message"].append(message.content.lower())
            if len(db['last_message'][str(message.author.id)]["message"]) >= 4:
                db['last_message'][str(message.author.id)]["message"].pop(0)
    except KeyError:
        db['last_message'][str(message.author.id)] = {"message": [message.content.lower()], "times": 1}

    
    #Save DB
    with open(db_path, 'w', encoding='utf8') as f:
        json.dump(db, f, indent=5)

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
