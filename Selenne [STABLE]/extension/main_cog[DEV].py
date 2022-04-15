import discord
from discord.ext import commands

class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
z/help - displays all the available commands
z/clear amount - will delete the past messages with the amount specified

Music commands:
z/mp <keywords> - finds the song on youtube and plays it in your current channel
z/mq - displays the current music queue
z/ms - skips the current song being played
```
"""
        self.text_channel_list = []

    #some debug info so that we know the bot has started    
    @commands.Cog.listener()
    async def on_ready(self):
        print('BOT Online')
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

    @commands.command(name="clear", help="Clears a specified amount of messages")
    async def clear(self, ctx, arg):
        #extract the amount to clear
        amount = 5
        try:
            amount = int(arg)
        except Exception: pass

        await ctx.channel.purge(limit=amount)

    
