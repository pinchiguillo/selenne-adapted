import sys
sys.dont_write_bytecode = True
try:
    import discord
    from discord.ext import commands
    import json
    import asyncio
    import os
    import importlib
    import sys
    import traceback
    import mysql.connector
    import yaml
except ImportError as e: print('Error importing {}, use Selenne.setup() in order to build all the required thins for Selenne'.format(e))

#? Module Related Data
VERSION = 'Selenne 5.5'
AUTHOR = 'pinchiguillo'
SUPPORT_SERVER = 'https://example.com/discord-invite'
GITHUB = 'https://github.com/pinchiguillo/Selenne-Project'
SPECS = '='*15 + '   Selenne Module Specifications   ' + '='*15 + f'\n\tVersion: {VERSION}' + f'\n\tAuthor: {AUTHOR}' + f'\n\tSupport Server: {SUPPORT_SERVER}' + f'\n\tGitHub: {GITHUB}' + '\n'

New_Feuture = f'='*15 + '   {VERSION} New Features   ' + '='*15 + '''
Added Default SQL database
'''

Feuture_Updates = '='*15 + '   Selenne Future Updates   ' + '='*15 + '''
Bug fixes
'''

class Core(commands.Bot):
    
    #!DO NOT TOUCH ANYTHING, config in config.py file

    version = VERSION
    core_version = '2.4.e'
    building = True
    SQL = True
    import config
    #_TOCKEN_LOCK = False
    
    def __init__(self):
        #? Check all the bot files
        try:
            import config
            self.config = config
        except ImportError:
            exit()
        try: open('bot.log', 'r', encoding='utf8').read()
        except FileNotFoundError: pass

        #? Load config
        #! All config will be loaded via this method

        #? Load databases
        try:
            with open('config.yaml', 'r', encoding='utf-8') as stream: __config__ = yaml.safe_load(stream)
            self._database_ =  mysql.connector.connect(user=__config__['Database']['Credentials']['Username'], password=__config__['Database']['Credentials']['Password'], host=__config__['Database']['Credentials']['Host'], database=__config__['Database']['Credentials']['Database'])
        except Exception as e: 
            if 'Unknown database' in str(e): raise Exception('Database table not found')
            else: raise Exception('Error while loading database \'{}\''.format(__config__['Database']['Credentials']['Database']))

        #! Will allow per server prefix in 5.4
        async def set_prefix(bot, message): 
            prefix = config.PREFIX
            return commands.when_mentioned_or(*prefix)(bot, message)
        
        super().__init__(
            command_prefix=set_prefix,
            description = config.description,
            activity = discord.Game(name = config.activity),
            status = config.status,
            intents = config.intents
            )
        #? Universal Vars
        
        #* Staff checks
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
        self.oid = self.owner
        self.color = config.color
        self.colours = config.colours
        self.help_path = 'db/system/help.json'
        self.main_prefix = config.PREFIX[0]
        
        
        self.developers = self.staff['developers'] + [self.staff['owner']] #! NOT PERFECT
        self.dev_servers = self.staff['dev_servers']
        self.bot_servers = self.staff['bot_servers']

        #? Logging Engine
        import logging
        self.save_log()
        logging.basicConfig(filename='bot.log', filemode='w', encoding = 'utf8', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=config.log)
        self.log = logging

        #? Databases Engine - SQLtools 1.2
        from dcs.sqltools import DataBase #! MERGE WITH THIS FILE
        self.database = DataBase(config.SQL)

        #? Extra config for extensions
        self.remove_command('help') #* extension.help
        self.config_database = None #* extension.servermanager

        #! Lock building vars (False is True)
        self.building = False


    #? Essential Bot Commands
    #! WILL BE UPDATED TO SLASH
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
                os.system('start /min Selenne.bat') #! Always Windowed=False
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
            with open('bot.log', 'r', encoding='utf-8') as f: oldlog = f.read()
            with open('db/old_logs.log', 'a', encoding='utf-8') as f: f.write(oldlog)
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
                        "extension.manager", #! DONT MODIFY THIS
                        "extension.help" #! DONT MODIFY THIS
                    ],
                    "normal": []
                }
            }
            with open('db/system/startup.json', 'w', encoding='utf-8') as f:
                json.dump(startup_data, f, indent=4, ensure_ascii=False)
        
        #? Built-in Commands Load
        #! NEED OPTIMIZATION
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

    #? On Ready
    async def on_ready(self):
        self.log.info(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        if self.config.warn_on_ready:
            try:
                self.pid = await self.fetch_user(000000000000000000)
            except: self.log.warning('Error while fetching owner')
            try:
                m = await self.pid.send('Ya vuelvo a estar conectada')
                await asyncio.sleep(5)
                await m.delete()
            except: self.log.warning('Error while sending message to owner')

    #? Command Error Handler
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandNotFound): await ctx.send('Command Not Found, try using `s.help`', delete_after=10)
        else:
            exception = getattr(exception, 'original', exception)
            self.log.error(''.join(traceback.format_exception(exception)))
    
    
    #? BOOT FUNCTION
    def boot(self):
        s = f'Title {self.version} [Experimental Build]' #! [Experimental Build] will be removed on Selenne Stable release
        os.system(s) #!
        self.run(self.config.TOCKEN)

    #! UNDER DEVELOPMENT
    def restricted(self, ctx, whitelist=True, blacklist=False, guild=None, channel=None, members=None):
        check = False
        if guild and ctx.guild.id is guild: check = True
        if channel and ctx.channel.id is channel: check = True
        if members:
            if isinstance(members, list):
                if ctx.author.id in members: check = True,
            else:
                if ctx.author is members: check = True

        if whitelist: return check
        elif blacklist:
            if check: return False
            else: return True

    #? Var protection
    @property
    def owner(self): return self._owner
    @owner.setter
    def owner(self, value):
        if self.building: self._owner = value
        else: 
            self._owner = self._owner
            #raise SecurityError('owner var attempt to change') #! NOT internal errors built

    @property
    def color(self): return self._color
    @color.setter
    def color(self, value):
        if self.building: self._color = value
        else:
            self._color = self._color
            #raise SecurityError('owner var attempt to change') #! NOT internal errors built

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

