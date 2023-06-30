import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

__EXTENSION_NAME__ = 'dcs'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(DCS_Public_Downloads_cog(bot))
    await bot.add_cog(DCS_Private_cog(bot))

    #await bot.tree.sync()

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class DCS_Public_Downloads_cog(discord.ext.commands.GroupCog, group_name='download', group_description='Various media downloaders'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    youtube_group = app_commands.Group(name='youtube', description='Youtube download tools')
    pixiv_group = app_commands.Group(name='pixv', description='Pixiv download tools')

    @youtube_group.command(name= 'video')
    @discord.app_commands.describe(
        url = 'The url of the video you want to download'
    )
    async def download_youtube_video(self, interaction: discord.Interaction, url:str):
        """Downloads a youtube video with maximun cualtity"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @youtube_group.command(name= 'audio')
    @discord.app_commands.describe(
        url = 'The url of the audio you want to download'
    )
    async def download_youtube_audio(self, interaction: discord.Interaction, url:str):
        """Downloads a youtube audio with maximun cualtity"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @discord.app_commands.command(name= 'instagram')
    @discord.app_commands.describe(
        url = 'The url of the post you want to download'
    )
    async def download_instagram(self, interaction: discord.Interaction, url:str):
        """Downloads an instagram post"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @pixiv_group.command(name= 'post')
    @discord.app_commands.describe(
        url = 'The url of the post you want to download',
        id = 'The id of the post you want to download'
    )
    async def download_pixiv_post(self, interaction: discord.Interaction, url:Optional[str] = None, id:Optional[int] = None):
        """Downloads a pixiv post"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @pixiv_group.command(name= 'account')
    @discord.app_commands.describe(
        url = 'The url of the account you want to download all picks',
        id = 'The id of the account you want to download all picks'
    )
    async def download_pixiv_account(self, interaction: discord.Interaction, url:Optional[str] = None, id:Optional[int] = None):
        """Downloads all the posts from an account"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    @pixiv_group.command(name= 'daily_top')
    @discord.app_commands.describe()
    async def download_pixiv_dailytop(self, interaction: discord.Interaction):
        """Downloads the top 3 daily picks"""
        await interaction.response.send_message('Not avilable', ephemeral=True)


class DCS_Private_cog(discord.ext.commands.GroupCog, group_name='dcs', group_description='DCS private tools'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        pass
    
    picklib_group = app_commands.Group(name='piclib', description='DCS picklib management')
    admin_group = app_commands.Group(name='admin', description='DCS admin management')

    @picklib_group.command(name= 'short')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Shorts all the saved metadata"""
        await interaction.response.send_message('Not avilable')

    @picklib_group.command(name= 'get')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Get all the saved metadata"""
        await interaction.response.send_message('Not avilable')

    @picklib_group.command(name= 'download')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Get full traceback of the metadata"""
        await interaction.response.send_message('Not avilable')

    @admin_group.command(name= 'status')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Shows the DCS Network Status"""
        await interaction.response.send_message('Not avilable')
