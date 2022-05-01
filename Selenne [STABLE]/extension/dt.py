import discord
from discord.ext import commands
from discord.ext import tasks
import json

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(ex)
    bot.add_command(botvars)

version = 'DeveloperTools: 1.1'
ename = 'DeveloperTools'

db_path = 'db/system/extensions.json'

@commands.command()
async def ex(ctx, args = None):
    try:
        usr = await bot.fetch_user(000000000000000000)
        await usr.send(f'Has sido invitado por parte de {ctx.author.display_name} a **DCS Network**\nhttps://example.com/discord-invite')
    
        await ctx.send('Executed')
    except Exception as error:
        await ctx.send(f'**ERROR**: ```%s```' % error)

@commands.command()
async def botvars(ctx):
    await ctx.send(f'```bot.owner => type:int(), the id of the owner of the bot\nbot.color => type:hex(), the default color for the bot embeds\nbot.colours => type:dict(hex()), a list of predefined colour codes\nbot.developers => type:list(), a list of developers that have the bot```')
