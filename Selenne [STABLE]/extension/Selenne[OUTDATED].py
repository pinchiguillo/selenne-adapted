import discord
from discord.ext import commands
import asyncio
import random

from dcs.functions import f_lib

class core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ai(self, ctx, *, args = None):
        if ctx.author.id == self.bot.owner:
            print('Reloading AI network')

class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = ['selenne', 'selene', 'sele']

    @commands.Cog.listener()
    async def on_message(self, message):
        bot = self.bot
        msg = message.content.lower()
        ch = message.channel

        mentioned = False
        
        #Detect Selenne mention (Convert to function)
        t1 = msg.split(' ')

        auth = False
        for name in self.name:
            if name in t1:
                auth = True

        if auth:
            mentioned = True

        #core
        if mentioned and not message.author.bot:
            if msg.lower in self.name:
                await ch.send('Hola!')
            elif 'hola' in msg:
                ans = [f'Hola {message.author.display_name}, como estas?', f'Hola {message.author.display_name}, que necesitas?', f'Como estas {message.author.display_name}?']
                await ch.send(ans[random.randint(0, len(ans) - 1)])
