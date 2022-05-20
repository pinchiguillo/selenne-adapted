import discord
from discord.ext import commands

import json

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(config)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'ServerManager:Afla'
db_path = 'db/system/servers.json'

@commands.command()
@commands.has_permissions(administrator=True)
async def config(ctx, args = 'display'):
    help = 'Help Display'

    #Load Specific
    with open(db_path, 'r') as f:
        db = json.load(f)
        db = db[str(ctx.guild.id)]


    if args.lower() == 'display':
        embed = discord.Embed(title = 'Actual Selenne Config', color=bot.color)
        for channel in db["channels"]:
            if not db["channels"][channel]:
                v = f'Use **s.config {channel}** to setup this channel'
            else:
                v = db["channels"][channel]
        
            embed.add_field(name = f'{channel.capitalize()} channel', value = v, inline=False)

        await ctx.send(embed=embed)
