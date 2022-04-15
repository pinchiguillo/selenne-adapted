import discord
from discord.ext import commands
import asyncio
import random

from dcs.functions import f_lib


async def setup(b):
    global bot
    bot = b
    bot.add_listener(on_message)

    bot.add_command(ai)

@commands.Cog.listener()
async def on_message(message):
    print(message.content)

@commands.command()
async def ai(ctx, *, args = None):
    if ctx.author.id == bot.owner:
        if not args:
            await ctx.send('Wrong Syntax')
        elif args == 'reload':
            msg = await ctx.send('Reloading AI model...')
            await bot.reload_extension('cog.Selenne')
            await msg.edit('AI model reloaded')
    else: 
        await ctx.send('You dont have permissions to use this command')
