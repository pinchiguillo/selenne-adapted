import discord
from discord.ext import commands

import json
import datetime

async def setup(b):
    global bot
    bot = b
    
    bot.add_listener(on_message)


version = 'AFKManager: Alfa'
ename = 'Default'

db_path = 'db/afkmanager.json'

@commands.command()
async def afkm(ctx, args = None):
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
    with open(db_path, 'r') as f:
        db = json.load(f)
    db[str(message.guild.id)][str(message.author.id)] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    with open(db_path, 'w') as f:
        json.dump(db, f, indent=5)

@commands.command()
async def ping(ctx):
    ctx.send('Pong')
