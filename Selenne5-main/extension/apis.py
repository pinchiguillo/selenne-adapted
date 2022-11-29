from logging import exception
import Selenne
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import requests
import datetime

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'APIs'
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
    extension.database.path = 'db/system/startup.json'
    #extension.database.start()

    #? Slash Commands
    extension.slash_command = False

    #? Commands
    extension.cogs = [Nasa]


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
class Nasa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = 'REDACTED_NASA_API_KEY'
        #! https://api.nasa.gov/

    @discord.app_commands.command(name = 'apod')
    async def apod_command(self, interaction: discord.Interaction):
        """Get Picture of the day provided by NASA"""
        
        data = requests.get(f'https://api.nasa.gov/planetary/apod?api_key=REDACTED_NASA_API_KEY')

        embed=discord.Embed(title = 'Astronomical Picture of the Day' , description = data.json()['explanation'], color = self.bot.color)
        embed.set_image(url = 'https://apod.nasa.gov/apod/image/2208/M20-Trifid-Nebula-1024.jpg')
        try:embed.set_footer(text = f"Image provided by {data.json()['copyright']}")
        except: pass
        await interaction.response.send_message(embed=embed)

    #! DONT WORK
    #@discord.app_commands.command(name = 'earth')
    async def earth_command(self, interaction: discord.Interaction):
        """Get a picture of the earth in a given coordinates"""
        
        #data = requests.get(f'https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&api_key=REDACTED_NASA_API_KEY')

        #embed=discord.Embed(title = 'Astronomical Picture of the Day' , description = data.json()['explanation'], color = self.bot.color)
        #embed.set_image(url = 'https://apod.nasa.gov/apod/image/2208/M20-Trifid-Nebula-1024.jpg')
        #embed.set_footer(text = f"Image provided by {data.json()['copyright']}")
        #await interaction.response.send_message(embed=embed)
        await interaction.response.send_message('Under Mantenience')


class Default_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