#? Setup function for the bot 
#! DO NOT CREATE DCS FILE YET (It will be removed in the future)
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
        {'name':'mysql', 'pip': 'pip install mysql-connector-python'},
        {'name':'yaml', 'pip': 'pip install yaml'},
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
        try: open(file['name']).read()
        except:
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

#? Selenne Extension management tools
#! BETA
class Extension():
    def __init__(self, bot):
        self.bot = bot
        #! Scheme

        self.name = None
        self.version = None
        self.bot_version = None

        #? Slash Commands
        self.slash_command = False
        self.update_tree = False
        
        #? Cooldown
        #! ALFA
        self.cooldown_time = 0
        self.__cooldown_list__ = list()

        self.default_embed = discord.Embed(title = bot.nullchar, color=bot.color)

        class Config():
            def __init__(self, extension):
                self.enabled = False
                self.name = extension.name
                self.premium = False
                self.attr_name = f'{extension.name}'
                self.config_dict = dict()
                self.sync()

            def sync(self):
                if not self.enabled: return
                for guild in os.listdir('db/guilds'):
                    with open(os.path.join('db/guilds', guild), 'w+') as f:
                        data = json.load(f)

                        if not self.attr_name in data.keys(): data[self.attr_name] = {'enabled': False, 'request_premium': self.premium, 'display_name': self.name}
                        
                        json.dump(self.data, f, indent=4, ensure_ascii=False)

            async def get(self, guild):
                with open(os.path.join('db/guilds', str(guild) + '.json'), 'r') as f:
                    return json.load(f)

        self.config = Config(self)
        
        #! RELEASED - Waiting help functions merge
        class Help():
            enabled = False
            def __init__(self):
                self.general_display = str()
                self.specific_display = dict()
                self.specific_display_help = "{'cmd': 'use'}"
                self.emoji = '❄️' #

            def add(self):
                return {'general_display': self.general_display,'specific_display': self.specific_display, 'emoji': self.emoji}
        self.help = Help()
        
        #! ALFA
        class Database():
            def __init__(self):
                self.storage_type = None
                self.path = None
                self.sql = None
                self.data = None

                self.__online__ = False

            def start(self):
                if self.storage_type == 'json_dir':
                    open(os.path.join(self.path, 'db.index')).read()
                    self.__online__ = True

            def get(self, entry:str):
                if not self.__online__: raise ValueError('Database not online')
                try: 
                    with open(os.path.join(self.path, f'{entry}.json'), 'r', encoding='utf8') as f:
                        return json.load(f)
                except: return None
            def edit(self, entry:str, new_value:dict):
                if not self.__online__: raise ValueError('Database not online')
                try: 
                    with open(os.path.join(self.path, f'{entry}.json'), 'r', encoding='utf8') as f:
                        data =  json.load(f)
                except: raise FileNotFoundError('Error while locating entry')

                data[str(list(new_value.keys())[0])] = new_value[str(list(new_value.keys())[0])]
                with open(os.path.join(self.path, f'{entry}.json'), 'w', encoding='utf8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
            def create(self, entry:str, values:dict):
                if not self.__online__: raise ValueError('Database not online')
                with open(os.path.join(self.path, f'{entry}.json'), 'w', encoding='utf8') as f:
                        json.dump(values, f, indent=4, ensure_ascii=False)
            def delete(self, entry:str):
                if not self.__online__: raise ValueError('Database not online')
                os.remove(os.path.join(self.path, f'{entry}.json'))

            def create_table(self, name:str):
                if not self.__online__: raise ValueError('Database not online')
                try:
                    os.mkdir(os.path.join(self.path, str(name)))
                    return True
                except FileExistsError:
                    return False

        self.database = Database()


        self.cogs = list()
        self.views = list()

    async def load(self):
        self.link_version()
        await self.check_compatibility()
        await self.load_cogs()
        await self.load_views()
        await self.add_help()
        await self.sync()
        self.config.sync()
        await self.loaded()
    async def unload(self):
        await self.remove_help()
        await self.unloaded()

    #! BUG FIX FUNCTION
    def link_version(self):
        _version = self.name.replace(' ', '')
        self._version = f'{_version.lower()}: {self.version}'

    #! RELEASED
    async def check_compatibility(self):
        if 'alfa' in self.version or 'beta' in self.version:
            self.bot.log.warning(f'{self.name} is being loaded in a development state')
        
        if list(self.bot_version)[8:11] != list(self.bot.version)[8:11]:  self.bot.log.warning(f'{self.name} OUTDATED. {self.name} built for {self.bot_version}, current: {self.bot.version}')

    #! RELEASED
    async def load_cogs(self):
        for cog in self.cogs:
                await self.bot.add_cog(cog(self.bot))
                self.bot.log.info(f'{cog} cog added')

    #! NOT TESTED
    async def load_views(self):
        for view in self.views:
                await self.bot.add_view(view)
                self.bot.log.info(f'{view} view reloaded')

    async def sync(self):
        if self.slash_command:
            await self.bot.tree.sync()
            self.bot.log.info(f'slash.tree upaded by {self._version}') 

    #! MERGE TO HELP CLASS
    async def add_help(self):
        if not self.help.enabled: return
        with open(self.bot.help_path, 'r', encoding='utf-8') as f:
            help_list = json.load(f)
        help_list[self.name] = self.help.add()
        with open(self.bot.help_path, 'w', encoding='utf-8') as f:
            json.dump(help_list, f, indent=5)
    async def remove_help(self):
        with open('db/system/help.json', 'r', encoding='utf-8') as f:
            help_list = json.load(f)
        del help_list[self.name]
        with open('db/system/help.json', 'w', encoding='utf-8') as f:
            json.dump(help_list, f, indent=5, ensure_ascii= False)
    async def get_help(self, name=None):
        data = dict()
        if not name: name = self.name
        with open(self.bot.help_path, 'r', encoding='utf-8') as f:
            help_dir = json.load(f)
            if help_dir[name]['specific_display']:
                try:
                    for key in help_dir[name]['specific_display'].keys():
                        data[key] = self.database.data[name]['specific_display'][key]
                        
                except Exception as e:
                    self.bot.log.error('Error while creating specific_display: %s', e)
                    return 'Cant found that extension'
            else: return f'{name} Doesnt have specific help'
            return data

    #! MERGE TO DATABASE CLASS
    async def load_db(self):
        if self.database.storage_type == 'json':
            with open(self.database.path, 'r', encoding='utf-8') as f:
                self.database.data =  json.load(f)
        else: raise ValueError('This database type is not supported')
    async def unload_db(self):
        if self.database.storage_type == 'json':
            with open(self.database.path, 'w', encoding='utf-8') as f:
                json.dump(self.database.data, f, indent=5, ensure_ascii = False)

    #? Setup and Teardown functions
    #! RELEASED
    async def loaded(self): self.bot.log.info(f'extension.{self._version.lower()} loaded')
    async def unloaded(self): self.bot.log.info(f'extension.{self._version.lower()} unloaded')
