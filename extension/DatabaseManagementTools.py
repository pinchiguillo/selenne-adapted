import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

__EXTENSION_NAME__ = 'Database Management Tools'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(Database_Listeners(bot))
    await bot.add_cog(Database_Sync_Core(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code
class Database_Listeners(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self): pass


class Database_Sync_Core(discord.ext.commands.GroupCog, group_name = 'sdb', group_description = 'Selenne Database Admin Tools'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = 'stats')
    @discord.app_commands.describe()
    async def sdbat_stats_cmd(self, interaction:discord.Interaction):
        """Get Database Stats"""
        
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @discord.app_commands.command(name = 'sync')
    @discord.app_commands.describe()
    async def sdbat_sync_cmd(self, interaction:discord.Interaction):
        """Force de Sync of all the api data and the database"""
        await interaction.response.send_message('Not avilable', ephemeral=True)
