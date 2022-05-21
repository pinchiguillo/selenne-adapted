import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(log)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'Logs: 1.0'

@commands.command()
async def log(ctx, args = None):
    if ctx.author.id in bot.developers:
        await ctx.send(file=discord.File('bot.log'))
    else: await ctx.send('You dont have permission to run this command')