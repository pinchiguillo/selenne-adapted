import discord
from discord.ext import commands
import re

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(at)

    bot.add_command(mute)
    bot.add_command(unmute)
    bot.add_command(private)

    bot.add_command(mute_)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'AdminTools: Alfa'
ename = 'AdminTools'

@commands.command()
async def at(ctx, args = None):
    if 'help' in args:
        await ctx.send('Not Setup')
    else:
        await ctx.send(f'Current Version: **{version}**')

    
@commands.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    embed = discord.Embed(title = 'Mutted Member', description=f"{member.mention} was muted by {ctx.author.mention}", colour=bot.color)
    embed.add_field(name="reason:", value=reason, inline=False)

    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    #await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@commands.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    #await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(title="Unmuted Member", description=f" {member.mention} is unmuted",colour=bot.color)
    await ctx.send(embed=embed)

 
@commands.command() #OUTDATED
##@commands.has_role(root_role)
async def private(ctx, auth : discord.Member, *, body):
    #l_ch = bot.get_channel(log_ch)
    await auth.send(body)
    embed=discord.Embed(title = 'Mensaje Privado Enviado', description = f'{ctx.author.mention} envio un mensaje privado', color=0xff0088)
    embed.add_field(name = 'User', value = str(auth), inline=False)
    embed.add_field(name = 'Message', value = str(body), inline=False)


####################################################################################################################################################################################
@commands.command()
@commands.has_permissions(manage_messages=True)
async def _mute(ctx, member: discord.Member):
    pass

#This should be at your other imports at the top of your code
import asyncio

@commands.command()
@commands.has_permissions(manage_messages=True)
async def mute_(ctx, user : discord.Member, duration = 0,*, unit = None):

    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await ctx.send(f":white_check_mark: Muted {user} for {duration}{unit}")
    await user.add_roles(mutedRole)
    if unit == "s":
        wait = 1 * duration
        await asyncio.sleep(wait)
    elif unit == "m":
        wait = 60 * duration
        await asyncio.sleep(wait)
    await user.remove_roles(mutedRole)
    await ctx.send(f":white_check_mark: {user} was unmuted")


#
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


@commands.command()
@commands.has_permissions(manage_roles=True)
async def _mute_(self, ctx, member:discord.Member, *, time:TimeConverter = None):
    """Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
    &mute @Someone 1d"""
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(("Muted {} for {}s" if time else "Muted {}").format(member, time))
    if time:
        await asyncio.sleep(time)
        await member.remove_roles(role)