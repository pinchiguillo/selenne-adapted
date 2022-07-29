from Tools.extension import Extension
import discord

#? Configuration
async def setup(bot):
    global extension
    extension = Extension(bot)
    
    #? Basic Info
    extension.name = 'Teemplate'
    extension.version = 'Alfa'
    extension.bot_version = 'Selenne 5.2'
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}

    #? Cogs
    extension.cogs = []
    extension.views = []


    #! DO NOT TOUCH
    #? Check Compatibility
    await extension.check_compatibility()
    await extension.load_cogs()
    await extension.load_views()
    await extension.add_help()
    await extension.loaded()
async def teardown(bot):
    await extension.remove_help()
    await extension.unloaded()

#! Extension Code

#? Sample
class Default_cog(discord.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.commands.command()
    async def extension(self, ctx, args = None):
        pass

    @discord.commands.Cog.listener()
    async def on_message(self, message):
        pass
