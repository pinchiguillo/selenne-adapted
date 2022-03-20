#Experimental Bot: Selenne

#Import nextcord
import nextcord
from nextcord import activity
from nextcord import channel 
from nextcord.ext import commands
from nextcord.embeds import Embed

#Import utils
import os

#Private Libraries

bot = commands.Bot(command_prefix= 's.')

@bot.event
async def on_ready():
    print(f'BOT ONLINE')

import cmd
for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            bot.load_extension(f"modules.{folder}.cog")
    
from config import TOCKEN
bot.run(TOCKEN)