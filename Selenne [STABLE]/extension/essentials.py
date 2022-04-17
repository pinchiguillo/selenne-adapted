import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(essentials)


version = 'Essentials: Alfa'
ename = 'Essentials'

@commands.command()
async def essentials(ctx, mode = None, args = None):
    if mode == 'help':
        h = 'Cant Display Help'
        await ctx.send(h)
    else:
        await ctx.send('Use **s.essentials help** in order to get help')
