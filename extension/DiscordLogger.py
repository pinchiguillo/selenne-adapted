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
    COGS = []

    for cog in COGS:
        try: await bot.add_cog(cog(bot))
        except Exception as e: bot.logger.error('Failed to load cog: {}: {}'.format(cog.__name__, e))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

if not __EXTENSION_NAME__: __EXTENSION_NAME__ = os.path.splitext(os.path.basename(__file__))[0]

#! Extension Code

#? Sample
class AutoModLogger(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    #? AutoMod
    @commands.Cog.listener()
    def on_automod_rule_create(rule:discord.AutoModRule): pass
    
    @commands.Cog.listener()
    def on_automod_rule_update(rule:discord.AutoModRule): pass
    
    @commands.Cog.listener()
    def on_automod_rule_delete(rule:discord.AutoModRule): pass
    
    @commands.Cog.listener()
    def on_automod_action(execution:discord.AutoModAction): pass

class ChannelLogger(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    #? Channels
    @commands.Cog.listener()
    def on_guild_channel_delete(channel:discord.abc.GuildChannel): pass
    
    @commands.Cog.listener()
    def on_guild_channel_update(before:discord.abc.GuildChannel, after:discord.abc.GuildChannel): pass
    
    @commands.Cog.listener()
    def on_guild_channel_pins_update(channel, last_pin:datetime.datetime): pass
    
    @commands.Cog.listener()
    def on_private_channel_update(before:discord.GroupChannel, after:discord.GroupChannel): pass
    
    @commands.Cog.listener()
    def on_private_channel_pins_update(channel:discord.abc.PrivateChannel, last_pin:datetime.datetime): pass
    
    @commands.Cog.listener()
    def on_typing(channel:discord.abc.Messageable, user:Union[discord.User, discord.Member], when:datetime.datetime): pass
    
    @commands.Cog.listener()
    def on_raw_typing(payload:discord.RawTypingEvent): pass

class GuildLogger(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    #? Guilds
    @commands.Cog.listener()
    def on_guild_available(guild:discord.Guild): pass
    
    @commands.Cog.listener()
    def on_guild_unavailable(guild:discord.Guild): pass
    
    @commands.Cog.listener()
    def on_guild_join(guild:discord.Guild): pass
    
    @commands.Cog.listener()
    def on_guild_remove(guild:discord.Guild): pass
    
    @commands.Cog.listener()
    def on_guild_update(before:discord.Guild, after:discord.Guild): pass
    
    @commands.Cog.listener()
    def on_guild_emojis_update(guild, before:Sequence[discord.Emoji], after:Sequence[discord.Emoji]): pass
    
    @commands.Cog.listener()
    def on_guild_stickers_update(guild, before:Sequence[discord.GuildSticker], after:Sequence[discord.GuildSticker]): pass
    
    @commands.Cog.listener()
    def on_audit_log_entry_create(entry:discord.AuditLogEntry): pass
    
    @commands.Cog.listener()
    def on_invite_create(invite:discord.Invite): pass
    
    @commands.Cog.listener()
    def on_invite_delete(invite:discord.Invite): pass
    
    @commands.Cog.listener()
    def on_integration_create(integration:discord.Integration): pass
    
    @commands.Cog.listener()
    def on_guild_integrations_update(guild:discord.Guild): pass
    
    @commands.Cog.listener()
    def on_webhooks_update(channel:discord.abc.GuildChannel): pass
    
    @commands.Cog.listener()
    def on_raw_integration_delete(payload:discord.RawIntegrationDeleteEvent): pass
    
    #? Roles
    
    @commands.Cog.listener()
    def on_guild_role_create(role:discord.Role): pass
    
    @commands.Cog.listener()
    def on_guild_role_delete(role): pass
    
    @commands.Cog.listener()
    def on_guild_role_update(before:discord.Role, after:discord.Role): pass

class MemberLogger(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    #! @commands.Cog.listener()
    #? Members
    @commands.Cog.listener()
    
    def on_member_join(member:discord.Member): pass
    @commands.Cog.listener()
    
    def on_member_remove(member:discord.Member): pass
    @commands.Cog.listener()
    
    def on_raw_member_remove(payload:discord.RawMemberRemoveEvent): pass
    @commands.Cog.listener()
    
    def on_member_update(before:discord.Member, after:discord.Member): pass
    @commands.Cog.listener()
    
    def on_user_update(before, after): pass
    @commands.Cog.listener()
    
    def on_member_ban(guild, user): pass
    @commands.Cog.listener()
    
    def on_member_unban(guild, user): pass
    @commands.Cog.listener()
    
    def on_presence_update(before, after): pass

class MessageLogger(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    #! @commands.Cog.listener()
    #? Messages
    @commands.Cog.listener()
    def on_message(message:discord.Message): pass
    
    @commands.Cog.listener()
    def on_message_edit(before, after): pass
    
    @commands.Cog.listener()
    def on_message_delete(message): pass
    
    @commands.Cog.listener()
    def on_bulk_message_delete(messages:list[discord.Message]): pass
    
    @commands.Cog.listener()
    def on_raw_message_edit(payload:discord.RawMessageUpdateEvent): pass
    
    @commands.Cog.listener()
    def on_raw_message_delete(payload:discord.RawMessageDeleteEvent): pass
    
    @commands.Cog.listener()
    def on_raw_bulk_message_delete(payload:discord.RawBulkMessageDeleteEvent): pass
    

    #? Reactions
    @commands.Cog.listener()
    def on_reaction_add(reaction:discord.Reaction, user:Union[discord.Member, discord.User]): pass
    
    @commands.Cog.listener()
    def on_reaction_remove(reaction:discord.Reaction, user:Union[discord.Member, discord.User]): pass
    
    @commands.Cog.listener()
    def on_reaction_clear(message, reactions:list[discord.Reaction]): pass
    
    @commands.Cog.listener()
    def on_reaction_clear_emoji(reaction:discord.Reaction): pass
    
    @commands.Cog.listener()
    def on_raw_reaction_add(payload:discord.RawReactionActionEvent): pass
    
    @commands.Cog.listener()
    def on_raw_reaction_remove(payload:discord.RawReactionActionEvent): pass
    
    @commands.Cog.listener()
    def on_raw_reaction_clear(payload:discord.RawReactionClearEvent): pass
    
    @commands.Cog.listener()
    def on_raw_reaction_clear_emoji(payload:discord.RawReactionClearEmojiEvent): pass


    #? Threads
    @commands.Cog.listener()
    def on_thread_create(thread:discord.Thread): pass
    
    @commands.Cog.listener()
    def on_thread_join(thread:discord.Thread): pass
    
    @commands.Cog.listener()
    def on_thread_update(before, after): pass
    
    @commands.Cog.listener()
    def on_thread_remove(thread): pass
    
    @commands.Cog.listener()
    def on_thread_delete(thread): pass
    
    @commands.Cog.listener()
    def on_raw_thread_update(payload:discord.RawThreadUpdateEvent): pass
    
    @commands.Cog.listener()
    def on_raw_thread_delete(payload:discord.RawThreadDeleteEvent): pass
    
    @commands.Cog.listener()
    def on_thread_member_join(member:discord.ThreadMember): pass
    
    @commands.Cog.listener()
    def on_thread_member_remove(member:discord.ThreadMember): pass
    
    @commands.Cog.listener()
    def on_raw_thread_member_remove(payload:discord.RawThreadMembersUpdate): pass
