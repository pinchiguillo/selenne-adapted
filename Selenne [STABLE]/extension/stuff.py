import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    bot.log.warning(f'{__name__} outdated')


    bot.add_command(countdown_date_to_be_reached_in_days_hours_minutes_and_seconds_Made_by_Pinchiguillo)

def teardown(bot):
    bot.log.info(f'{__name__} unloaded')

@commands.command()
async def sao(ctx):
    embed=discord.Embed(title = 'Sword Art Online', description = 'Datos temporales de Sword Art Online (Aincrad)', color=0x00d5ff)
    embed.add_field(name = 'Fecha de Inicio', value = '06/11/2022 13:00', inline=True)
    embed.add_field(name = 'Tiemo Restante', value = '[error:data.cant.load]', inline=True)
    embed.add_field(name = '■', value = '■', inline=False)
    embed.add_field(name = 'Fecha de Finalización', value = '07/1/2024 14:55', inline=True)
    embed.add_field(name = 'Tiempo Restante', value = '[error:data.cant.load]', inline=True)
    await ctx.send(embed=embed)

@commands.command()
async def countdown_date_to_be_reached_in_days_hours_minutes_and_seconds_Made_by_Pinchiguillo(ctx):
    await ctx.send('Prueba a usar s.c :)')