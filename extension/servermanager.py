import discord
from discord.ext import commands

import json

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')
    1
    bot.add_command(config)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

bot_version = 'Selenne 4.8.5'
version = 'ServerManager: 1.0.3'
db_path = 'db/system/servers.json'

@commands.command()
@commands.has_permissions(administrator=True)
async def config(ctx, *, args = 'display'):
    await ctx.message.delete()
    #Check if server in db
    with open(db_path, 'r') as f:
        full_db = json.load(f)
        try:
            db = full_db[str(ctx.guild.id)]
        except:
            db = {
                "channels": {
                    "news": False,
                    "reports": False,
                    "suggestions": False,
                    "logs": False
                },
                "settings": {
                    "color": False
          }
     }
        full_db[str(ctx.guild.id)] = db

    match args.split(' ')[0]:
        case 'display':
            embed = discord.Embed(title = 'Actual Selenne Config', color=bot.color)
            for channel in db["channels"]:
                if not db["channels"][channel]:
                    v = f'Use **s.config channel {channel}** to setup this channel'
                else:
                    
                    v = f'<#{db["channels"][channel]}>'
                
                embed.add_field(name = f'{channel.capitalize()} channel', value = v, inline=False)
            await ctx.send(embed=embed)
        case 'channel':
            db["channels"][args[2]] = ctx.channel.id
            await ctx.send(f'This channel has been setted up as {args} channel', delete_after = 5)
        
        case _:
            await ctx.send('**WRONG SYNTAX**', delete_after = 5)

    #Save
    with open(db_path, 'w') as f:
        json.dump(full_db, f, indent=5)
