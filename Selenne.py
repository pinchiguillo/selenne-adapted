import discord
from discord.ext import commands
import json
import asyncio
import os
import importlib
import sys

#? Module Related Data
VERSION = 'Selenne 5.2'
AUTHOR = 'pinchiguillo'
SUPPORT_SERVER = 'https://discord.gg'
GITHUB = 'https://github.com/pinchiguillo'
SPECS = '='*15 + '   Selenne Module Specifications   ' + '='*15 + f'\n\tVersion: {VERSION}' + f'\n\tAuthor: {AUTHOR}' + f'\n\tSupport Server: {SUPPORT_SERVER}' + f'\n\tGitHub: {GITHUB}' + '\n'

New_Future = f'='*15 + '   {VERSION} New Features   ' + '='*15 + '''
Added Extension class in order to make cleaner the buiding of the class
'''

Future_Updates = '='*15 + '   Selenne Future Updates   ' + '='*15 + '''
In future updates we will add a new function, "Selenne.Core.allowed(whitelist=False, blacklist=False)", it will make easy if a guild has access to an specific command
We are currently working on Slash Commands
We are currently working on Permanent Views
'''

class Core(commands.Bot):
    
    #!DO NOT TOUCH ANYTHING, config in config.py file

    version = VERSION
    core_version = '2.2'
    building = True
    import config
    #_TOCKEN_LOCK = False
    
    def __init__(self):
        #? Check all the bot files
        try:
            import config
            self.config = config
        except ImportError:
            exit()
        try: open('bot.log', 'r').read()
        except FileNotFoundError: pass

        async def set_prefix(bot, message): return config.PREFIX
        super().__init__(
            command_prefix=set_prefix,
            description = config.description,
            activity = discord.Game(name = config.activity),
            status = config.status,
            intents=discord.Intents.all()
            )
        #? Universal Vars

        try:
            self._staff_file = open(config.staff_file, 'r+', encoding='utf-8')
        except: 
            self._staff_file = {
                "owner": None,
                "developers": [],
                "dev_servers": [],
                "bot_servers": []
            }
            try: 
                with open(config.staff_file, 'w', encoding='utf-8') as f:
                    json.dump(self._staff_file, f, indent=4)

                self._staff_file = open(config.staff_file, 'r+', encoding='utf-8')
            except FileNotFoundError: raise FileNotFoundError(f'Selenne could not find "{config.staff_file}"')
            
        self.staff = json.load(self._staff_file)
        self.nullchar = '\u200b'
        self.owner = self.staff['owner']
        self.owner_id = self.owner
        self.color = config.color
        self.colours = config.colours
        
        
        self.developers = self.staff['developers'] + [self.staff['owner']] #! NOT PERFECT
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
        self.config_database = None #* extension.servermanager

        #! Lock building vars (False is True)
        self.building = False

    #? Essential Bot Commands
    class cmd_core(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.command()
        async def bye(self, ctx):
            if ctx.author.id == self.bot.owner:
                await ctx.reply('bye!')
                self.bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot')
                await self.bot.close()
            
        @commands.command()
        async def off(self, ctx):
            if ctx.author.id == self.bot.owner:
                await ctx.reply('bye!')
                self.bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Stoped the bot')
                await self.bot.close()

        @commands.command()
        async def reboot(self, ctx):
            if ctx.author.id in self.bot.developers:
                await ctx.reply('Rebooting bot...')
                os.system('start /min bot.bat')
                self.bot.log.critical(f'{ctx.author.display_name}({ctx.author.id}) Rebooted the bot the bot')
                await self.bot.close()

        @commands.command()
        async def version(self, ctx, args = '-bot'):
            match args.lower():
                case '-bot': await ctx.send(f'Bot current version: **{self.bot.version}**')
                case '-core': await ctx.send(f'Bot core current verison: **{self.bot.core_version}**')


    #! NOT BUILD
    class staff_management(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
        
        @commands.command()
        async def stafflist(self, ctx):
            await ctx.send(str(self.bot.developers))
        @commands.command()
        async def addstaff(self, ctx):
            await ctx.send(f'addstaff function is not built in `{self.bot.core_version}`')
        @commands.command()
        async def removestaff(self, ctx):
            await ctx.send(f'remove function is not built in `{self.bot.core_version}`')

    #! NOT BUILD - ERROR OTP
    class developer_management(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
        
        @commands.command()
        async def devserver(self, ctx, args = '-list'):
            await ctx.send('**ERROR** while tying to load dev server list')

   #? Internal Functions
    def save_log(self):
        try:
            with open('bot.log', 'r') as f: oldlog = f.read()
            with open('db/old_logs.log', 'a') as f: f.write(oldlog)
        except FileNotFoundError:
            print('ERROR: Latest cant be found')
            print('INFO: \'bot.log\' ')

    #?Setup
    async def setup_hook(self):
        try:
            with open('db/system/startup.json', 'r', encoding='utf-8') as f:
                startup_data = json.load(f)
        except: 
            startup_data = {
                "extensions": {
                    "systematic": [
                        "extension.manager",
                        "extension.help"
                    ],
                    "normal": []
                }
            }
            with open('db/system/startup.json', 'w', encoding='utf-8') as f:
                json.dump(startup_data, f, indent=4, ensure_ascii=False)
        
        #? Built-in Commands Load
        try:
            await self.add_cog(self.cmd_core(self))
            self.log.info(f'cmd_core loaded')
        except Exception as error: self.log.critical(f'While loading cmd_core: {error}')
        try:
            await self.add_cog(self.staff_management(self))
            self.log.info(f'staff_management loaded')
        except Exception as error: self.log.critical(f'While loading staff_management: {error}')
        try:
            await self.add_cog(self.developer_management(self))
            self.log.info(f'developer_management loaded')
        except Exception as error: self.log.critical(f'While loading developer_management: {error}')

        #? Startup extensions loader
        #* Systematic
        for extension in startup_data['extensions']['systematic']:
            try:
                await self.load_extension(extension)
            except Exception as error:
                self.log.critical(f'Error while loading {extension}: {error}')
                self.log.info(f'You can solve this error by downloading extension folder on {GITHUB}')
                await self.stop()
                print('Check "bot.log" in order to find the error')

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
        if self.config.warn_onready:
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
        else: self.log.error(exception)
    
    #? BOOT FUNCTION
    def boot(self):
        self.run(self.config.TOCKEN)

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

def setup():
    path =  os.getcwd()
    
    #? Check before starting
    check = input('Running the setup script will rebuld Selenne and all the config and files will be deleted\nContinue?\tType YES\n> ')
    if check != 'YES':
        print('Setup aborted')
        exit()
    
    #? Installing libraries
    modules = [
        {'name':'discord', 'pip': 'pip install -U git+https://github.com/Rapptz/discord.py'},
        {'name':'PyNaCl', 'pip': 'pip install PyNaCl'},
        {'name':'youtube_dl', 'pip': 'pip install youtube_dl'},
        {'name':'mysql', 'pip': 'pip install mysql-connector-python'}
        ]
    for module in modules:
        try: importlib.import_module(module['name'], package=None)
        except ImportError: os.system(module['pip'])
    print('All Modules Installed')

    #? File System
    folders = ['db', 'db/system']
    files = [
        {'name': 'db/system/help.json', 'content': '{}'}
    ]
    for folder in folders:
        try: os.mkdir(folder)
        except FileExistsError: pass

    for file in files:
        with open(file['name'], 'w', encoding='utf-8') as f:
            f.write(file['content'])

    print('All File System Created')

    #? Add directory to path
    sys.path.append(path)
    print('Direcotry added to path')

    #? Selenne Boot Files
    check = input('Create Boot Files?\tType YES\n> ')
    if check == 'YES':
        files = [
            {'name': 'Selenne.vbs', 'content': '''Set WshShell = CreateObject("WScript.Shell")

WshShell.Run chr(34) & "Selenne.bat" & Chr(34), 0

Set WshShell = Nothing'''},
            {'name': 'Selenne.bat', 'content': '''@echo off
title Selenne 5  [Experimental Build]
python main.py

exit'''},
            {'name': 'Add to startup.txt', 'content': '''First on "run" type "shell:startup"
On the folder that will open paste a direct access of Selenne.vbs (will be Selenne.lnk)

NOTE: If you want to see the terminal that Selenne is using paste the Selenne.bat file insteard of Selenne.vbs'''},
        ]
        for file in files:
            with open(file['name'], 'w', encoding='utf-8') as f:
                f.write(file['content'])
        
        print('All startup Files Created')

    print('SETUP DONE!')
