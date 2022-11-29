import asyncio
import Selenne
import discord
from discord.ext import commands

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'ManagementLib'
    extension.version = '1.0'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json_dir'
    extension.database.path = 'db/system/guild'
    extension.database.start()


    #? Commands
    extension.cogs = [ManagementTools]


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

default_config = {
    'prefix': 's.',
    'allowed_features': [],
    'forbidden_features': [],
    'channels': {
        'news': None,
        'log': None,
        'suggestions': None
        }
}

#? Sample
class ManagementTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.command()
    async def config(self, ctx, args = None):
        data = extension.database.get(ctx.guild.id)
        if not data:
            await ctx.send('Gracias por utilizar Selenne, estamos realizando los ultimos ajustes.')
            extension.database.create(ctx.guild.id, default_config)
            await asyncio.sleep(1)
            await ctx.send(f'Vuelve a usar `{self.bot.main_prefix}config`')
        else:
            await ctx.send(data)

    @commands.command()
    async def enable(self, ctx, args = None):
        pass

    @commands.command()
    async def disable(self, ctx, args = None):
        pass
