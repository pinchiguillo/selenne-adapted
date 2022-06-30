import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(stats)
    bot.add_command(serverlist)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

bot_version = 'Selenne 4.8.6'
version = 'BotStats: 1.1'
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

@commands.command()
async def serverlist(ctx, args = None):
    if ctx.author.id in bot.developers:
        srvs = len(list(bot.guilds))
        embed = discord.Embed(title = 'Selenne Servers (OnlyStaff)', color = bot.color)
        embed.description = f'Selenne is in `{srvs}` different servers'
        for server in bot.guilds:
            embed.add_field(name = f'{server}', value = f'Owner: {server.owner.mention}\nMembers: `{len(server.members)}`\nChannels: `{len(server.channels)}`\nRoles: `{len(server.roles)}`', inline=True)

        
        await ctx.send(embed=embed)
    else:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')