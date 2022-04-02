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

import importlib

os = importlib.import_module("schemes.selenne")

os.run()