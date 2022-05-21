import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(help)
    bot.add_command(adminhelp)
    bot.add_command(developerhelp)

    global helpembed
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

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



#Developers help: 
'https://gist.github.com/Painezor/eb2519022cd2c907b56624105f94b190'