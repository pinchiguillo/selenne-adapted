import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(log)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

bot_version = 'Selenne 4.8.5'
version = 'Logs: 1.0'

@commands.command()
async def log(ctx, args = None):
    if ctx.author.id in bot.developers:
        await ctx.send(file=discord.File('bot.log'))
    else: await ctx.send('You dont have permission to run this command')