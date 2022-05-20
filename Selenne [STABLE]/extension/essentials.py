import discord
from discord.ext import commands

import os
import json

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(ping)
    bot.add_command(bye)
    bot.add_command(reboot)
    bot.add_command(echo)
    bot.add_command(invite)
    bot.add_command(clear)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'Essentials: 1.2'
ename = 'Essentials'
    
@commands.command()
async def ping(ctx):
    if ctx.author.id in bot.developers:
        await ctx.send('Pong')    

@commands.command()
async def bye(ctx):
    if ctx.author.id in bot.developers:
        await ctx.reply('bye!')
        bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot the bot')
        await bot.close()

@commands.command()
async def reboot(ctx):
    if ctx.author.id in bot.developers:
        await ctx.reply('Rebooting bot...')
        os.system('start /min bot.bat')
        bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Rebooted the bot the bot')
        await bot.close()

@commands.command()
#@commands.has_permissions(administrator=True)
async def echo(ctx, *, args):
    await ctx.send(args)

@commands.command() # OUTDATED
async def invite(ctx, args = None):
    with open('db/invitations.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    if args and ctx.author.id in bot.developers:
        db[str(ctx.guild.id)] = args
        with open('db/invitations.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=5)
        await ctx.send('Invitation Saved')
        
    else:
        try:
            if db[str(ctx.guild.id)]: pass
            await ctx.send(str(db[str(ctx.guild.id)]))
        except:
            await ctx.send('Your Guild does not have an invitation use s.invite [invitation]')

@commands.command()
async def clear(ctx, ammount = 10000):
	await ctx.channel.purge(limit = ammount)
