import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': 's.dcs',
        'specific_display': {
            's.dcs report [Cause]': 'Reports to DCS an issue (only avilable on specific guilds)'
            }
        }

    #add_help()

    #ADD CMD

    bot.add_command(dcs)

    #END
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

bot_version = 'Selenne 4.8.5'
version = 'dcs.network: Beta'
ename = 'DCS Network'

db_path = 'db/DCSN.json'

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)

def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)
def save_db(db:dict):
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5)

@commands.command()
async def dcs(ctx, mode = None, *, args:str):
    if not args:
        await ctx.send('Wrong Syntax')
        return
    db = load_db()
    await ctx.message.delete()
    owner = await bot.fetch_user(bot.owner)
    match mode.lower():
        case 'report':
            try:
                db['reports'][str(ctx.guild.id)][str(ctx.author.id)]['report'].append(args)
                await ctx.send('Report submitted', delete_after=10)
                await owner.send('You have a new report')
            except KeyError:
                try:
                    db['reports'][str(ctx.guild.id)][str(ctx.author.id)] = {'name':str(ctx.author), 'report':[args]}
                    await ctx.send('Report submitted', delete_after=10)
                    await owner.send('You have a new report')
                except KeyError:
                    await ctx.send('Your Guild does not have DCS support', delete_after=10)
            save_db(db)
        
        case _:
            await ctx.send('Wrong Arguments', delete_after=10)
