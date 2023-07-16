# Selenium 5 Custom Bot

import sys
sys.dont_write_bytecode = True

import yaml
import json
import asyncio
import os
import importlib
import traceback
import mysql.connector
import logging
import platform

import discord
from discord.ext import commands

#? 
#? This is a custom verion of Selenne 5
#? This version avoids all the modular functions
#? 
#! This version ONLY suports slash Commans
#? 
#? Developed by pinchiguillo
#? 

#! Missing Config.generate()
class Config():
    name:str
    version:str
    prefix:str
    token:str
    owner:int
    warn_on_ready:bool
    description:str
    activity:str
    status:str
    color:int
    colours:dict[str, int]
    databases:dict
    extensions:list
    localDB:str

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

class Core(commands.Bot): # commands.AutoShardedBot() #! 1000+ Servers
    VERSION = 'Selenium 5.5b'

    AUTHOR = 'pinchiguillo'
    log_level = logging.DEBUG
    intents_cfg = discord.Intents.all()
    BIRTH_DAY = '25/5/2021'

    tree_sync = False

    #? Error Class
    class Error():
        class ConfigNotFound(Exception): 
            def __init__(self): super().__init__('Config file (config.yaml) not found')
        
        class ConfigLoadFailure(Exception): 
            def __init__(self): super().__init__('Error while loading config file (config.yaml)')

        class CorruptConfig(Exception): 
            def __init__(self): super().__init__('Config file (config.yaml) is corrupted')

        class CantConnectDatabaseError(Exception): 
            def __init__(self): super().__init__('Error while connecting to databasel')

    
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
            
            #? Increasing var acces
            self.nullchar = '\u200b'
            self.owner:discord.User = self.config.owner #! Owner discord user will be loaded when online
            del self.config.owner
            self.color = self.config.color
            del self.config.color
            self.colours = self.config.colours
            del self.config.colours

            self.logger.info('Config loaded')

        except FileNotFoundError as e: 
            self.logger.critical('Exception while loading config file: {}'.format(e))
            raise self.Error.ConfigNotFound()
        except KeyError as e:
            self.logger.critical('Exception while loading config file: {}'.format(e))
            raise self.Error.CorruptConfig()
        except Exception as e: 
            self.logger.critical('Exception while loading config file: {}'.format(e))
            raise self.Error.ConfigLoadFailure()

        #? Import discord bot class
        super().__init__(
            command_prefix = self.config.prefix,
            description = self.config.description,
            activity = discord.Game(name = self.config.activity),
            status = self.config.status,
            intents = self.intents_cfg
            )
        self.logger.debug('Discord.py main bot class data loaded')

        #? BOOT
        if autoboot: self.boot()

    async def setup_hook(self):
        
        self.__load_databases__()

        #? Load Extensions
        for extension in self.config.extensions:
            try:
                await self.load_extension(f'{extension}')
            except Exception as error:
                self.logger.error(f'{extension} failed to load: {error}')

        if self.tree_sync: await self.tree.sync()

    async def on_ready(self):
        self.logger.info(f'Bot online using {self.VERSION}')
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        
        try:
            self.owner = await self.fetch_user(self.owner)
        except Exception as e: self.logger.warning('Error while fetching owner discord user: {}'.format(e))
        
        if self.config.warn_on_ready:
            try: await self.owner.send(self.language('es-ES', 'online'), delete_after=5)
            except: self.logger.warning('Error while sending message to owner')

    #? Command Error Handler
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandNotFound): await ctx.send('Command Not Found, try using `s.help`', delete_after=10)
        else:
            exception = getattr(exception, 'original', exception)
            self.logger.error(''.join(traceback.format_exception(exception)))

    def __load_databases__(self):
        try:
            self.database = mysql.connector.connect(
                host = self.config.databases.get('host'),
                user = self.config.databases.get('username'),
                password = self.config.databases.get('password'),
                database = self.config.databases.get('database'),
                )
        except mysql.connector.errors.DatabaseError as e:
            self.logger.critical('Cant connect to database')
            raise e

    def boot(self):
        os.system('title {}'.format(self.config.version))
        self.run(self.config.token)
