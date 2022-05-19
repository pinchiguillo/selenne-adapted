import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b

    bot.add_command(help)
    bot.add_command(adminhelp)
    bot.add_command(developerhelp)

    global helpembed
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)

version = 'Help: Alfa'
ename = 'Help'


@commands.command()
async def help(ctx, args = None):
    await ctx.send(embed=helpembed)

@commands.command()
async def adminhelp(ctx, args = None):
    await ctx.send(embed=helpembed)

@commands.command()
async def developerhelp(ctx, args = None):
    helpembed.description = 'Only Verifyed Selenne Developers Commands'
    helpembed.add_field(name = '```s.reboot```', value = 'Reboots the whole bot')

    await ctx.send(embed=helpembed)
