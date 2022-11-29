import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import string
import random

allowed_characters = string.ascii_letters + string.digits

__EXTENSION_NAME__ = 'promocode_handler'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(Promocode_cog(bot))

    #await bot.tree.sync()

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class Promocode_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot
        global database
        database = self.bot.database

    @discord.app_commands.command(name = 'addpromocode')
    @discord.app_commands.describe()
    async def add_promocode_cmd(self, interaction: discord.Interaction):
        """Create a promocode"""

        await interaction.response.send_modal(Create_Promocode())

    @discord.app_commands.command(name = 'promocode')
    @discord.app_commands.describe()
    async def promocode_cmd(self, interaction: discord.Interaction):
        """Redeem code"""

        await interaction.response.send_modal(Promocode())

class Create_Promocode(discord.ui.Modal, title = 'Redeem code'):
    
    _code_ = ''
    for c in range(16):
        _code_ += random.choice(allowed_characters)

    code = discord.ui.TextInput(
        label = 'Code',
        max_length = 16,
        default = _code_

    )
    uses = discord.ui.TextInput(
        label = 'Uses',
        max_length = 16,
        default = 1

    )

    async def on_submit(self, interaction: discord.Interaction):

        cursor = database.cursor(buffered=True)
        cursor.execute("INSERT INTO `promocodes` (`code`, `creation_date`, `expiration_date`, `last_use`, `uses_remaining`) VALUES ('{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '{}');".format(self.code.value, self.uses.value))
        database.commit()

        await interaction.response.send_message(f'Your code: , {self.code.value}, uses: {self.uses.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

class Promocode(discord.ui.Modal, title = 'Redeem code'):
    
    code = discord.ui.TextInput(
        label = 'Code',
        placeholder = '',
    )

    async def on_submit(self, interaction: discord.Interaction):
        cursor = database.cursor(buffered=True)
        cursor.execute("SELECT * FROM `promocodes` WHERE `code` LIKE '{}'".format(self.code.value))
        codes = cursor.fetchall()

        if len(codes) == 0: await interaction.response.send_message('Invalid promocode', ephemeral=True)

        cursor.execute("UPDATE promocodes SET uses_remaining = uses_remaining - 1 WHERE `code` LIKE '{}';".format(self.code.value))
        cursor.execute("DELETE FROM promocodes WHERE uses_remaining <= 0;".format(self.code.value))
        database.commit()

        await interaction.response.send_message('Valid promocode', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong {}'.format(error), ephemeral=True)
