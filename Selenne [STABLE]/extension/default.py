import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    
    bot.add_listener(on_message)

    bot.add_command(extension)

version = 'Default: 1.1'
ename = 'Default'

@commands.command()
async def extension(ctx, args = None):
    if ctx.author.id == bot.owner:
        if args == 'reload':
            try:
                await bot.reload_extension('')
                await ctx.send(f'**{ename}** reloaded')
            except:
                await ctx.send(f'Error while reloading {ename}. Try rebooting the whole bot')
        else:
            await ctx.send(f'Current Version: **{version}**')
    else:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')

@commands.Cog.listener()
async def on_message(message):
    print(message.content)

@commands.command()
async def ping(ctx):
    ctx.send('Pong')

@commands.command()
async def ex(ctx):
    if ctx.author.id in bot.developers:
        prt = None
        try:
            #

            await ctx.send('**Done**')
            if prt:
                await ctx.send(f'```{prt}```')
        except Exception as error:
            await ctx.send(f'```{error}```')
