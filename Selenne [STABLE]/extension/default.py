import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    
    bot.add_listener(on_message)

    bot.add_command(ping)


@commands.Cog.listener()
async def on_message(message):
    print(message.content)

@commands.command()
async def ping(ctx):
    ctx.send('Pong')
