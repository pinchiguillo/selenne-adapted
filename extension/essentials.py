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
    COGS = [Essentials]

    for cog in COGS:
        try: await bot.add_cog(cog(bot))
        except Exception as e: bot.logger.error('Failed to load cog: {}: {}'.format(cog.__name__, e))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

if not __EXTENSION_NAME__: __EXTENSION_NAME__ = os.path.splitext(os.path.basename(__file__))[0]

#! Extension Code



#? Sample
class Essentials(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot
    
    @discord.app_commands.command(name = 'serverinfo')
    @discord.app_commands.describe()
    async def serverinfo_SlashCommand(self, interaction: discord.Interaction):
        """Get the discord server information"""
        await interaction.response.defer(ephemeral=False, thinking=True)

        #Get bot count
        bots = 0
        for member in interaction.guild.members:
            if member.bot: bots += 1

        #? Generate the embed
        embed = discord.Embed(title = 'ServerInfo', color= self.bot.color)
        embed.add_field(name = 'Owner', value = interaction.guild.owner.mention)
        embed.add_field(name = 'Creation Date', value = interaction.guild.created_at.strftime("%d/%m/%Y"))
        embed.add_field(name = 'Members', value = len(interaction.guild.members))
        embed.add_field(name = 'Channels', value = len(interaction.guild.channels))
        embed.add_field(name = 'Bots', value = bots)
        embed.add_field(name = 'Emojis', value = len(interaction.guild.emojis))
        embed.add_field(name = 'Nitro Boosters', value = len(interaction.guild.premium_subscribers))

        embed.set_thumbnail(url = interaction.guild.icon.url)

        await interaction.followup.send(embed=embed, view=ServerInfoView())

    @discord.app_commands.command(name = 'whois')
    @discord.app_commands.describe(
        user = 'The user you to get info'
    )
    async def whois_SlashCommand(self, interaction: discord.Interaction, user:discord.Member|discord.User = None):
        """Get data about an user"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        if not user: user = interaction.user

        # Get Roles
        rolesl = list()
        for role in user.roles:
            if role.name != '@everyone':
                rolesl.append(role.mention)
        roles = ", ".join(reversed(rolesl))

        #? Create the embed
        embed = discord.Embed(title= f'Who is {user}?', colour = self.bot.color)

        embed.set_thumbnail(url = user.avatar)
        embed.set_footer(text = f'Requested by - {interaction.user}', icon_url = interaction.user.avatar)

        embed.add_field(name = 'ID:', value = user.id, inline=False)
        embed.add_field(name = 'Name:', value = user.display_name, inline=False)
        diff = str(datetime.datetime.now() - user.created_at.replace(tzinfo=None)).split(',')[0]
        embed.add_field(name = 'Created at:', value = f'{user.created_at.strftime("%d/%m/%Y %H:%M")} ({diff} ago)', inline=False)
        diff = str(datetime.datetime.now() - user.joined_at.replace(tzinfo=None)).split(',')[0]
        embed.add_field(name = 'Joined at:', value = f'{user.joined_at.strftime("%d/%m/%Y %H:%M")} ({diff} ago)', inline = False)
        if len(rolesl) >= 1:
            embed.add_field(name = f'Roles: {len(rolesl)} ',value = ''.join([roles]), inline=False)
            embed.add_field(name = 'Top Role:', value = user.top_role.mention, inline=False)
        else:
            embed.add_field(name = f'Roles: 0',value = self.bot.nullchar, inline=False)

        await interaction.followup.send(embed=embed)

    @discord.app_commands.command(name = 'echo')
    @discord.app_commands.describe(
        message = 'The message you want Selenne to say',
        times = 'The number of times the message will repeat'
    )
    async def echo_SlashCommand(self, interaction: discord.Interaction, message:str, times: discord.app_commands.Range[int, 1, 10] = 1):
        """Make Selenne repeat a message"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        await interaction.followup.send(f'Okey {interaction.user.mention}', ephemeral=True)

        for _ in range(times):
            await interaction.channel.send(message)

class ServerInfoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    
    @discord.ui.button(label = 'Emojis', style=discord.ButtonStyle.blurplevent, disabled=True)
    async def EmojiBTN(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


