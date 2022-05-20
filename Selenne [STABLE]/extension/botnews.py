import discord
from discord.ext import commands
from discord.ext import tasks
import json

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(bn)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'BotNews: 1.1'
ename = 'Default'

db_path = 'db/afkmanager.json'

@commands.command()
async def bn(ctx, args = None):
    if ctx.author.id == bot.owner:
        with open(db_path, 'r') as f:
            db = json.load(f)


    with open('news.txt', 'r') as f:
        news = f.read()

    db_keys = list(db.keys())

    for gld in db_keys:
        g_id = int(gld)
        guild = await bot.fetch_guild(g_id)
        ch = await guild.fetch_channel(db[gld])

        embed=discord.Embed(title = 'Novedade Selenne', description = news, color = bot.color)
        embed.set_footer(text = 'DCS | Equipo de desarrollo de Selenne')
        await ch.send(embed=embed)
