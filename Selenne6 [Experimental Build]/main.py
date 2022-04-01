#Experimental Bot: Selenne

#Import discord
from ast import Delete
import discord
from discord import activity
from discord import channel
from discord.components import Button 
from discord.ext import commands
from discord.embeds import Embed

from discord.ui import View, Button
import asyncio

#Import utils
import os

from discord.ui.button import button

#Private Libraries

intents = discord.Intents.default()  # All but the THREE privileged ones
intents.message_content = True  # Subscribe to the Message Content intent
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix='s.', intents=intents)  # Pass the intents into your commands.Bot or discord.Client

@bot.event
async def on_ready():
    print(f'BOT ONLINE')

    _guild = 913949547514974249
    _channel = 913949547514974252
    _message = 956875392965287986

    g = await bot.fetch_guild(_guild)
    ch = await g.fetch_channel(_channel)
    msg = await ch.fetch_message(_message)

    button1 = Button(label='First Button!!!', style=discord.ButtonStyle.blurple)

    async def button_callback(interaction):
        await interaction.response.edit_message(content='Hello', view = None)

    button1.callback = button_callback
    view = View()
    view.add_item(button1)

    await msg.edit(msg.content, view = view)

@bot.command()
@commands.has_permissions(administrator=True)
async def btn(ctx):
    if ctx.guild.id == 913949547514974249:
        button1 = Button(label='First Button!!!', style=discord.ButtonStyle.blurple)

        async def button_callback(interaction):
            await interaction.response.edit_message(content='Hello', view = None)

        button1.callback = button_callback
        view = View()
        view.add_item(button1)

        await ctx.send('hi!', view=view)
        await asyncio.sleep

@bot.command()
async def build(ctx, *,data = None):
    if ctx.guild.id == 913949547514974249:
        
        if not data:
            #Paglist
            def pagination(pag):

                if pag == 1:
                    return'Albedo\nAloy\nAmber\nArataki Itto\nBarbara\nBeidou\nBennett\nChongyum\nDiluc\nDiona'
                elif pag == 2:
                    return 'Eula\nGanyu\nGorou\nHu Tao\nJean\nKaedehara Kazuha\nKaeya\nKamisato Ayaka\nKequing'
                elif pag == 3:
                    return 'Klee\nKujou Sara\nLisa\nMona\nNingguang\nNoelle\nQiqi\nRiden Shogun\nRazor\nRosaria'
                elif pag == 4:
                    return 'Sangibiniya Kokomi\nSayu\nShenhe\nSucrose\nTartaglia\nThoma\nTraveler\nVenti\nXiangling\nXiao'
                elif pag == 5:
                    return 'Xingqiu\nXinyan\nYae Miko\nYanfei\nYoimiya\nYun Jun\nZhongli'
                else:
                    return 'Not in Index'

            button1 = Button(label='◄', style=discord.ButtonStyle.blurple)
            button2 = Button(label='X', style=discord.ButtonStyle.danger)
            button3 = Button(label='►', style=discord.ButtonStyle.blurple)

            bot.pag = 1


            #Button Functions
            async def button_callback_back(interaction):
                bot.pag -= 1
                embed=discord.Embed(title="Genshin Impact Builds Bot", description=pagination(bot.pag), color=0x7ecdd7)
                embed.set_footer(text=f'Pagina: {bot.pag}/X')
                await interaction.response.edit_message(embed=embed, view=view)
                

            button1.callback = button_callback_back
            async def button_callback_exit(interaction):
                embed=discord.Embed(title="Genshin Impact Builds Bot", description="ERROR WHILE CLOSING builds.th", color=0x7ecdd7)
                await interaction.response.edit_message(embed=embed, view=None)
                '''await interaction.delete()
                #await interaction.delete_original_message()'''
            button2.callback = button_callback_exit
            async def button_callback_next(interaction):
                bot.pag += 1
                embed=discord.Embed(title="Genshin Impact Builds Bot", description=pagination(bot.pag), color=0x7ecdd7)
                embed.set_footer(text=f'Pagina: {bot.pag}/X')
                await interaction.response.edit_message(embed=embed, view=view)
                
                if bot.pag == 6:
                    #button3.disabled=True
                    pass
            button3.callback = button_callback_next
            
            #Generate
            des = ''
            '''for i in range(len(pag1)):
                des = des + pag1[i] + '\n'''

            embed=discord.Embed(title="Genshin Impact Builds Bot", description=des, color=0x7ecdd7)
            embed.set_footer(text="Main Menu")

            #Pagination
            embed.set_footer(text=f'Pagina: {bot.pag}/X')
            if bot.pag == 1:
                #button1.disabled=True
                pass

            #Create
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)

        #OTP
        await ctx.send(embed=embed, view=view)

