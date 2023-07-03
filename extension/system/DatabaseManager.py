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
class Default_Listeners_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    #! @commands.Cog.listener()
    #? App Commands
    def on_raw_app_command_permissions_update(payload:discord.RawAppCommandPermissionsUpdateEvent): pass
    def on_app_command_completion(interaction:discord.Interaction, command:Union[discord.app_commands.Command, discord.app_commands.ContextMenu]): pass
    
    #? AutoMod
    def on_automod_rule_create(rule:discord.AutoModRule): pass
    def on_automod_rule_update(rule:discord.AutoModRule): pass
    def on_automod_rule_delete(rule:discord.AutoModRule): pass
    def on_automod_action(execution:discord.AutoModAction): pass

    #? Channels
    def on_guild_channel_delete(channel:discord.abc.GuildChannel): pass
    def on_guild_channel_update(before:discord.abc.GuildChannel, after:discord.abc.GuildChannel): pass
    def on_guild_channel_pins_update(channel, last_pin:datetime.datetime): pass
    def on_private_channel_update(before:discord.GroupChannel, after:discord.GroupChannel): pass
    def on_private_channel_pins_update(channel:discord.abc.PrivateChannel, last_pin:datetime.datetime): pass
    def on_typing(channel:discord.abc.Messageable, user:Union[discord.User, discord.Member], when:datetime.datetime): pass
    def on_raw_typing(payload:discord.RawTypingEvent): pass

    #? Conexion
    def on_connect(): pass
    def on_disconnect(): pass
    def on_shard_connect(shard_id:int): pass
    def on_shard_disconnect(shard_id:int): pass

    #? Debug
    def on_error(event:str, *args, **kwargs): pass
    def on_socket_event_type(event_type:str): pass
    def on_socket_raw_receive(msg:str): pass

    #? Gateway
    def on_ready(): pass
    def on_resumed(): pass
    def on_shard_ready(shard_id): pass
    def on_shard_resumed(shard_id): pass

    #? Guilds
    def on_guild_available(guild:discord.Guild): pass
    def on_guild_unavailable(guild:discord.Guild): pass
    def on_guild_join(guild:discord.Guild): pass
    def on_guild_remove(guild:discord.Guild): pass
    def on_guild_update(before:discord.Guild, after:discord.Guild): pass
    def on_guild_emojis_update(guild, before:Sequence[discord.Emoji], after:Sequence[discord.Emoji]): pass
    def on_guild_stickers_update(guild, before:Sequence[discord.GuildSticker], after:Sequence[discord.GuildSticker]): pass
    def on_audit_log_entry_create(entry:discord.AuditLogEntry): pass
    def on_invite_create(invite:discord.Invite): pass
    def on_invite_delete(invite:discord.Invite): pass
    def on_integration_create(integration:discord.Integration): pass
    def on_guild_integrations_update(guild:discord.Guild): pass
    def on_webhooks_update(channel:discord.abc.GuildChannel): pass
    def on_raw_integration_delete(payload:discord.RawIntegrationDeleteEvent): pass

    #? Interactios
    def on_interaction(interaction:discord.Interaction): pass

    #? Members
    def on_member_join(member:discord.Member): pass
    def on_member_remove(member:discord.Member): pass
    def on_raw_member_remove(payload:discord.RawMemberRemoveEvent): pass
    def on_member_update(before:discord.Member, after:discord.Member): pass
    def on_user_update(before, after): pass
    def on_member_ban(guild, user): pass
    def on_member_unban(guild, user): pass
    def on_presence_update(before, after): pass

    #? Messages
    def on_message(message:discord.Message): pass
    def on_message_edit(before, after): pass
    def on_message_delete(message): pass
    def on_bulk_message_delete(messages:list[discord.Message]): pass
    def on_raw_message_edit(payload:discord.RawMessageUpdateEvent): pass
    def on_raw_message_delete(payload:discord.RawMessageDeleteEvent): pass
    def on_raw_bulk_message_delete(payload:discord.RawBulkMessageDeleteEvent): pass

    #? Reactions
    def on_reaction_add(reaction:discord.Reaction, user:Union[discord.Member, discord.User]): pass
    def on_reaction_remove(reaction:discord.Reaction, user:Union[discord.Member, discord.User]): pass
    def on_reaction_clear(message, reactions:list[discord.Reaction]): pass
    def on_reaction_clear_emoji(reaction:discord.Reaction): pass
    def on_raw_reaction_add(payload:discord.RawReactionActionEvent): pass
    def on_raw_reaction_remove(payload:discord.RawReactionActionEvent): pass
    def on_raw_reaction_clear(payload:discord.RawReactionClearEvent): pass
    def on_raw_reaction_clear_emoji(payload:discord.RawReactionClearEmojiEvent): pass
    
    #? Roles
    def on_guild_role_create(role:discord.Role): pass
    def on_guild_role_delete(role): pass
    def on_guild_role_update(before:discord.Role, after:discord.Role): pass

    #? Scheduled Events
    def on_scheduled_event_create(event:discord.ScheduledEvent): pass
    def on_scheduled_event_delete(event:discord.ScheduledEvent): pass
    def on_scheduled_event_update(before, after): pass
    def on_scheduled_event_user_add(event, user): pass
    def on_scheduled_event_user_remove(event, user): pass

    #? Stages
    def on_stage_instance_create(stage_instance:discord.StageInstance): pass
    def on_stage_instance_delete(stage_instance:discord.StageInstance): pass
    def on_stage_instance_update(before:discord.StageInstance, after:discord.StageInstance): pass

    #? Threads
    def on_thread_create(thread:discord.Thread): pass
    def on_thread_join(thread:discord.Thread): pass
    def on_thread_update(before, after): pass
    def on_thread_remove(thread): pass
    def on_thread_delete(thread): pass
    def on_raw_thread_update(payload:discord.RawThreadUpdateEvent): pass
    def on_raw_thread_delete(payload:discord.RawThreadDeleteEvent): pass
    def on_thread_member_join(member:discord.ThreadMember): pass
    def on_thread_member_remove(member:discord.ThreadMember): pass
    def on_raw_thread_member_remove(payload:discord.RawThreadMembersUpdate): pass

    #? Voice
    def on_voice_state_update(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState): pass

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Default_Commands_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot
    
    @discord.app_commands.command(name = '')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    subgroup = app_commands.Group(name = 'sub-sub command', description = 'Description')

    @subgroup.command(name = '')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

class Default_CommandGroup_cog(discord.ext.commands.GroupCog, group_name = 'name', group_description = 'Description'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = '')
    @discord.app_commands.describe()
    async def defa(self, interaction: discord.Interaction):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)

    subgroup = app_commands.Group(name = 'sub-sub command', description = 'Description')

    @subgroup.command(name = '')
    @discord.app_commands.describe()
    async def dam_calendar_update(self, interaction: discord.Interaction, yaml: discord.Attachment):
        """Description"""
        await interaction.response.send_message('Not avilable', ephemeral=True)
