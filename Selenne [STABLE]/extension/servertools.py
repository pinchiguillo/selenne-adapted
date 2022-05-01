import discord
from discord.ext import commands

import json
import asyncio

async def setup(b):
    global bot
    bot = b

    bot.add_command(_anounce)
    bot.add_command(acls)

version = 'Default: 1.1'
ename = 'Default'

db_path = 'db/system/servers.json'

def get_settings(ctx):
    with open(db_path, 'r') as f:
        db = json.load(f)
        return db[str(ctx.guild.id)]
    

@commands.command()
@commands.has_permissions(administrator=True)
async def _anounce(ctx, *, args):
    print('CMD DETECTED')
    settings = get_settings(ctx)
    print('DATA COLECTED')
    #Get data
    try:
        newsch = int(settings["channels"]["news"])
    except:
        await ctx.send('You dont have a **News Channel** configured. Use **s.config** to configurate your server')
        return
    finally:
        ch = await bot.fetch_channel(newsch)
        embed=discord.Embed(title = '📢 Anuncio', description = str(args), color = bot.color)
        embed.set_author(name = ctx.guild)
        embed.set_thumbnail(url = ctx.guild.icon)
        #embed.add_field(name="a", value="a", inline=False)
        await ch.send('@everyone', embed=embed)


@commands.Cog.listener()
async def on_message(message):
    print(message.content)

@commands.command()
async def ping(ctx):
    ctx.send('Pong')

@commands.command()
async def acls(ctx):
    messages = await ctx.channel.purge(limit = 1000)
    msg = await ctx.send(f'{messages} Deleted')
    await asyncio.sleep(5)
    await msg.delete()
