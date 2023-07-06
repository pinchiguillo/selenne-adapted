import sys
sys.dont_write_bytecode = True

import Selenne

#? Discord library and shortcuts
import discord
from discord.ext import commands
from discord import app_commands

#? Required for documentation (can be removed)
from ctypes import Union
import datetime
from typing import Sequence

#? Extra Libraries
import os

#! Extension Name (if not the filename will be used)
__EXTENSION_NAME__ = ''

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))

    #! Add cog Classes    
    COGS = [SanityChecker]

    for cog in COGS:
        try: await bot.add_cog(cog(bot))
        except Exception as e: bot.logger.error('Failed to load cog: {}: {}'.format(cog.__name__, e))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

if not __EXTENSION_NAME__: __EXTENSION_NAME__ = os.path.splitext(os.path.basename(__file__))[0]

#! Extension Code

#? Sample
class SanityChecker(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot
    
    @discord.app_commands.command(name = 'SanityChecker')
    @discord.app_commands.describe()
    async def SanityChecker_slashCommand(self, interaction: discord.Interaction):
        """Checks the status of the current node"""
        await interaction.response.defer(ephemeral=True, thinking=True)

        if not interaction.user is self.bot.owner: 
            await interaction.followup.send('You dont have access to this command')
            return


        await interaction.followup.send('Not Avilable')
