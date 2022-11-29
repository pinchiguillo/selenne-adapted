import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional

__EXTENSION_NAME__ = ''

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    #await bot.add_cog(Default_cog(bot))

    #await bot.tree.sync()

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
        await interaction.response.send_message('Not avilable', ephemeral=True)


class Default_Slash_cog(discord.ext.commands.GroupCog, group_name = 'name', group_description = 'Description'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = '')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    subgroup = app_commands.Group(name = 'sub-sub command', description = 'Description')

    @subgroup.command(name= '')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)
