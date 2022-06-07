import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(stats)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

bot_version = 'Selenne 4.8.6'
version = 'BotStats: 1.0'
ename = 'Bot Stats'

@commands.command()
async def stats(ctx, args = None):
    if ctx.author.id in bot.developers:
        srvs = len(list(bot.guilds))
        usrs = len(list(bot.users))
        
        owner = await bot.fetch_user(bot.owner)
        developers = len(bot.developers)
        st = f'Selenne es un bot creado por **{owner.display_name}**.\nActualmente esta siendo desarrollado por **{developers}** personas\n{bot.nullchar}'

        embed=discord.Embed(title = 'Selenne Stats', description = st, color=bot.color)
        embed.add_field(name = 'Servers', value = srvs, inline = True)
        embed.add_field(name = 'Users', value = usrs, inline = True)
        await ctx.send(embed=embed)
    else:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')

