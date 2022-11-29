import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands

import json

__EXTENSION_NAME__ = 'Leveling Roles'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(Leveling_core(bot))
    await bot.add_cog(Leveling_cog(bot))

    #await bot.tree.sync()

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class Leveling_core(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        cursor = self.bot.database.cursor(buffered=True)
        SQL = "INSERT INTO leveling_xp(guild, user, xp) SELECT '{}', '{}', 0  WHERE NOT EXISTS(SELECT 1 FROM leveling_xp WHERE guild = '{}' AND user = '{}');".format(message.guild.id, message.author.id, message.guild.id, message.author.id)
        try: cursor.execute(SQL)
        except Exception as e: 
            self.bot.logger.error('SQL ERROR on \'{}\' by \'{}\': {}'.format(message.guild.id, message.author.id, e))
        SQL = "UPDATE `leveling_xp` SET `xp`= `xp` + 1 WHERE `leveling_xp`.`guild` = '{}' AND `leveling_xp`.`user` = '{}';".format(message.guild.id, message.author.id)
        cursor.execute(SQL)
        self.bot.database.commit()

class Leveling_cog(discord.ext.commands.GroupCog, group_name = 'xprole', group_description = 'Level up in the server sending messages!'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = 'profile')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @discord.app_commands.command(name = 'top')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @discord.app_commands.command(name = 'administrate')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)




    administrateroup = app_commands.Group(name = 'administrate', description = 'Administrate XPRoles configuration in the server')

    @administrateroup.command(name= 'enable')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('You cant use this command', ephemeral=True)

    @administrateroup.command(name= 'config')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('You cant use this command', ephemeral=True)
    
    @administrateroup.command(name= 'role')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('You cant use this command', ephemeral=True)

    @administrateroup.command(name= 'purge')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('You cant use this command', ephemeral=True)