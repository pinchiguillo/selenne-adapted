import discord
from discord.ext import commands

import os
import json

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

    global extension_help
    
    extension_help = {
        'general_display': 'use **s.help Essentials** for more info',
        'specific_display': {
            's.ping': 'Makes Selenne send a message back (Only Developers)',
            's.bye': 'Shutdowns Selenne (Only Onwer)',
            's.reboot': 'Reboots Selenne (Only Developers)',
            's.echo [message]': 'Makes Selenne send the message back (Only Administrators)',
            's.invite [link]': 'Sends a saved invitation, if a link is given saves that link as the server invitation (Saving only for Administrators)',
            's.clear [amount]': 'Deletes an especific amount of messages, by default 10000 (Only Administrators)'
            }
        }

    add_help()

    #ADD CMD
    bot.add_command(ping)
    bot.add_command(bye)
    bot.add_command(reboot)
    bot.add_command(echo)
    bot.add_command(invite)
    bot.add_command(clear)


def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

bot_version = 'Selenne 4.8.6'
version = 'Essentials: 1.2'
ename = 'Essentials'

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)

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
@commands.has_permissions(administrator=True)
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
