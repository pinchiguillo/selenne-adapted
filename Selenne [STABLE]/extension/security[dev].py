import discord
from discord.ext import commands

import asyncio

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(login)

version = 'Security: Alfa'
ename = 'Security'

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
