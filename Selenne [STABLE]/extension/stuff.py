import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b


    bot.add_command(sao)

@commands.command()
async def sao(ctx):
    embed=discord.Embed(title = 'Sword Art Online', description = 'Datos temporales de Sword Art Online (Aincrad)', color=0x00d5ff)
    embed.add_field(name = 'Fecha de Inicio', value = '06/11/2022 13:00', inline=True)
    embed.add_field(name = 'Tiemo Restante', value = '[error:data.cant.load]', inline=True)
    embed.add_field(name = '■', value = '■', inline=False)
    embed.add_field(name = 'Fecha de Finalización', value = '07/1/2024 14:55', inline=True)
    embed.add_field(name = 'Tiempo Restante', value = '[error:data.cant.load]', inline=True)
    await ctx.send(embed=embed)
