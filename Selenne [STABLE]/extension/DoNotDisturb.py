import discord
from discord.ext import commands

import json
import datetime

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_listener(on_message)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'DoNotDisturb: 1.0'
ename = 'Do Not Disturb'

db_path = 'db/DoNotDisturb.json'

@commands.Cog.listener()
async def on_message(message):
    if message.author.bot:
        return
    pinchi = await bot.fetch_user(bot.owner)
    if 'pinchi' in message.content.lower() or 'pinchiguillo' in message.content.lower() or '000000000000000000' in message.content:
        await message.reply(f'Actualmente {pinchi.mention} no esta disponible, cuando este disponible le avisare para que te resonda.', delete_after=15)
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
        except:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            with open(db_path, 'r', encoding='utf-8') as f:
                db = json.load(f)

        try:
            db[f'{message.author.display_name}:{message.author.id}'][str(datetime.datetime.now())] = message.content
        except KeyError:
            db[f'{message.author.display_name}:{message.author.id}'] = {}
            db[f'{message.author.display_name}:{message.author.id}'][str(datetime.datetime.now())] = message.content

        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4)