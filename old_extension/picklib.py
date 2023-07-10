import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional

__EXTENSION_NAME__ = 'Picklib'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(PickLib_cog(bot))


async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class PickLib_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

        self.__guild__ = 866477454468841472
        self.__channel__ = 927376122281357322

        self.__references__ = {
            'instagram': 'https://www.instagram.com/',
            'pixiv': 'https://www.pixiv.net/en/artworks/',
            'twitter': 'https://twitter.com/',
            'pinterest': 'https://pin.it',
            'youtube': 'https://www.youtube.com/',
        }

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return

        if not (message.guild.id == self.__guild__ and message.channel.id == self.__channel__): return

        data = message.content.split('https')
        ndata = list()

        for d in data:
            if d.startswith('://'): ndata.append('https{}'.format(d))

        if len(ndata) == 0: 
            await message.reply('That is not a link, and PickLib only support image links', delete_after=10)
            return
        
        for link in ndata:

            if not 'https://' in link:
                await message.reply('That is not a link, and PickLib only support image links', delete_after=10)
                continue

            platform = None
            for __platform__ in self.__references__:
                if link.startswith(self.__references__[__platform__]): platform = __platform__

            cursor = self.bot.database.cursor(buffered=True)
            cursor.execute("SELECT * FROM `picklib` WHERE `link` LIKE '{}'".format(link))
            db_existence = cursor.fetchall()
            if len(db_existence) != 0:
                await message.reply('Link alrready in database', delete_after=10)
            else:
                SQL = "INSERT INTO `picklib` (`platform`, `link`, `downloaded`, `fetch_date`) VALUES ('{}', '{}', '0', CURRENT_TIMESTAMP);".format(platform, link)
                cursor.execute(SQL)
                self.bot.database.commit()

                await message.reply('Link Fetched', delete_after=10)

        
        await message.delete()

    @discord.app_commands.command(name = 'picklib')
    @discord.app_commands.describe()
    async def picklib_command(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

#! DATE UPLOADS: SELECT * FROM `picklib` WHERE `fetch_date` >= '2022-12-31 00:00:00'