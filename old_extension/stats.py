import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

__EXTENSION_NAME__ = 'stats'

import json
import os
import datetime

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    global __bot__
    __bot__ = bot
    
    await bot.add_cog(Stats_cog(bot))
    
    #await bot.tree.sync()

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample

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


class Stats_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot:Selenne.Core = bot

    @discord.app_commands.command(name = 'stats')
    @discord.app_commands.describe()
    async def stats(self, interaction: discord.Interaction):
        """Show Selenne Statistics"""
        await interaction.response.defer(thinking=True)

        cursor = self.bot.database.cursor(buffered=True)
        SQL = "SELECT * FROM `message`"
        cursor.execute(SQL)

        msg_count = len(cursor.fetchall())

        embed=discord.Embed(title = 'Selenne Stats', description = '**Version**: ***{0}*** - Bot Desarrollado por *DCS*'.format(self.bot.VERSION), color=__bot__.color)
        embed.add_field(name = 'Bot', value = '**Cumpleaños**: *{}*\n**Version**: *{}*\n**Owner**: ***{}***'.format(self.bot.BIRTH_DAY, self.bot.VERSION, self.bot.owner.display_name), inline=False)
        embed.add_field(name = 'Estadisticas', value = '**Nodo**: ***{}***\n**Servidores**: `{}`\n**Usuarios**: `{}`\n**Mensajes leidos**: `{}`'.format(self.bot.__node__, len(list(self.bot.guilds)), len(list(self.bot.users)), msg_count), inline=False)
        #len(list(self.bot.guilds))
        #len(list(self.bot.users))

        await interaction.followup.send(embed=embed, view=ReleasesView())
    