#Selenne Stable Version
#By DCS Network

import discord
from discord.ext import commands
import json
import asyncio

#Internal
import config

#Logging System
with open('bot.log', 'r') as f: oldlog = f.read()
with open('db/old_logs.log', 'a') as f: f.write(oldlog)
import logging
logging.basicConfig(filename='bot.log', filemode='w', encoding = 'utf8', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=config.log)


class Selenne(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX), #https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.when_mentioned_or
            description = config.version,
            activity = discord.Game(name = config.activity),
            status = config.status,
            intents=intents
            )

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        try:
            self.pid = await self.fetch_user(000000000000000000)
        except: logging.warning('Error while fetching owner')
        try:
            m = await self.pid.send('Ya vuelvo a estar conectada')
            await asyncio.sleep(5)
            await m.delete()
        except: logging.warning('Error while sending message to owner')

bot = Selenne()
bot.remove_command('help')

#Universal Vars
bot.version = config.version
bot.nullchar = '\u200b'
bot.owner = config.owner
bot.color = config.color
bot.colours = config.colours
bot.developers = config.developers

#Check if works
bot.log = logging

#SetUp
@bot.event
async def setup_hook():
    
    #Load Extensions Manager
    try:
        await bot.load_extension('extension.manager')
    except: 
        logging.critical('Error while loading Extensions Manager')
        await bot.stop()
    
    with open('startup_extensions.cfg', 'r') as f:
        startup_extensions = f.readlines()
        for extension in startup_extensions:
            l = extension.removesuffix('\n')
            try:
                await bot.load_extension(f'{l}')
            except Exception as error:
                logging.error(f'{l} failed to load: {error}')
    

    #Reload Buttons
    pass

#Run
logging.info('Bot start')
bot.run(config.TOCKEN)
