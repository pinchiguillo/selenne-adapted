from colorama import Fore, init
import json
import discord
from discord import activity
from discord import channel 
from discord.ext import commands
from discord.embeds import Embed
import asyncio
from datetime import datetime

from dcs.AI import reg
from dcs.functions import f_lib

class scheme():
    def __init__(self, bot):
        self.bot = bot
        main_config = reg.read('config.json')
    
    @commands.Cog.listener()
    async def on_message(message):
        pass
