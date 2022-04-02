import discord
from discord.ext import commands

class esssentials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong')
    
    @commands.command()
    async def bye(self, ctx):
        if ctx.author.id == 000000000000000000:
            await ctx.reply('bye!')
            exit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(ctx, *, args):
        await ctx.send(args)

class on_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))
