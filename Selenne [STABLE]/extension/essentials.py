import discord
from discord.ext import commands

import os

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(ping)
    bot.add_command(bye)
    bot.add_command(reboot)
    bot.add_command(echo)
    bot.add_command(invite)
    bot.add_command(clear)


version = 'Essentials: Beta'
ename = 'Essentials'
    
@commands.command()
async def ping(ctx):
    if ctx.author.id in bot.developers:
        await ctx.send('Pong')    

@commands.command()
async def bye(ctx):
    if ctx.author.id in bot.developers:
        await ctx.reply('bye!')
        exit()

@commands.command()
async def reboot(ctx):
    if ctx.author.id in bot.developers:
        await ctx.reply('Rebooting bot...')
        os.system('start /min bot.bat')
        exit()

@commands.command()
@commands.has_permissions(administrator=True)
async def echo(ctx, *, args):
    await ctx.send(args)

@commands.command() # OUTDATED
async def invite(ctx):
    await ctx.send('Not Reloaded')

@commands.command()
async def clear(ctx, ammount = 10000):
	await ctx.channel.purge(limit = ammount)
