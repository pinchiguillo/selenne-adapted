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

class Core(commands.Bot): # commands.AutoShardedBot() #! 1000+ Servers
    VERSION = 'Selenium 5.4b.269d'

    AUTHOR = 'pinchiguillo'
    log_level = logging.DEBUG
    indents_cfg = discord.Intents.all()
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

        class LanguagesNotFound(Exception): 
            def __init__(self): super().__init__('Languaje file (language.yaml) not found')
        
        class LanguagesLoadFailure(Exception): 
            def __init__(self): super().__init__('Error while loading language file (language.yaml)')

        class CorruptLanguagesFile(Exception): 
            def __init__(self): super().__init__('language file (language.yaml) is corrupted')

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
            with open('config.yaml', 'r', encoding='utf8') as f:
                self.config = yaml.safe_load(f)

                #? Saving config as variables
                self.nullchar = '\u200b'
                self.owner = self.config['owner']
                self.oid = self.config['owner_id']
                self.color = self.config['color']
                self.colours = self.config['colours']

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

        #? Load Languages
        try:
            with open('languages.yaml', 'r', encoding='utf8') as f:
                self.__languages__ = yaml.safe_load(f)


                self.logger.info('Language loaded')
        except FileNotFoundError as e: 
            self.logger.critical('Exception while loading Language file: {}'.format(e))
            raise self.Error.LanguagesNotFound()
        except KeyError as e:
            self.logger.critical('Exception while loading Language file: {}'.format(e))
            raise self.Error.CorruptLanguagesFile()
        except Exception as e: 
            self.logger.critical('Exception while loading Language file: {}'.format(e))
            raise self.Error.LanguagesLoadFailure()
        
        #? Import discord bot class
        super().__init__(
            command_prefix = self.config['prefix'], #! Only for developer actions
            description = self.config['description'],
            activity = discord.Game(name = self.config['activity']),
            status = self.config['status'],
            intents = self.indents_cfg
            )
        self.logger.debug('Parent data imported')

        #? BOOT
        if autoboot: self.boot()

    def language(self, lan, text) -> str:
        return self.__languages__[lan][text]

    async def setup_hook(self):
        
        self.__load_databases__()

        #? Load Extensions
        for extension in self.config['extensions']:
            try:
                await self.load_extension(f'{extension}')
            except Exception as error:
                self.logger.error(f'{extension} failed to load: {error}')

        if self.tree_sync: await self.tree.sync()

    async def on_ready(self):
        self.logger.info(f'Bot online using {self.VERSION}')
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        
        try:
            self.owner_user = await self.fetch_user(self.oid)
        except Exception as e: self.logger.warning('Error while fetching owner: {}'.format(e))
        
        if self.config['warn_on_ready']:
            try:
                m = await self.owner_user.send(self.language('es-ES', 'online'))
                await asyncio.sleep(5)
                await m.delete()
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
                host = self.config['databases']['host'],
                user = self.config['databases']['username'],
                password = self.config['databases']['password'],
                database = self.config['databases']['database'],
                )
        except mysql.connector.errors.DatabaseError as e:
            self.logger.critical('Cant connect to database')
            raise e

    def boot(self):
        os.system('title Selenne 5 (Block Version)')
        self.run(self.config['TOKEN'])
