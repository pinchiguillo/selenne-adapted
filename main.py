#
#TODO: Selenne Stable Version
#TODO: By DCS Network

#?
import discord
from discord.ext import commands
import json
import asyncio
import os

#?Internal
import config

#? Selene Core 2.1.3 By pinchiguillo
class Selenne(commands.Bot):
    
    #!DO NOT TOUCH ANYTHING, config in config.py file

    version = 'Selenne 5.2-PRE'
    core_version = '2.1.3_BETA'
    building = True
    #_TOCKEN_LOCK = False
    async def set_prefix(self, bot, message): return config.PREFIX
    def __init__(self):

        super().__init__(
            command_prefix=self.set_prefix,
            description = config.description,
            activity = discord.Game(name = config.activity),
            status = config.status,
            intents=discord.Intents.all()
            )
        #? Universal Vars

        #self.TOCKEN = config.TOCKEN
        self._staff_file = open(config.staff_file, 'r+', encoding='utf-8')
        self.staff = json.load(self._staff_file)
        self.nullchar = '\u200b'
        self.owner = self.staff['owner']
        self.color = config.color
        self.colours = config.colours
        
        self.developers = self.staff['developers'].append(self.owner)
        self.dev_servers = self.staff['dev_servers']
        self.bot_servers = self.staff['bot_servers']

        #? Logging Engine
        import logging
        self.save_log()
        logging.basicConfig(filename='bot.log', filemode='w', encoding = 'utf8', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=config.log)
        self.log = logging

        #? Databases Engine - SQLtools 1.2
        from dcs.sqltools import DataBase
        self.database = DataBase(config.SQL)

        #? Extra config
        self.remove_command('help') #* extension.help

        #! Lock building vars (False is True)
        self.building = False
        self._TOCKEN_LOCK = True

    #? Essential Bot Commands
    
    #? Internal Functions
    def save_log(self):
        with open('bot.log', 'r') as f: oldlog = f.read()
        with open('db/old_logs.log', 'a') as f: f.write(oldlog)

    #?Setup
    async def setup_hook(self):
        with open('db/system/startup.json', 'r', encoding='utf-8') as f:
            startup_data = json.load(f)
        
        #? Core Commands Load
        class cmd_core(commands.Cog):
            def __init__(self, bot):
                self.bot = bot

            @commands.command()
            async def bye(self, ctx):
                if ctx.author.id == self.bot.owner:
                    await ctx.reply('bye!')
                    self.bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot the bot')
                    await self.bot.close()
            
            @commands.command()
            async def off(self, ctx):
                if ctx.author.id == self.bot.owner:
                    await ctx.reply('bye!')
                    self.bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot the bot')
                    await self.bot.close()

            @commands.command()
            async def reboot(self, ctx):
                if ctx.author.id in self.bot.developers:
                    await ctx.reply('Rebooting bot...')
                    os.system('start /min bot.bat')
                    self.bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Rebooted the bot the bot')
                    await self.bot.close()
        try:
            await self.add_cog(cmd_core(self))
            self.log.info(f'cmd_core loaded')
        except Exception as error:
            self.log.critical(f'While loading cmd_core: {error}')

        #? Startup extensions loader


        #* Systematic
        for extension in startup_data['extensions']['systematic']:
            try:
                await self.load_extension(extension)
            except Exception as error:
                self.log.critical(f'Error while loading {extension}: {error}')
                await self.stop()

        #* Normal
        for extension in startup_data['extensions']['normal']:
            try:
                await self.load_extension(f'{extension}')
            except Exception as error:
                self.log.error(f'{extension} failed to load: {error}')

    async def on_ready(self):
        self.log.info(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        if config.warn_onready:
            try:
                self.pid = await self.fetch_user(000000000000000000)
            except: self.log.warning('Error while fetching owner')
            try:
                m = await self.pid.send('Ya vuelvo a estar conectada')
                await asyncio.sleep(5)
                await m.delete()
            except: self.log.warning('Error while sending message to owner')

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandNotFound): await ctx.send('Command Not Found, try using `s.help`', delete_after=10)
    
    #? Var protection
    @property
    def owner(self): return self._owner
    @owner.setter
    def owner(self, value):
        if self.building: self._owner = value
        else: self._owner = self._owner

    @property
    def color(self): return self._color
    @color.setter
    def color(self, value):
        if self.building: self._color = value
        else: self._color = self._color

    @property
    def staff(self): return self._staff
    @staff.setter
    def staff(self, value):
        if not isinstance(value, dict): raise ValueError('the \'Selenne.staff\' must be \'dict\'')
        if not self.building:
            self._staff = value
            json.dump(self._staff, self._staff_file, indent=4)
        else:
            self._staff = value
 
#! Run
Selenne().run(config.TOCKEN)

exit()
