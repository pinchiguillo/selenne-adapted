import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional

__EXTENSION_NAME__ = 'Configuration'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    await bot.add_cog(Configuration_cog(bot))


async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class Configuration_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = 'config')
    @discord.app_commands.describe()
    async def configuration(self, interaction: discord.Interaction):
        """Configure the Selenne features in your guild"""

        embed = discord.Embed(title = 'Selenne Configuration Pannel', description = 'Click on the feature that you want to manage.', color = self.bot.color)

        #! ECR = Extra configuration required
        temp_data = {
            'F1': {
                'enabled': True,
                'ecr': False
            },
            'F2': {
                'enabled': False,
                'ecr': False
            },
            'F3': {
                'enabled': True,
                'ecr': True
            },
            'F4': {
                'enabled': False,
                'ecr': True
            },
            'F5': {
                'enabled': True,
                'ecr': False
            },
        }

        await interaction.response.send_message(embed=embed, view=ConfigurationView(temp_data), ephemeral=True)



class ConfigurationView(discord.ui.View):
    def __init__(self, data:dict):
        super().__init__()
        self.timeout = 600

        self.data = data


        #? Selector Classes
        class FeatureSelector(discord.ui.Select):
            def __init__(self, options):
                
                self.__options__ = options

                #! DB
                ex_data = {
                    'F4': {},
                }
                #! DB

                __options__ = []

                for opt in options:
                    if options[opt]['enabled']:
                        if options[opt]['ecr']:
                            if opt in ex_data.keys(): #! DB Call
                                __options__.append(discord.SelectOption(label = opt, emoji='🟩', value = opt))
                            else:
                                __options__.append(discord.SelectOption(label = opt, emoji='🟧', value = opt))

                        else:
                            __options__.append(discord.SelectOption(label = opt, emoji='🟩', value = opt))
                    else:
                        __options__.append(discord.SelectOption(label = opt, emoji='🟥', value = opt))

                super().__init__(placeholder='Features', min_values=1, max_values=1, options=__options__)

                        
            async def callback(self, interaction: discord.Interaction):

                if self.__options__[self.values[0]]['enabled']: self.__options__[self.values[0]]['enabled'] = False
                elif not self.__options__[self.values[0]]['enabled']: self.__options__[self.values[0]]['enabled'] = True
                
                await interaction.response.edit_message(view=ConfigurationView(self.__options__))
                    
        self.add_item(FeatureSelector(data))

    @discord.ui.button(label = 'Save', style=discord.ButtonStyle.green, disabled=False, row=1) #! Remove disabled
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()

        self.data

        embed = interaction.message.embeds[0]
        embed.description = 'Config Closed'

        await interaction.response.edit_message(embed=embed, view=None)
