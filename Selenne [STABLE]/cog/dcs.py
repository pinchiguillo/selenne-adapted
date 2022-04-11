import discord
from discord.ext import commands
import asyncio

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
    async def echo(self, ctx, *, args):
        await ctx.send(args)

    @commands.command()
    async def bye(self, ctx):
        if ctx.author.id == 000000000000000000:
            await ctx.reply('bye!')
            await self.bot.close()

    @commands.command() # OUTDATED
    async def invite(self, ctx):
        await ctx.send('Not Reloaded')

    @commands.command()
    async def clear(self, ctx, ammount = 1000):
	    await ctx.channel.purge(limit = ammount)

class on_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

class management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
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
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        #await member.send(f" you have unmutedd from: - {ctx.guild.name}")
        embed = discord.Embed(title="Unmuted Member", description=f" {member.mention} is unmuted",colour=0x00ccff)
        await ctx.send(embed=embed)

    @commands.command() #OUTDATED
    ##@commands.has_role(root_role)
    async def private(self, ctx, auth : discord.Member, *, body):
        bot = self.bot
        #l_ch = bot.get_channel(log_ch)
        await auth.send(body)
        embed=discord.Embed(title = 'Mensaje Privado Enviado', description = f'{ctx.author.mention} envio un mensaje privado', color=0xff0088)
        embed.add_field(name = 'User', value = str(auth), inline=False)
        embed.add_field(name = 'Message', value = str(body), inline=False)

class stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sao(self, ctx):
        embed=discord.Embed(title = 'Sword Art Online', description = 'Datos temporales de Sword Art Online (Aincrad)', color=0x00d5ff)
        embed.add_field(name = 'Fecha de Inicio', value = '06/11/2022 13:00', inline=True)
        embed.add_field(name = 'Tiemo Restante', value = '[error:data.cant.load]', inline=True)
        embed.add_field(name = '■', value = '■', inline=False)
        embed.add_field(name = 'Fecha de Finalización', value = '07/1/2024 14:55', inline=True)
        embed.add_field(name = 'Tiempo Restante', value = '[error:data.cant.load]', inline=True)
        await ctx.send(embed=embed)

#PerServer
class security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def login(self, ctx):
        bot = self.bot
        prefix = 's.'
        #
        #channel = bot.get_channel(welcome_ch)
        msg_owner = ctx.message.author
        role = discord.utils.get(msg_owner.guild.roles, name = 'Campesino')
        await ctx.author.add_roles(role)
        await ctx.send('Bienvenido al server!')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=100)
        embed=discord.Embed(title = 'Seguriad de DCS', description = 'Actualmente en Discord hay muchos bots que grifean servidores, por eso DCS trae proteccion a tu servidor!', color = 0xee00ff)
        embed.add_field(name = 'Log-In', value = f'Utiliza {prefix}login para entrar al servidor', inline=False)
        await ctx.send(embed=embed)
    