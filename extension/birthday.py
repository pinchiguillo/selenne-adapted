import discord
from discord.ext import commands
import json

import datetime
import asyncio

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

    global extension_help
    
    extension_help = {
        'general_display': 's.check',
        'specific_display': {
            's.check': 'checks'
            }
        }

    add_help()

    #ADD CMD
    bot.add_command(check)


def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

bot_version = 'Selenne 4.8.5'
version = 'Birthday_Alerts: Beta'
ename = 'Birthday Alerts'

db_path = 'db/bd.json'

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
async def check(ctx, args = None):
    if not ctx.author.id == bot.owner: return

    await ctx.message.reply('Checking Started')
    bd = datetime.datetime(2022,1,1,0, 0)
    while True:
        await asyncio.sleep(1)
        if (bd - datetime.datetime.now()) <= datetime.timedelta(seconds = 0):
            break
    usr = await bot.fetch_user(bot.owner)
    await usr.send('Feliz Cumpleaños!')
