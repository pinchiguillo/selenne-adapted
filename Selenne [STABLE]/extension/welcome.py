import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_listener(on_member_join)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'Welcome: 1.1'
ename = 'Welcome'

@commands.Cog.listener()
async def on_member_join(self, member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send('Welcome {0.mention}.'.format(member))
