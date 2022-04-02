import discord
from discord.ext import commands

class core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog
    async def Sb(self, ctx):
        await ctx.send('Unable To Load')