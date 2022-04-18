import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b

    bot.add_command(at)

    bot.add_command(mute)
    bot.add_command(unmute)
    bot.add_command(private)

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

    embed = discord.Embed(title = 'Mutted Member', description=f"{member.mention} was muted by {ctx.author.mention}", colour=0x00ccff)
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
    embed = discord.Embed(title="Unmuted Member", description=f" {member.mention} is unmuted",colour=0x00ccff)
    await ctx.send(embed=embed)

@commands.command() #OUTDATED
##@commands.has_role(root_role)
async def private(ctx, auth : discord.Member, *, body):
    #l_ch = bot.get_channel(log_ch)
    await auth.send(body)
    embed=discord.Embed(title = 'Mensaje Privado Enviado', description = f'{ctx.author.mention} envio un mensaje privado', color=0xff0088)
    embed.add_field(name = 'User', value = str(auth), inline=False)
    embed.add_field(name = 'Message', value = str(body), inline=False)
