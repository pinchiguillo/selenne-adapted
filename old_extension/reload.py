import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional

__EXTENSION_NAME__ = 'Reload 1.0'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(Reload_cog(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class Reload_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

    @discord.app_commands.command(name='privatereload')
    @discord.app_commands.describe()
    async def privatereload(self, interaction: discord.Interaction):
        """Admin Command for Bot Extensions Reload"""
        
        data = ''
        embed=discord.Embed(title='Display', description=data)

        await interaction.response.send_message('Not avilable', ephemeral=True, embed=embed)
