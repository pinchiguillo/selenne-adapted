import yaml, discord, logging, platform, traceback

from discord.ext import commands

class Config():
    prefix:str
    token:str
    warn_on_ready:bool
    color:int
    colours:dict[str, int]

    class LoadError(Exception):
        def __init__(self, filename:str):
            self.filename = filename
            self.message = 'Error while loading \'{}\' config file'.format(filename)
            super().__init__(self.message)

        def __str__(self):
            return self.message

    def __init__(self, file:str = 'config.yaml') -> None:
        self.__file__ = file
        try: self.load()
        except self.LoadError as e:
            if input('Generate File? Y/n\n> ').lower() == 'y':
                self.generate_file()
                print('File generated in \'{}\''.format(self.__file__))
                exit()

    
    def load(self) -> None:
        with open(self.__file__, 'r', encoding='utf8') as f:
            self.__config__ = yaml.safe_load(f)

        self.name = self.__config__['name']
        self.version = self.__config__['version']
        self.prefix = self.__config__['prefix']
        self.token = self.__config__['TOKEN']
        self.owner = self.__config__['owner']
        self.warn_on_ready = self.__config__['warn_on_ready']
        self.description = self.__config__['description']
        self.activity = self.__config__['activity']
        self.status = self.__config__['status']
        self.color = self.__config__['color']
        self.colours = self.__config__['colours']
        self.databases = self.__config__['databases']
        self.extensions = self.__config__['extensions']
        self.localDB = self.__config__['LocalDatabase']


    def generate_file(self, as_str:bool = False) -> str|None:
        string = '''Not Implemented'''

        if as_str: return string
        with open(self.__file__, 'w', encoding='utf8') as f: f.write(string)


class Core(commands.Bot): #? CLUSTERING: commands.AutoShardedBot() #! 1000+ Servers
    """Core of the framework"""
    
    __version__ = '6.0'

    prefix:str
    log_level = logging.DEBUG
    intents_cfg = discord.Intents.all()

    AUTHOR = 'pinchiguillo'
    BIRTH_DAY = '25/5/2021'

    def __init__(self, autoboot = True):
        
        #? Load Logging
        logging.basicConfig(filename='bot.log', filemode='a', encoding = 'utf8', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=self.log_level)
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Logger Started')

        #? Node
        self.__node__ = platform.node()
        
        #? Load Config
        try: 
            self.config = Config('config.yaml')
            
            #? Increasing var access
            self.nullchar = '\u200b'
            self.color = self.config.color
            self.colours = self.config.colours

            self.logger.info('Config loaded')

        except FileNotFoundError as e: 
            self.logger.critical('Exception while loading config file: {}'.format(e))
            raise Exceptions.ConfigNotFound()
        except KeyError as e:
            self.logger.critical('Exception while loading config file: {}'.format(e))
            raise Exceptions.CorruptConfig()
        except Exception as e: 
            self.logger.critical('Exception while loading config file: {}'.format(e))
            raise Exceptions.ConfigLoadFailure()

        #? Import discord bot class
        super().__init__(
            command_prefix = self.config.prefix,
            description = self.config.description,
            activity = discord.Game(name = 'Under Development'), #!!!
            status = 'Under Development', #!!!
            intents = self.intents_cfg
            )
        self.logger.debug('Discord.py main bot class data loaded')

        #? BOOT
        if autoboot: self.boot()
    
    async def setup_hook(self):
        
        self.__load_databases__()

        #? Load Extensions
        with open('configs\\extensions.yaml') as f:
            extensions = yaml.load_all(f, Loader=yaml.FullLoader)
        for extension in extensions:
            self.extension = Extension(extension)
            self.load_extension(self.extension.filename)

    def __load_databases__(self): #!!!
        pass

    async def on_ready(self):
        self.logger.info(f'Bot online using {self.__version__}')
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        
        self.app_data = await self.application_info()
        
        self.owner = self.app_data.owner
        
        if self.config.warn_on_ready:
            try: await self.owner.send('Selenne Online!', delete_after=5)
            except: self.logger.warning('Error while sending message to owner')

    #? Command Error Handler
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandNotFound): await ctx.send('Command Not Found, try using `s.help`', delete_after=10)
        else:
            exception = getattr(exception, 'original', exception)
            self.logger.error(''.join(traceback.format_exception(exception)))

class Exceptions(): 
    class LoadError(Exception):
        def __init__(self, filename:str):
            self.filename = filename
            self.message = 'Error while loading \'{}\' file'.format(filename)
            super().__init__(self.message)

    class ConfigNotFound(Exception): 
        def __init__(self, cfg_file): super().__init__('Config file ({}) not found'.format(cfg_file))

    class CorruptConfig(Exception): 
        def __init__(self, cfg_file): super().__init__('Config file ({}) is corrupted'.format(cfg_file))

    class ConfigLoadFailure(Exception): 
        def __init__(self, cfg_file): super().__init__('Error while loading config file ({})'.format(cfg_file))

class Databases(): 
    """Framework database Manager"""

    @staticmethod
    def load(self) -> 'Databases':
        with open('configs\\databases.yaml') as f:
            return Databases(yaml.load_all(f, Loader=yaml.FullLoader))

    def __init__(self, databases) -> None:
        for database in databases:
            setattr(self, database['name'], database['connection'])

class Model(): 
    """Default Model for the framework"""
    
    database = None
    table = None

    @staticmethod
    def exists() -> bool:
        pass

    def create() -> bool:
        pass

class Extension(): 
    """Extensions for the framework"""

    filename:str

    name:str
    description:str
    version:str
    validVersion:list[str]
    requires:list['Extension']

    def __init__(self, data):
        
        self.filename = data['filename']
        
        self.name:str = data['name']
        self.description:str = data['description']
        self.version = data['version']

        self.validVersion = data['validVersions']
        
        self.requires = [Extension(data) for data in data['requires']]


class Display(): 
    """Display Manager for the framework"""

    @staticmethod
    def load(self) -> 'Display':
        with open('configs\\display.yaml') as f:
            return Display(yaml.load_all(f, Loader=yaml.FullLoader))

    def __init__(self, displays) -> None:
        for display in displays:
            setattr(self, display['name'], display['path'])
            