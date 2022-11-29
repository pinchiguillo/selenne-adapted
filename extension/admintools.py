import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import datetime

__EXTENSION_NAME__ = 'Admin Tools'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(AdminTools_cog(bot))

    #await bot.tree.sync()

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class AdminTools_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = 'timeout')
    @discord.app_commands.checks.has_permissions(manage_messages = True)
    @app_commands.choices(time=[
        discord.app_commands.Choice(name = '60 segundos', value = 1),
        discord.app_commands.Choice(name = '5 minutos', value = 2),
        discord.app_commands.Choice(name = '1 hora', value = 3),
        discord.app_commands.Choice(name = '1 dia', value = 4),
        discord.app_commands.Choice(name = '1 semana', value = 5),
    ])
    @discord.app_commands.default_permissions(moderate_members=True)
    @discord.app_commands.describe(
        user = 'The user that will have a timeout',
        reason = 'Reason of the timeout'
    )
    async def admintools_timeout(self, interaction: discord.Interaction, user: discord.Member, reason:str, time: discord.app_commands.Choice[int]):
        """Puts an user a timeout and sends a message"""

        match time.value:
            case 1: i_time = datetime.timedelta(minutes=1)
            case 2: i_time = datetime.timedelta(minutes=5)
            case 3: i_time = datetime.timedelta(hours=1)
            case 4: i_time = datetime.timedelta(days=1)
            case 5: i_time = datetime.timedelta(days=7)

        await user.timeout(i_time, reason=reason)
        await interaction.response.send_message('{} has been muted'.format(user.mention), ephemeral=True)
        await interaction.channel.send('*{} ha sido aislado durante {} por {}*'.format(user.mention, time.name, reason))
