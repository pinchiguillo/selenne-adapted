import discord
from discord.ext import commands
from discord.ext import tasks
import json

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(ex)

version = 'DeveloperTools: 1.1'
ename = 'DeveloperTools'

db_path = 'db/system/extensions.json'

@commands.command()
async def ex(ctx, args = None):
    try:
    
        await ctx.send(len(bot.users))
    
        await ctx.send('Executed')
    except Exception as error:
        await ctx.send(f'**ERROR**: ```%s```' % error)