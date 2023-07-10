import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional

__EXTENSION_NAME__ = 'CustomProfile'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    #await bot.add_cog(Default_cog(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class Default_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

    @discord.app_commands.command()
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send('Not avilable', ephemeral=True)


class CustomProfile_Commands_cog(discord.ext.commands.GroupCog, group_name = 'name', group_description = 'Description'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = '')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    customprofile = app_commands.Group(name = 'CustomProfile', description = 'Custom Profile Extension')

    @customprofile.command(name= 'info')
    @discord.app_commands.describe()
    async def customprofile_info(self, interaction: discord.Interaction):
        """Gives information about the Custom Profile Extension"""

        embed = discord.Embed(name='Custom Profile Info', color=self.bot.color)

        embed.description = '''Custom Profile es una extension que permite a los usuarios crearse un personaje, subirlo de nivel... al estilo RPG
Custom Profile de Selenne tiene actualmente:
Nada -_-

'''

        await interaction.response.send_message('Not avilable', ephemeral=True)
