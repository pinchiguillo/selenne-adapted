import sys
sys.dont_write_bytecode = True
import Selenne
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Teemplate'
    extension.version = 'Alfa'
    extension.bot_version = 'Selenne 5.5'
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/system/startup.json'
    #extension.database.start()

    #? Slash Commands
    extension.slash_command = False

    #? Commands
    extension.cogs = []

    #? Config
    extension.config.enabled = False
    #extension.config.name = '' #? Default: extension.name
    extension.config.premium = False
    #extension.config.attr_name = '' #? Default: extension.name
    extension.config.config_dict = {}

    #! DO NOT TOUCH
    #? Check Compatibility
    await extension.load()
async def teardown(bot): await extension.unload()

#! Extension Code

#? Sample
class Default_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

    @discord.app_commands.command()
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction, first_value: int, second_value: Optional(int)):
        """Description"""
        await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')