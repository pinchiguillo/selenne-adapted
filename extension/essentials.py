import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import datetime

__EXTENSION_NAME__ = 'Essentials'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    global color
    
    color = bot.color
    
    await bot.add_cog(Essentials_cog(bot))

    #await bot.tree.sync()

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

class AdminStatsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    
    @discord.ui.button(label = 'AdminStats', style=discord.ButtonStyle.danger)
    async def apuntes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.resolved_permissions.administrator:
            
            embed=discord.Embed(title = 'Advanced Server Stats', description = '''**Stats of the last 7 days**
**Messages**: `Not Avilable`
**New Members**: `Not Avilable`
**Different Comunicators**: `Not Avilable`
''', color=color)

            await interaction.response.send_message(embed=embed, view = None, ephemeral=True)
        else: await interaction.response.send_message('You cant see this :(', ephemeral=True)

#? Sample
class Essentials_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    @discord.app_commands.command(name = 'serverinfo')
    @discord.app_commands.describe()
    async def serverinfo(self, interaction: discord.Interaction):
        """Shows the server info"""

        guild = interaction.guild

        bots = 0
        for member in guild.members:
            if member.bot: bots += 1

        embed = discord.Embed(title = 'ServerInfo', color= self.bot.color)
        embed.add_field(name = 'Owner', value = guild.owner.mention)
        embed.add_field(name = 'Creation Date', value = guild.created_at.strftime("%d/%m/%Y"))
        embed.add_field(name = 'Members', value = len(guild.members))
        embed.add_field(name = 'Channels', value = len(guild.channels))
        embed.add_field(name = 'Bots', value = bots)
        embed.add_field(name = 'Emojis', value = len(guild.emojis))
        embed.add_field(name = 'Nitro Boosters', value = len(guild.premium_subscribers))
        
        embed.set_thumbnail(url = guild.icon.url)

        await interaction.response.send_message(embed=embed, view = AdminStatsView())

    @discord.app_commands.command(name = 'whois')
    @discord.app_commands.describe(
        user = 'The user you to get info'
    )
    async def whois(self, interaction: discord.Interaction, user:discord.Member):
        """Tells some interesting information about an user"""

        rolesl = list()
        for role in user.roles:
            if role.name != '@everyone':
                rolesl.append(role.mention)


        roles = ", ".join(reversed(rolesl))


        embed = discord.Embed(title= f'Who is {user}?', colour = self.bot.color)

        embed.set_thumbnail(url = user.avatar)
        embed.set_footer(text = f'Requested by - {interaction.user}', icon_url = interaction.user.avatar)

        embed.add_field(name = 'ID:', value = user.id, inline=False)
        embed.add_field(name = 'Name:', value = user.display_name, inline=False)
        diff = str(datetime.datetime.now() - user.created_at.replace(tzinfo=None)).split(',')[0]
        embed.add_field(name = 'Created at:', value = f'{user.created_at.strftime("%d/%m/%Y %H:%M")} ({diff} ago)', inline=False)    #!embed.add_field(name = 'Created at:', value = user.created_at, inline=False)
        diff = str(datetime.datetime.now() - user.joined_at.replace(tzinfo=None)).split(',')[0]
        embed.add_field(name = 'Joined at:', value = f'{user.joined_at.strftime("%d/%m/%Y %H:%M")} ({diff} ago)', inline = False)    #!embed.add_field(name = 'Joined at:', value = user.joined_at, inline = False)

        if len(rolesl) >= 1:
            embed.add_field(name = f'Roles: {len(rolesl)} ',value = ''.join([roles]), inline=False)
            embed.add_field(name = 'Top Role:', value = user.top_role.mention, inline=False)
        else:
            embed.add_field(name = f'Roles: 0',value = self.bot.nullchar, inline=False)
        


        await interaction.response.send_message(embed=embed)

    #!
    @discord.app_commands.command(name = 'ban')
    @discord.app_commands.describe(
        user = 'The user you want to ban',
        reason = 'The reason of the ban'
    )
    async def ban_user(self, interaction: discord.Interaction, user:discord.User, reason: Optional[str] = None):
        """Ban an user with Selenne logging"""
        await interaction.response.send_message('Feature not avilable')

    #!
    @discord.app_commands.command(name = 'kick')
    @discord.app_commands.describe(
        user = 'The user you want to kick',
        reason = 'The reason of the kick'
    )
    async def kick_user(self, interaction: discord.Interaction, user:discord.User, reason: Optional[str] = None):
        """Kick an user with Selenne logging"""
        await interaction.response.send_message('Feature not avilable')

    @discord.app_commands.command(name = 'echo')
    @discord.app_commands.default_permissions(manage_messages=True)
    @discord.app_commands.describe(
        message = 'The message you want Selenne to say',
        times = 'The number of times the message will repeat'
    )
    async def echo(self, interaction: discord.Interaction, message: str, times: discord.app_commands.Range[int, 1, 10] = 1):
        """Makes Selenne to repeat a message"""
        
        await interaction.response.send_message(f'Okey {interaction.user.mention}', ephemeral=True)

        for _ in range(times):
            await interaction.channel.send(message)

#! cooldowns, default_permissions