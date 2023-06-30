import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

__EXTENSION_NAME__ = 'Slash_Sync'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(Slash_Sync(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#? Sample
class Slash_Sync(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def sync(self, ctx) -> None:
        if ctx.author.id != self.bot.oid:
            await ctx.send('You cant sync commands')
            return
        await self.bot.tree.sync()

        await ctx.send('Slash command syncronized')
        self.bot.logger.info('Slash command syncronized')
        self.bot.logger.info('Current slash commands: {}'.format(', '.join(self.bot.tree.get_commands())))