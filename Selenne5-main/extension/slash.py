import Selenne
import discord
from discord.ext import commands
from typing import Optional

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Slash Commands'
    extension.version = 'Alfa'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Slash Commands
    extension.slash_command = False

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/system/startup.json'
    #extension.database.start()


    #? Commands
    extension.cogs = [Slash_cog]


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
class Slash_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @discord.app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        """Says hello!"""
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')

    #? ADD
    @discord.app_commands.command()
    @discord.app_commands.describe(
        first_value='The first value you want to add something to',
        second_value='The value you want to add to the first value',
    )
    async def add(self, interaction: discord.Interaction, first_value: int, second_value: int):
        """Adds two numbers together."""
        await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

    #? Hybrid Commands
    @commands.hybrid_command(name="ping")
    async def ping_command(self, ctx: commands.Context):
        """Check if Selenne is online"""
        await ctx.send('Pong!')

    
    @discord.app_commands.command()
    @discord.app_commands.rename(text_to_send='text') #! Renames A variable
    @discord.app_commands.describe(text_to_send='Text to send in the current channel')
    async def send(self, interaction: discord.Interaction, text_to_send: str):
        """Sends the text into the current channel."""
        await interaction.response.send_message(text_to_send)

    @discord.app_commands.command()
    @discord.app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
    async def joined(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        """Says when a member joined."""
        # If no member is explicitly provided then we use the command user here
        member = member or interaction.user

        # The format_dt function formats the date time into a human readable representation in the official client
        await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')