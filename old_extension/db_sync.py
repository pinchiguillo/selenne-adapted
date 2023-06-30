import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

__EXTENSION_NAME__ = 'Guild Manager'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(database_listeners_cog(bot))
    await bot.add_cog(database_sync_core(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class database_listeners_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        cursor = self.bot.database.cursor(buffered=True)
        SQL = "INSERT INTO `guild` (`id`, `name`, `owner`, `creation_date`, `index_date`, `update_date`, `premium`, `lang`) SELECT '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '0', 'es-ES' FROM `guild` WHERE NOT EXISTS (SELECT id FROM guild WHERE id = '{}') LIMIT 1;".format(guild.id, guild, guild.owner.id, guild.created_at, guild.id)
        cursor.execute(SQL)
        self.bot.database.commit()

    @commands.Cog.listener()
    async def on_guild_update(self, before:discord.Guild, after:discord.Guild):
        cursor = self.bot.database.cursor(buffered=True)
        SQL = "UPDATE `guild` SET `name` = '{}', `owner` = '{}' WHERE `guild`.`id` = '{}';".format(after.name, after.owner.id, after.id)
        cursor.execute(SQL)
        self.bot.database.commit()
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel:discord.TextChannel): #discord.TextChannel and discord.VoiceChannel
        cursor = self.bot.database.cursor(buffered=True)
        SQL = "INSERT INTO `channel` (`guild`, `id`) VALUES ('{}', '{}');".format(channel.guild.id, channel.id)
        cursor.execute(SQL)
        self.bot.database.commit()

class database_sync_core(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @commands.command()
    async def __sync_db_guilds__(self, ctx):
        await ctx.send('Syncing database...')

        try:
            for x, guild in enumerate(self.bot.guilds):
                cursor = self.bot.database.cursor(buffered=True)
                SQL = "INSERT INTO `guild` (`id`, `name`, `owner`, `creation_date`, `index_date`, `update_date`, `premium`, `lang`) SELECT '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '0', 'es-ES' WHERE NOT EXISTS(SELECT 1 FROM `guild` WHERE `id` = '{}');INSERT INTO `guild` (`id`, `name`, `owner`, `creation_date`, `index_date`, `update_date`, `premium`, `lang`) SELECT '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '0', 'es-ES' WHERE NOT EXISTS(SELECT 1 FROM `guild` WHERE `id` = '{}');".format(guild.id, str(guild).replace("'", r"\'"), guild.owner.id, guild.created_at, guild.id)
                cursor.execute(SQL)
                self.bot.database.commit()
                print('{} registered'.format(x))
                
            await ctx.send('Sync complete')
        except Exception as e:
            await ctx.send('```{}``` ```{}```'.format(e, SQL))

    @commands.command()
    async def __sync_db_channels__(self, ctx):
        await ctx.send('Syncing database...')

        try:
            for x, guild in enumerate(self.bot.guilds):
                for channel in list(guild.channels):
                    cursor = self.bot.database.cursor(buffered=True)
                    SQL = "INSERT INTO `channel` (`guild`, `id`) VALUES ('{}', '{}');".format(guild.id, channel.id)
                    cursor.execute(SQL)
                    self.bot.database.commit()
            await ctx.send('Sync complete')
        except Exception as e:
            #await ctx.send('```{}``` ```{}```'.format(e, SQL))
            pass
