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
import os, json

#! Extension Name (if not the filename will be used)
__EXTENSION_NAME__ = ''

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))

    #! Add cog Classes    
    COGS = [BotStats]

    for cog in COGS:
        try: await bot.add_cog(cog(bot))
        except Exception as e: bot.logger.error('Failed to load cog: {}: {}'.format(cog.__name__, e))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

if not __EXTENSION_NAME__: __EXTENSION_NAME__ = os.path.splitext(os.path.basename(__file__))[0]

#! Extension Code

#? Sample
class BotStats(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot
    
    @discord.app_commands.command(name = 'stats')
    @discord.app_commands.describe()
    async def stats_slashCommand(self, interaction: discord.Interaction):
        """Show Selenne Stats"""
        await interaction.response.defer(ephemeral=True, thinking=True)

        cursor = self.bot.database.cursor(buffered=True)
        SQL = "SELECT * FROM `message`"
        cursor.execute(SQL)

        msg_count = len(cursor.fetchall())

        embed=discord.Embed(title = 'Selenne Stats', description = '**Version**: ***{0}*** - Bot Desarrollado por *DCS*'.format(self.bot.VERSION), color=__bot__.color)
        embed.add_field(name = 'Bot', value = '**Cumpleaños**: *{}*\n**Version**: *{}*\n**Owner**: ***{}***'.format(self.bot.BIRTH_DAY, self.bot.VERSION, type(self.bot.owner)), inline=False)
        embed.add_field(name = 'Stadisticas', value = '**Nodo**: ***{}***\n**Servidores**: `{}`\n**Usuarios**: `{}`\n**Mensajes leidos**: `{}`'.format(self.bot.__node__, len(list(self.bot.guilds)), len(list(self.bot.users)), msg_count), inline=False)
        
        await interaction.followup.send(embed=embed, view=ReleasesView())

class ReleasesView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    
    @discord.ui.button(label = 'Releases', style=discord.ButtonStyle.blurple, disabled=False) #! Remove disabled
    async def releases(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        embed=discord.Embed(title = 'Selenne Release Notes', description = '***Selenne*** is a bot that is actualy under development.\nUpdates of the last versions:'.format(__bot__.VERSION), color=__bot__.color)
        
        with open('releases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for release in data['releases']:
            embed.add_field(name = release, value = data['releases'][release], inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label = 'Active Expansions Development', style=discord.ButtonStyle.green, disabled=False) #! Remove disabled
    async def expansions_dev(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        embed=discord.Embed(title = 'Active Expansions Development', description = __bot__.nullchar, color=__bot__.color)
        
        with open('releases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for expansion in data['expansions']:
            embed.add_field(name = expansion, value = data['expansions'][expansion], inline=False)

        embed.set_footer(text = 'Last update: {}'.format(datetime.datetime.fromtimestamp(os.path.getmtime('releases.json')).strftime('%d/%m/%Y')))

        await interaction.response.send_message(embed=embed, ephemeral=True)
