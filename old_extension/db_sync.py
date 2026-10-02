import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional

import mysql.connector

__EXTENSION_NAME__ = 'Database Sync'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    #? Load the AFK changes to the database
    #await database_sync_core.__sync_db_guilds__(bot)
    #await database_sync_core.__sync_db_channels__(bot)
    bot.logger.info('All databases synced')

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
        SQL = "INSERT INTO `guild` (`id`, `name`, `owner`, `creation_date`, `index_date`, `update_date`, `premium`, `lang`) SELECT %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '0', 'es-ES' FROM `guild` WHERE NOT EXISTS (SELECT id FROM guild WHERE id = %s) LIMIT 1;"
        cursor.execute(SQL, (guild.id, guild.name, guild.owner_id, guild.created_at, guild.id))
        self.bot.database.commit()

    @commands.Cog.listener()
    async def on_guild_update(self, before:discord.Guild, after:discord.Guild):
        cursor = self.bot.database.cursor(buffered=True)
        SQL = "UPDATE `guild` SET `name` = %s, `owner` = %s WHERE `guild`.`id` = %s;"
        cursor.execute(SQL, (after.name, after.owner_id, after.id))
        self.bot.database.commit()
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel:discord.TextChannel): #discord.TextChannel and discord.VoiceChannel
        cursor = self.bot.database.cursor(buffered=True)
        SQL = "INSERT INTO `channel` (`guild`, `id`) VALUES (%s, %s);"
        cursor.execute(SQL, (channel.guild.id, channel.id))
        self.bot.database.commit()

class database_sync_core(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot
        
        self.__sync_db_guilds__.start()
        self.__sync_db_channels__.start()

    @tasks.loop(seconds=60.0, count=1)
    async def __sync_db_guilds__(self): #(self, ctx)
        self.bot.logger.info('DB SYNC: Syncing guilds...')
        
        duplicates = -1
        for x, guild in enumerate(self.bot.guilds):
            try:
                cursor = self.bot.database.cursor(buffered=True)                
                
                SQL = """
INSERT INTO `guild` (`id`, `name`, `owner`, `creation_date`, `index_date`, `update_date`, `premium`, `lang`) 
VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '0', 'es-ES');
"""
                
                cursor.execute(SQL, (guild.id, guild.name, guild.owner_id, guild.created_at))
                self.bot.database.commit()
                
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    duplicates += 1
                else:
                    self.bot.logger.error('DB SYNC: Fail to sync guild {}: {}'.format(x, e))
                    self.bot.logger.debug('DB SYNC: SQL: {}'.format(SQL))
        self.bot.logger.info('DB SYNC: {} guilds added/updated'.format(x-duplicates))

    @__sync_db_guilds__.before_loop
    async def __before_sync_db_guilds__(self):
        await self.bot.wait_until_ready()

    #!
    @tasks.loop(seconds=60.0)
    async def __sync_db_channels__(self): #(self, ctx)
        self.bot.logger.info('DB SYNC: Syncing channels...')

        duplicates = -1
        for x, guild in enumerate(self.bot.guilds):
            for channel in list(guild.channels):
                try:
                    cursor = self.bot.database.cursor(buffered=True)
                    SQL = "INSERT INTO `channel` (`guild`, `id`) VALUES (%s, %s);"
                    cursor.execute(SQL, (guild.id, channel.id))
                    self.bot.database.commit()
                except Exception as e:
                    if 'Duplicate entry' in str(e):
                        duplicates += 1
                    else:
                        self.bot.logger.error('DB SYNC: Fail to sync channel {}: {}'.format(x, e))
                        self.bot.logger.debug('DB SYNC: SQL: {}'.format(SQL))
        self.bot.logger.info('DB SYNC: {} channels added/updated'.format(type(x - duplicates)))

    @__sync_db_channels__.before_loop
    async def __before_sync_db_channels__(self):
        await self.bot.wait_until_ready()
