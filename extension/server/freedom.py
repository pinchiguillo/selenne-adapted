import discord
from discord.ext import commands

from discord.ext import tasks
import discord.utils as utils

import asyncio

import datetime

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'{__name__} loaded')

    #freedom_kick.start()
    bot.add_command(test)

def teardown(bot):
    bot.log.info(f'{__name__} unloaded')
    freedom_kick.stop()

server_id = 839310820755243018

@tasks.loop(time=datetime.time(0))
async def freedom_kick():
    pass

@commands.command()
async def test(ctx):
    guild = bot.fetch_guild(913949547514974249)
    role = await utils.get(discord.role, name = 'nuevo rol')
    await ctx.send(role.mention)