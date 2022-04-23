import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    

    bot.add_command(dcs)

version = 'DCS: Alfa'
ename = 'DCS API'

@commands.command()
async def dcs(ctx, *, args = None):
    if ctx.author.id == bot.owner:
        if args.startswith('reload'):
            args = args.removeprefix('reload')

    else:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')

@commands.Cog.listener()
async def on_message(message):
    print(message.content)

@commands.command()
async def ping(ctx):
    ctx.send('Pong')
