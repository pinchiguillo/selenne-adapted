import Selenne
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import os
import json

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Config Tools'
    extension.version = '2.3'
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
    extension.cogs = [Configuration_GUI]


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
class Configuration_GUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not os.path.exists(os.path.join('db/guilds', f'{guild.id}.json')):
            with open(os.path.join('db/guilds', f'{guild.id}.json'), 'w') as f:
                json.dump(dict(), f)



    @discord.app_commands.command()
    @discord.app_commands.describe()
    async def config(self, interaction: discord.Interaction):
        """Configure Selenne"""

        with open(os.path.join('db/guilds', f'{interaction.guild.id}.json'), 'r') as f:
            data = json.load(f)

        embed = extension.default_embed
        embed.title = 'Interfaz de configuracion grafica de Selenne'
        if data['premium']: embed.description = 'Tu servidor es **premium**'
        else: embed.description = 'Tu servidor **no es premium**'
        await interaction.response.send_message(embed=embed, view=ConfigView(data))

class Dropdown(discord.ui.Select):
    def __init__(self, data):
        self.data = data
        # Set the options that will be presented inside the dropdown
        options = []

        for option in self.data:
            if isinstance(data[option], dict):
                try:
                    if data[option]['request_premium'] and not data['premium']: options.append(discord.SelectOption(label = self.data[option]['display_name'], value=f'$premium_request${option}', description = 'Esta es una opcion premium', emoji = '🚫'))
                    else:
                        if self.data[option]['enabled']: options.append(discord.SelectOption(label = self.data[option]['display_name'], value=option, description = 'Habilitado', emoji = '🟩'))
                        elif not self.data[option]['enabled']: options.append(discord.SelectOption(label = data[option]['display_name'], value=option, description = 'Deshabilitado', emoji = '🟥'))
                        else: options.append(discord.SelectOption(label = self.data[option]['display_name'], value=data[option], description = 'Habilitado, Sin Configurar', emoji = '🟧'))
                except Exception as e: extension.bot.log.info(e)

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Opciones', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if '$premium_request$' in self.values[0]:
            await interaction.response.send_message('Esta es una opcion premium, mejora el servidor para poder usarla', ephemeral=True)
            return
        else:
            if self.data[self.values[0]]['enabled']: self.data[self.values[0]]['enabled'] = False
            elif not self.data[self.values[0]]['enabled']: self.data[self.values[0]]['enabled'] = True

            await interaction.response.edit_message(view=ConfigView(self.data))

            with open(os.path.join('db/guilds', f'{interaction.guild.id}.json'), 'w') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        


class ConfigView(discord.ui.View):
    def __init__(self, data):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(data))