@bot.command()
async def update_msg(ctx):
    if ctx.guild.id == 913949547514974249:

        _channel = 913949547514974252
        _message = 956633745232896040

        ch = await bot.fetch_channel(_channel)
        msg = await ch.fetch_message(_message)
        await msg.edit('Hi!', embed=None)

@bot.command()
@commands.has_permissions(administrator=True)
async def anounce(ctx, *, args):
    _guild = 541658092639879189
    _channel = 860336491255300106
    if ctx.guild.id == _guild:
        ch = await bot.fetch_channel(_channel)
        embed=discord.Embed(title="📢 Anuncio", description=str(args), color=0x660000)
        embed.set_author(name="Zuteki")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/541658092639879189/a7d9a4e0a5c781fce57763c80f455ed3.jpg?size=128")
        #embed.add_field(name="a", value="a", inline=False)
        await ch.send('@everyone', embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def normas(ctx):
    if ctx.guild.id == 541658092639879189:
        normas = '''⚔️ Evita entrar en conflictos con usuarios que puedan dar problemas. Cualquier mensaje o contenido de su desagrado por DM/Privado, favor de Bloquear. Zuteki no se hará responsable de los acontecimientos externos al servidor. Por último, le recomendamos dirigirse a soporte de discord.

⚔️ Debes acatar y obedecer como indica en Reglas de Comunidad Discord y Términos y Condiciones de Discord. No cumplirlas es una sanción severa.

⚔️ Esta rotundamente prohibido enviar contenido NSFW (+18) en cualquier canal donde interactúe. 

⚔️ Prohibido usurpación o suplantación de usuario. Esto quiere decir nick/apodo o avatar con el fin de difamar, extorsionar o dañar a un usuario.

⚔️ Evitar el uso constante de palabras soeces y además de usar mayúsculas en su totalidad. Esto quiere decir moderar su vocabulario y evitar el uso de mayúsculas.

⚔️ Difundir una invitación de otro servidor que no sea de Zuteki es motivo de sanción a criterio de administración o moderación. Evite a toda costa.

⚔️ Prohibido evadir una sanción con multicuentas, esto podría complicar su permanencia en el servidor.

⚔️ Sanción máxima cualquier intento de "Raid". Si notamos algún indicio de raideo se aplica pena máxima "Ban permanente".

⚔️ Evite hacer spam o flood en cualquier canal. Esto incluye: imágenes/gif, textos repetidos o emojis, automáticamente la directiva de uno de nuestros bots lo borrara.

⚔️ Evite mencionar contenido de spoiler de cualquier anime, manga, novela y/o comic web en cualquier canal en el que se interactúe, para eso está el canal <#860351889471832084>, o simplemente "Marcar como spoiler" en el recuadro para imagen/gif o video. Incumplirlo es motivo de sanción (Warn o mute). 

⚔️ Prohibido mandar links, videos y imágenes que logre crashear el discord.

⚔️ Prohibido el autofarm (aunque sea usando bots).

⚔️ Tened cuidado con temas que puedan generar discordia. Está claro que cada uno tenemos nuestro punto de vista sobre "x" cosa y podemos hablar de ello, pero sin generar malos rollos. Que sean discusiones sanas en las que habléis de forma razonable, sin malas palabras. Recordad, respeto y buenas palabras, ante todo.

⚔️ Prohibido tener una conducta denigratoria ya sea por raza, cultura, nacionalidad, etnia u orientación sexual. Esto incluye acoso sexual y a menores. NO discriminación, NI acoso.

⚔️ Prohibido toxicidad de cualquier tipo hacia cualquier integrante dentro de la comunidad. Es motivo de sanción.

⚔️ Prohibido incitar el odio hacia el staff mostrando "pruebas" o cualquier elemento que apunte tal motivo, se debe evitar a toda costa la comunidad toxica dentro del servidor.

⚔️ No pedir rangos, está prohibido pedir ser Administrador; Moderador, u otros. 

⚔️ No utilizar @everyone Esto se usa para cosas importantes. Sólo pueden usarlo los Administradores; Moderadores, u owner, para avisaros de cambios y demás. '''

        embed=discord.Embed(title="❖ Reglas de Zuteki", description=normas, color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/541658092639879189/a7d9a4e0a5c781fce57763c80f455ed3.jpg?size=128")
        embed.set_footer(text="Administración | Zuteki")
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def sanciones(ctx):
    if ctx.guild.id == 541658092639879189:
        normas = '''⚔️ 3 warns equivalente a un mute.

⚔️ 3 mutes equivalente a un kick.

⚔️ La acumulación de los 2 puntos anteriores, puede aplicar a un Ban.

⚔️ A criterio de los miembros de staff pueden aplicar Ban o Tempban directamente si lo amerita.


⚔️ Según las acciones que cometas puede variar las sanciones correspondientes dependiendo de la gravedad del asunto. Evita problemas y lee el reglamento.


~ Advertir previamente a una sanción está bajo criterio del Staff ~
'''

        embed=discord.Embed(title="❖ Sanciones de Zuteki", description=normas, color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/541658092639879189/a7d9a4e0a5c781fce57763c80f455ed3.jpg?size=128")
        embed.set_footer(text="Administración | Zuteki")
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def echo(ctx, *, args):
    await ctx.send(args)

@bot.command()
@commands.has_permissions(administrator=True)
async def nacionalidades(ctx):
    colours = [0xe0004f,0x2bff00,0x66ff00,0xed0202,0xffbb00,0xffdd00,0xff004c,0xff8800,0x007bff,0x00ffcc,0x0084ff,0xcc3352,0x01bcaf,0x0062ff,0x00ccff,0xff0000,0x0a2ac7,0xc75f0a,0xe628d6,0xe0bb00]
    i = 0
    #Venecuela
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326410400301136/paletas_paises_ve.png')
    await ctx.send(embed=embed)
    #Bolivia
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326410622570536/paletas_paises_bo.png')
    await ctx.send(embed=embed)
    #Brasil
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326411025244280/paletas_paises_br.png')
    await ctx.send(embed=embed)
    #Chile
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326411247550554/paletas_paises_cl.png')
    await ctx.send(embed=embed)
    #Colombia
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326411419496498/paletas_paises_co.png')
    await ctx.send(embed=embed)
    #Ecuador
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326411734057000/paletas_paises_ec.png')
    await ctx.send(embed=embed)
    #Peru
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326411931213925/paletas_paises_pe.png')
    await ctx.send(embed=embed)
    #Paraguay
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326412430344313/paletas_paises_py.png')
    await ctx.send(embed=embed)
    #Uruguay
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326412723933304/paletas_paises_uy.png')
    await ctx.send(embed=embed)
    #Guatemala
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326469875503174/paletas_paises_gu.png')
    await ctx.send(embed=embed)
    #Honduras
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326470139768842/paletas_paises_ho.png')
    await ctx.send(embed=embed)
    #Mexico
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326470378831902/paletas_paises_mx.png')
    await ctx.send(embed=embed)
    #Nicaragua
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326470601138176/paletas_paises_ni.png')
    await ctx.send(embed=embed)
    #Panama
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326471003770880/paletas_paises_pa.png')
    await ctx.send(embed=embed)

    #Puerto Rico
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326471263842374/paletas_paises_pr.png')
    await ctx.send(embed=embed)
    #Republica Dominicana
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326471536459776/paletas_paises_rd.png')
    await ctx.send(embed=embed)
    #El Salvador
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326471754571876/paletas_paises_sr.png')
    await ctx.send(embed=embed)
    #Costa Rica
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326471981051934/paletas_paises_cr.png')
    await ctx.send(embed=embed)
    #Cuba
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326472249503794/paletas_paises_cu.png')
    await ctx.send(embed=embed)
    #España
    embed=discord.Embed(color=colours[i])
    i += 1
    embed.set_image(url = 'https://media.discordapp.net/attachments/957326343241076816/957326520299421786/paletas_paises_es.png')
    await ctx.send(embed=embed)

from config import TOCKEN
bot.run(TOCKEN)
