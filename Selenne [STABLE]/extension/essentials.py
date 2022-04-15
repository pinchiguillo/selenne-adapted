import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b

    bot.add_command(essentials)
    bot.add_command(load)
    bot.add_command(unload)

essentials_version = 'Essentials: 1.0'

@commands.command()
async def essentials(ctx, args = None):
    if ctx.author.id == bot.owner:
        if args == 'reload':
            try:
                await bot.reload_extension('extension.essentials')
                await ctx.send(f'**essentials** reloaded')
            except:
                await ctx.send(f'Error while reloading essentials. Try rebooting the whole bot')
        else:
            await ctx.send(f'Current Version: **{essentials_version}**')
    else:
        await ctx.send('YOU DONT HAVE PERMISSIONS TO DO THIS')

@commands.command()
async def load(ctx, extension):
    if ctx.author.id == bot.owner:
        try:
            await bot.load_extension(f'extension.{extension}')
            await ctx.send(f'**{extension}** loaded')
        except:
            await ctx.send(f'Error while loading **{extension}**')
    else:
        await ctx.send('YOU DONT HAVE PERMISSIONS TO DO THIS')      

@commands.command()
async def unload(ctx, extension):
    if ctx.author.id == bot.owner:
        try:
            await bot.unload_extension(f'extension.{extension}')
            await ctx.send(f'**{extension} unloaded**')
        except:
            await ctx.send(f'Error while unloading **{extension}**')
    else:
        await ctx.send('YOU DONT HAVE PERMISSIONS TO DO THIS')      

@commands.command()
async def extension(ctx, args = None):
    if ctx.author.id  == bot.owner:
        if args == 'load':
            pass
        elif args == 'unload':
            pass
        elif args == 'list':
            pass
