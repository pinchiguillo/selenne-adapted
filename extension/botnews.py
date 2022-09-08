import discord
from discord.ext import commands
from discord.ext import tasks
import json

async def setup(b):
    global bot
    bot = b
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(bn)
    bot.add_command(update)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

bot_version = 'Selenne 4.8.6'
version = 'BotNews: 1.1'
ename = 'Default'

db_path = 'db/afkmanager.json'

@commands.command()
async def bn(ctx, args = None):
    if ctx.author.id == bot.owner:
        with open(db_path, 'r') as f:
            db = json.load(f)


    with open('news.txt', 'r') as f:
        news = f.read()

    db_keys = list(db.keys())

    for gld in db_keys:
        g_id = int(gld)
        guild = await bot.fetch_guild(g_id)
        ch = await guild.fetch_channel(db[gld])

        embed=discord.Embed(title = 'Novedade Selenne', description = news, color = bot.color)
        embed.set_footer(text = 'DCS | Equipo de desarrollo de Selenne')
        await ch.send(embed=embed)

@commands.command()
async def update(ctx, args = None):
    await ctx.send('''La versión de Selenne que estas utilizando es la **4.8.6**, la última versión que estará disponible de la **Serie 4.x**.
 
Actualmente nuestro equipo de desarrolladores está trabajando en la **versión 5.0**, la cual soluciona una gran variedad de bugs y implementará nuevas funciones entre las que destacan:
- La implementación pública del **Módulo Config** el cual permite a otros módulos configurar opciones específicas para cada servidor.
- La implementación del sistema de anuncios en servidores no premium.
- Más minijuegos como **Tic Tac Toe**, o **Fishing** (Beta).
- Mejoras en el módulo musical.
- Se añadirá la opción de conversiones horarias.
- Implementación de más comandos para facilitar la moderación en el servidor.
- Sistema de expulsión de miembros fantasma
- Protección anti raideos
- Estadísticas del servidor
 
Todos los servidores que posean **Selenne** serán considerados como **Premium**
''')
