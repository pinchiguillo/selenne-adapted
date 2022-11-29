import Selenne
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'WA Project Game'
    extension.version = 'Pre-Alfa'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/system/startup.json'
    #extension.database.start()

    #? Slash Commands
    extension.slash_command = False

    #? Commands
    extension.cogs = [WAP_Core]

    #? Config
    extension.config.enabled = False
    #extension.config.name = '' #? Default: extension.name
    extension.config.premium = False
    #extension.config.attr_name = '' #? Default: extension.name
    extension.config.config_dict = {}

    #! DO NOT TOUCH
    #? Check Compatibility
    await extension.check_compatibility()
    await extension.load_cogs()
    await extension.load_views()
    await extension.add_help()
    await extension.sync()
    extension.config.sync()
    await extension.loaded()
async def teardown(bot):
    await extension.remove_help()
    await extension.unloaded()

#! Extension Code

#? Sample
class WAP_Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command()
    @discord.app_commands.describe()
    async def wa(self, interaction: discord.Interaction):
        """Comando principal del juego itegrado: WA Project Game"""
        cfg = await extension.config.get(interaction.guild.id)
        cfg = cfg['allow_wap']
        if not cfg['enabled']:
            await interaction.response.send_message('WA Project Game is not enabled, use /config to enable it', ephemeral=True)

        embed, view = __WAP_TOOLS__.user_menu(interaction.user)
        await interaction.response.send_message(embed=embed, view=view)

#! CMDS: 
# wafriends
# waguild
# wapvp

class __WAP_TOOLS__():
    def user_menu(user):
        embed = extension.default_embed
        embed.title = f'Tarjeta de Usuario de {user.display_name}'
        embed.description = '''
**Nivel**: `{}`
**Clase**: `{}`
**Gremio**: *{}*

**STATS**
'''
        return embed, None
    def inventory_menu(): pass
    def friends_menu(): pass
    def guild_menu(): pass
    def item_menu(): pass
    def crafting_menu(): pass
    def pvp_menu(): pass
    def mail_menu(): pass