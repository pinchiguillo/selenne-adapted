import Selenne
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import json

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Genshin Tools'
    extension.version = 'Alfa'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/genshin.json'
    #extension.database.start()

    #? Slash Commands
    extension.slash_command = False

    #? Commands
    extension.cogs = [Genshin]


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
class Genshin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name = 'genshin')
    @discord.app_commands.describe(
        build = 'Search for Genshin Character Builds',
        information = 'Search for Artifacts and Characters information'
    )
    async def genshin_command(self, interaction: discord.Interaction, build:Optional[str] = None, information:Optional[str] = None):
        """Tools for make your Genshin gameplay easier"""

        if build:
            await extension.load_db()
            builds = extension.database.data['builds']
            
            data = False
            for bld in builds:
                if build.lower() in builds[bld]['aliases']: 
                    name = bld
                    data = builds[bld]

            if not data:
                await interaction.response.send_message(f'Could not find the build of ***{build}*** in the database') 
                return

            #? Build Menu
            
            embed = discord.Embed(title = f'Genshin Builds - {name}', description = '**Cargando...**', color=self.bot.color)
            embed.description = str('⭐️' * data['stars'])

            #? Adding data
            menus = dict()
            for __build__ in data['build']:
                menus[__build__] = {
                    'emoji': '🔤',
                    'build': data['build'][__build__]
                }
            main_menu = data['recomended_build']

            embed = buildembed(embed, menus[main_menu]['build'])
            await interaction.response.send_message(embed=embed, view=GenshinBuildView(menus, data['recomended_build'], embed))

            #!----------------------------------------------------------------

            #await interaction.response.send_message(embed=embed)

        elif information: await interaction.response.send_message(f'Genshin Information for ***{information}***')
        else: await interaction.response.send_message(f'Selenne will have more Gensin Tools Soon!')

#! -----------------------------------------------------------------------------
def buildembed(embed, build):
    embed.clear_fields()
    
    embed.add_field(name = 'Armas', value=build['weapons'], inline=False)
    embed.add_field(name = 'Artefactos', value=build['artifacts']['sets'], inline=False)
    embed.add_field(name = 'Estadisticas Artefactos', value=build['artifacts']['stats'], inline=False)
    embed.add_field(name = 'Estadisticas Secundarias', value=build['artifacts']['stats-priority'], inline=False)
    embed.add_field(name = 'Equipos', value=build['teams'], inline=False)

    return embed

class Dropdown(discord.ui.Select):
    def __init__(self, menus, active_menu,embed):
        self.menus = menus
        self.embed = embed
        options = []

        for page in menus.keys():
            if page == active_menu: options.append(discord.SelectOption(label=page, emoji=menus[page]['emoji'], default=True))
            else: options.append(discord.SelectOption(label=page, emoji=menus[page]['emoji']))

        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        embed = buildembed(self.embed, self.menus[self.values[0]]['build'])
        await interaction.response.edit_message(embed=embed, view=GenshinBuildView(self.menus, self.values[0], self.embed))

class GenshinBuildView(discord.ui.View):
    def __init__(self, menus, active_menu, embed):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(menus, active_menu, embed))
