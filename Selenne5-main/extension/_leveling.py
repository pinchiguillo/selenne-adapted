import Selenne
import discord
from discord.ext import commands

import asyncio

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Leveling System'
    extension.version = 'Alfa'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/system/startup.json'


    #? Commands
    extension.cogs = [Leveling]


    #! DO NOT TOUCH
    #? Check Compatibility
    await extension.check_compatibility()
    await extension.load_cogs()
    await extension.load_views()
    await extension.add_help()
    await extension.loaded()
async def teardown(bot):
    await extension.remove_help()
    await extension.unloaded()

#! Extension Code

#? Sample
class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
        self.cooldown_time = 5
        self.__cooldown_list__ = list()

    def cooldown(self, author):
        self.__cooldown_list__.append(author.id)
        self.bot.log.info(self.__cooldown_list__)
        asyncio.sleep(self.cooldown_time)
        #self.__cooldown_list__.pop(self.__cooldown_list__.index(author.id))
        self.bot.log.info(self.__cooldown_list__)


    @commands.Cog.listener()
    async def on_message(self, message):
        self.bot.log.info('Message detected')
        if message.author.id != self.bot.owner: return
        self.bot.log.info('Owner')

        #? Cooldown
        if message.author.id in self.__cooldown_list__:
            self.bot.log.info('On Cooldown')
            return
        self.bot.log.info('Avilable')
        self.cooldown(message.author)
        self.bot.log.info(self.__cooldown_list__)
