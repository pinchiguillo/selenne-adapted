import discord
from discord.ext import commands

import json

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(ml)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'MyList: Alfa:1'
ename = 'MyList'

db_path = 'db/mylist.json'

@commands.command()
async def ml(ctx, mode = 'help', l = None, args = None):
    help = 'No Help'
    
    user = ctx.author.id

    with open (db_path, 'w') as f:
        db = json.load(f)

    

    if mode == 'add':
        pass
    elif mode == 'remove':
        pass
    elif mode == 'sow' or mode == 'display':
        pass
    elif mode == 'help':
        await ctx.send(help)
    else:
        await ctx.send(f'Wrong Syntax\n{help}')
