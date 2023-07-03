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
    COGS = [AdminTools]

    for cog in COGS:
        try: await bot.add_cog(cog(bot))
        except Exception as e: bot.logger.error('Failed to load cog: {}: {}'.format(cog.__name__, e))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

if not __EXTENSION_NAME__: __EXTENSION_NAME__ = os.path.splitext(os.path.basename(__file__))[0]

#! Extension Code

#? Sample
class AdminTools(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot


    @discord.app_commands.command(name = 'isloate')
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
    async def isolate_slashCommand(self, interaction: discord.Interaction, user: discord.Member, reason:str, time: discord.app_commands.Choice[int]):
        """Puts an user a timeout and sends a message"""
        await interaction.response.defer(ephemeral=True, thinking=True)

        match time.value:
            case 1: i_time = datetime.timedelta(minutes=1)
            case 2: i_time = datetime.timedelta(minutes=5)
            case 3: i_time = datetime.timedelta(hours=1)
            case 4: i_time = datetime.timedelta(days=1)
            case 5: i_time = datetime.timedelta(days=7)

        try: 
            await user.timeout(i_time, reason=reason)
            await interaction.followup.send('{} has been muted'.format(user.mention), ephemeral=True)
            await interaction.channel.send('*{} has been isolated for {} for {}*'.format(user.mention, time.name, reason))
        except: 
            await interaction.followup.send('An error has occurred isolating {}'.format(user.mention))

    @discord.app_commands.command(name = 'kick')
    @discord.app_commands.default_permissions(kick_members=True)
    @discord.app_commands.describe(
        reason = 'Reason of the kick'
    )
    async def kick_slashCommand(self, interaction: discord.Interaction, reason:str):
        """Kicks and sends a private message to a player"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        try: 
            await interaction.user.kick(reason = reason)

            await interaction.user.send('You have been kicked for {} from {}'.format(reason, interaction.guild.name))
        
            await interaction.followup.send('{} has been kicked'.format(interaction.user.mention), ephemeral=True)
        except:
            await interaction.followup.send('An error has occurred kicking {}'.format(interaction.user.mention))

    @discord.app_commands.command(name = 'ban')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(
        user = 'The user that will be banned',
        reason = 'Reason of the ban'
    )
    async def ban_slashCommand(self, interaction: discord.Interaction, user: discord.Member, reason:str):
        """Bans a player and sends a private message message"""
        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            await user.ban(delete_message_days=7, reason=reason)
            await user.send('You have been banned for {} from {}'.format(reason, interaction.guild.name))

            await interaction.followup.send('{} has been banned and his messages from the last 7 days have been deleted'.format(interaction.user.mention), ephemeral=True)
        except:
            await interaction.followup.send('An error has occurred while banning {}'.format(interaction.user.mention))

    @discord.app_commands.command(name = 'clear')
    @discord.app_commands.default_permissions(manage_messages=True)
    @discord.app_commands.describe(
        amount = 'The amount of messages that will be deleted',
        channel = 'The channel that will be cleared'
    )
    async def clear_slashCommand(self, interaction: discord.Interaction, channel:discord.TextChannel = None, amount:discord.app_commands.Range[int, 1, 500] = 100):
        """Cleans a channel"""
        await interaction.response.defer(ephemeral=True, thinking=True)

        if not channel: channel = interaction.channel

        c = 0
        for message in channel.history(limit=amount):
            await message.delete()
            c += 1

        await interaction.followup.send('{} messages deleted in {}'.format(c, channel.mention))
