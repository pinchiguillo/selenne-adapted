import discord
from discord.ext import commands

import json
import datetime

async def setup(b):
    global bot
    bot = b
    
    bot.add_listener(on_message)
    bot.add_command(afkm)
    bot.add_listener(on_member_join)


version = 'AFKManager: Beta'
ename = 'Default'

db_path = 'db/afkmanager.json'

@commands.command()
@commands.has_permissions(administrator=True)
async def afkm(ctx, args = 'help'):
    await afkcore(ctx=ctx, args=args)

@commands.Cog.listener()
async def on_message(message):
    if not message.guild:
        return
    with open(db_path, 'r') as f:
        db = json.load(f)
    try:
        db[str(message.guild.id)]
    except KeyError:
        db[str(message.guild.id)] = {}
    db[str(message.guild.id)][str(message.author.id)] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    with open(db_path, 'w') as f:
        json.dump(db, f, indent=5)

@commands.Cog.listener()
async def on_member_join(member):
    with open(db_path, 'r') as f:
        db = json.load(f)
    try:
        db[str(member.guild.id)]
    except KeyError:
        db[str(member.guild.id)] = {}
    db[str(member.guild.id)][str(member.id)] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    with open(db_path, 'w') as f:
        json.dump(db, f, indent=5)


async def afkcore(ctx, args:str):
    if 'purge' in args:
        args = args.removeprefix('purge ')

        with open(db_path, 'r') as f:
            db = json.load(f)

        afktime = datetime.timedelta(days = int(args))
        
        for user in db[str(ctx.guild.id)]:
            if datetime.datetime.now() - datetime.datetime.strptime(db[str(ctx.guild.id)][user], '%d/%m/%Y %H:%M') > afktime:
                user = await ctx.guil.get_member(int(user))
                await user.send(f'You have been kicked from **{ctx.guild}** for being afk more than **{afktime}**')
                await user.kick(reason = f'Being afk for more than {afktime}')
    else:
        await ctx.send('**Wrong Syntax**')
    