#Selenne Stable Version
#By DCS Network

import discord
from discord.ext import commands
import json
import asyncio
import os

#Internal
import config

#Logging System
with open('bot.log', 'r') as f: oldlog = f.read()
with open('db/old_logs.log', 'a') as f: f.write(oldlog)
import logging
logging.basicConfig(filename='bot.log', filemode='w', encoding = 'utf8', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=config.log)

async def get_prefix(bot, message):
  return 's.'  # or a list, ["pre1","pre2"]

#! Selene Core 2.1 By pinchiguillo
class Selenne(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        #!DO NOT TOUCH ANYTHING, config in config.py file
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX),
            description = config.description,
            activity = discord.Game(name = config.activity),
            status = config.status,
            intents=intents
            )

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        if config.warn_onready:
            try:
                self.pid = await self.fetch_user(000000000000000000)
            except: logging.warning('Error while fetching owner')
            try:
                m = await self.pid.send('Ya vuelvo a estar conectada')
                await asyncio.sleep(5)
                await m.delete()
            except: logging.warning('Error while sending message to owner')

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandNotFound): await ctx.send('Command Not Found, try using `s.help`', delete_after=10)

bot = Selenne()
bot.remove_command('help')

#! VERSION
bot.version = 'Selenne 5.1-PRE'
#Universal Vars
bot.nullchar = '\u200b'
bot.owner = config.owner
bot.color = config.color
bot.colours = config.colours
bot.developers = config.developers
bot.dev_servers = config.dev_servers
bot.bot_servers = config.bot_servers

bot.log = logging
bot.database = None

#SetUp
@bot.event
async def setup_hook():
    with open('db/system/startup.json', 'r', encoding='utf-8') as f:
        startup_data = json.load(f)

    #! Extensions
    #Systematic
    for extension in startup_data['extensions']['systematic']:
        try:
            await bot.load_extension(extension)
        except Exception as error:
            logging.critical(f'Error while loading {extension}: {error}')
            await bot.stop()

    #Normal
    for extension in startup_data['extensions']['normal']:
        try:
            await bot.load_extension(f'{extension}')
        except Exception as error:
            logging.error(f'{extension} failed to load: {error}')
    

    #Reload Buttons
    pass

#Essentials Commands
@bot.command()
async def bye(ctx):
    if ctx.author.id == bot.owner:
        await ctx.reply('bye!')
        bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot the bot')
        await bot.close()

@bot.command()
async def off(ctx):
    if ctx.author.id == bot.owner:
        await ctx.reply('bye!')
        bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot the bot')
        await bot.close()

@bot.command()
async def reboot(ctx):
    if ctx.author.id in bot.developers:
        await ctx.reply('Rebooting bot...')
        os.system('start /min bot.bat')
        bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Rebooted the bot the bot')
        await bot.close()

#Run
logging.info('Bot start')
bot.run(config.TOCKEN)

exit()
