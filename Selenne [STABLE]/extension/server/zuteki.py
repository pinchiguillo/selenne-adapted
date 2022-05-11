import discord
from discord.ext import commands

import asyncio

from discord.permissions import permission_alias

async def setup(b):
    global bot
    bot = b

    bot.add_command(anounce)
    bot.add_command(report)
    bot.add_command(suggest)
    bot.add_command(display)

    bot.add_listener(on_message)
    bot.add_listener(on_voice_state_update)

server_id = 959659781960917002

newsch = 959659782338400268
reportch = 963215746530418728
suggestch = 959659782569070623
logch = 965699651351220274
servercolor = 0x660000

@commands.command()
@commands.has_permissions(administrator=True)
async def anounce(ctx, *, args):
    if ctx.guild.id == server_id:
        ch = await bot.fetch_channel(newsch)
        embed=discord.Embed(title="📢 Anuncio", description=str(args), color=servercolor)
        embed.set_author(name="Zuteki")
        embed.set_thumbnail(url=ctx.guild.icon)
        #embed.add_field(name="a", value="a", inline=False)
        await ch.send('@everyone', embed=embed)

@commands.command()
async def report(ctx, *, body):
    if ctx.guild.id == server_id:
        ch = await bot.fetch_channel(reportch)
        embed=discord.Embed(title = 'Nuevo Reporte', color = 0xfa0000)
        embed.add_field(name = 'Usuario:', value = f'{ctx.author.mention}({ctx.author.id})', inline=False)
        embed.add_field(name = 'Contenido:', value = f'{body}', inline=False)
        await ch.send(embed=embed)
        await ctx.message.delete()
        await ctx.author.send('Tu reporte ha sido enviado con exito')
    
@commands.command()
async def suggest(ctx, *, body):
    if ctx.guild.id == server_id:
        ch = await bot.fetch_channel(suggestch)
        embed=discord.Embed(title = 'Nueva Sugerencia', description = body, color = 0x1b84b1)
        embed.add_field(name = 'Usuario:', value = f'{ctx.author.mention}', inline=False)
        sug = await ch.send(embed=embed)
        await sug.add_reaction('✅')
        await sug.add_reaction('❎')
        await ctx.message.delete()
        resp = await ctx.send('Gracias por la sugerencia')
        await asyncio.sleep(5)
        await resp.delete()

@commands.command()
@commands.has_permissions(administrator=True)
async def display(ctx, menu:str = 'Help'):
    if ctx.guild.id == server_id:
        h = '''```s.display normas``` muestra las normas del servidor\n```s.display sanciones``` muestra las sanciones del servidor\n```s.display nacionalidades``` Unique Display\n```s.display juegos```Unique Display\n```s.display verificacion```Unique Display\n```s.display report```Report Display'''
        if menu.lower() == 'help':
            embed=discord.Embed(title="Zuteki Display Command", description=h, color=0x660000)
            await ctx.reply(embed=embed)
        elif menu.lower() == 'normas':
            normas = '''❖ Evita entrar en conflictos con usuarios que puedan dar problemas. Cualquier mensaje o contenido de su desagrado por DM/Privado, favor de Bloquear. Zuteki no se hará responsable de los acontecimientos externos al servidor. Por último, le recomendamos dirigirse a soporte de discord.

❖ Debes acatar y obedecer como indica en Reglas de Comunidad Discord y Términos y Condiciones de Discord. No cumplirlas es una sanción severa.

❖ Esta rotundamente prohibido enviar contenido NSFW (+18) en cualquier canal donde interactúe. 

❖ Prohibido usurpación o suplantación de usuario. Esto quiere decir nick/apodo o avatar con el fin de difamar, extorsionar o dañar a un usuario.

❖ Evitar el uso constante de palabras soeces y además de usar mayúsculas en su totalidad. Esto quiere decir moderar su vocabulario y evitar el uso de mayúsculas.

❖ Difundir una invitación de otro servidor que no sea de Zuteki es motivo de sanción a criterio de administración o moderación. Evite a toda costa.

❖ Prohibido evadir una sanción con multicuentas, esto podría complicar su permanencia en el servidor.

❖ Sanción máxima cualquier intento de "Raid". Si notamos algún indicio de raideo se aplica pena máxima "Ban permanente".

❖ Evite hacer spam o flood en cualquier canal. Esto incluye: imágenes/gif, textos repetidos o emojis, automáticamente la directiva de uno de nuestros bots lo borrara.

❖ Evite mencionar contenido de spoiler de cualquier anime, manga, novela y/o comic web en cualquier canal en el que se interactúe, para eso está el canal <#860351889471832084>, o simplemente "Marcar como spoiler" en el recuadro para imagen/gif o video. Incumplirlo es motivo de sanción (Warn o mute). 

❖ Prohibido mandar links, videos y imágenes que logre crashear el discord.

❖ Prohibido el autofarm (aunque sea usando bots).

❖ Tened cuidado con temas que puedan generar discordia. Está claro que cada uno tenemos nuestro punto de vista sobre "x" cosa y podemos hablar de ello, pero sin generar malos rollos. Que sean discusiones sanas en las que habléis de forma razonable, sin malas palabras. Recordad, respeto y buenas palabras, ante todo.

❖ Prohibido tener una conducta denigratoria ya sea por raza, cultura, nacionalidad, etnia u orientación sexual. Esto incluye acoso sexual y a menores. NO discriminación, NI acoso.

❖ Prohibido toxicidad de cualquier tipo hacia cualquier integrante dentro de la comunidad. Es motivo de sanción.

❖ Prohibido incitar el odio hacia el staff mostrando "pruebas" o cualquier elemento que apunte tal motivo, se debe evitar a toda costa la comunidad toxica dentro del servidor.

❖ No pedir rangos, está prohibido pedir ser Administrador; Moderador, u otros. 

❖ Prohibido el uso de multicuentas dentro del servidor. 

❖ No utilizar @everyone Esto se usa para cosas importantes. Sólo pueden usarlo los Administradores; Moderadores, u owner, para avisaros de cambios y demás. '''

            embed=discord.Embed(title="❖ Reglas de Zuteki", description=normas, color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_footer(text="Administración | Zuteki")
            await ctx.send(embed=embed)
        elif menu.lower() == 'sanciones':
            normas = '''❖ 3 warns equivalente a un mute.

❖ 3 mutes equivalente a un kick.

❖ La acumulación de los 2 puntos anteriores, puede aplicar a un Ban.

❖ A criterio de los miembros de staff pueden aplicar Ban o Tempban directamente si lo amerita.


❖ Según las acciones que cometas puede variar las sanciones correspondientes dependiendo de la gravedad del asunto. Evita problemas y lee el reglamento.


~ Advertir previamente a una sanción está bajo criterio del Staff ~
'''

            embed=discord.Embed(title="❖ Sanciones de Zuteki", description=normas, color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_footer(text="Administración | Zuteki")
            await ctx.send(embed=embed)
        elif menu.lower() == 'nacionalidades':
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
        elif menu.lower() == 'juegos':
            colours = [0xffc800, 0xff00ea, 0x00e1ff,0xd40808]
            i = 0
            #Minecraft
            embed=discord.Embed(color=colours[i])
            i += 1
            embed.set_image(url = 'https://media.discordapp.net/attachments/959659783026270228/960262569174655036/banner_minecraft.jpg')
            await ctx.send(embed=embed)
            #Lol
            embed=discord.Embed(color=colours[i])
            i += 1
            embed.set_image(url = 'https://media.discordapp.net/attachments/959659783026270228/960262569531179048/banner_lol.jpg?width=1202&height=676')
            await ctx.send(embed=embed)
            #Genshin
            embed=discord.Embed(color=colours[i])
            i += 1
            embed.set_image(url = 'https://media.discordapp.net/attachments/959659783026270228/960262569866719332/banner_genshin.jpg')
            await ctx.send(embed=embed)
            #COD
            embed=discord.Embed(color=colours[i])
            i += 1
            embed.set_image(url = 'https://media.discordapp.net/attachments/959659783026270228/960262570273542184/banner_cod.png')
            await ctx.send(embed=embed)
        elif menu.lower() == 'categorias':
            veri = '''Para mantener la seguridad en el servidor hemos habilitado un sistema de verificacion.\nReacciona para poder acceder al resto del servidor
'''

            embed=discord.Embed(title="❖ Categorias de Zuteki", description = veri, color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_footer(text="Administración | Zuteki")
            await ctx.send(embed=embed)
        elif menu.lower() == 'reportes':
            veri = '''Utiliza este canal para reportar al Staff cualquier problema ocurrido en el servidor.\nUtiliza: ```s.report [reporte]``` para enviar un reporte.\n\nCon este metodo solo se puede mandar texto, si para procesar el reporte es necesario material auxiliar como imagenes u otras pruebas un miembro del staff se pondra en contacto por privado.\n\nSolo se aceptaran reportes de incidentes ocurridos dentro de Zuteki, para problemas externos ir directamente al soporte de Discord
'''

            embed=discord.Embed(title="❖ Reportes en Zuteki", description = veri, color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_footer(text="Administración | Zuteki")
            await ctx.send(embed=embed)
        elif menu.lower() == 'presentaciones':
            txt = '''Información del canal
Canal exclusivo para presentación, no es para chatear, tampoco es obligatorio presentarse ya que es de manera voluntaria, sin embargo se le borrará su presentación si no se acoge a la plantilla dada o parecido y pueden incluso añadir alguna cosa adicional o detalle a su gusto.

Plantilla de presentación
❖ Apodo:
❖ Edad:
❖ Género:
❖ Personalidad:
❖ Hobby:
❖ Música:
❖ Juegos:
❖ País:'''
            embed=discord.Embed(title="❖ Plantilla Presentaciones", description=txt, color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_footer(text="Administración | Zuteki")
            await ctx.send(embed=embed)
        elif menu.lower() == 'nitro':
            txt = '''Al boostear el servidor se te entregaran una serie de recompensas que te permitirán acceder a canales privados de boostes, se te entregara el rango Gran maestro y se recibirá una cantidad de experiencia dentro del servidor

**Recompensas:**

» Se les entregará 20000 puntos de experiencia, el primer boosteo(primer mes) recibirá 20000 puntos y en el segundo boosteo(segundo mes) recibirá la misma cantidad, pero ya del tercer boosteo
en adelante no recibirá más experiencia hasta el otro año. Total 40000 puntos de experiencia al año.

**Proximamente se añadiran nuevas recompensas**
'''
            embed=discord.Embed(title="❖ Informacion Boost del servidor", description=txt, color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_footer(text="Administración | Zuteki")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Zuteki Display Command", description=h, color=0x660000)
            await ctx.reply(embed=embed)

@commands.Cog.listener()
async def on_message(message):
    if not message.guild:
        return
    if message.guild.id == server_id and not message.author.bot:
        role = 962725878255714365

        log = await message.guild.fetch_channel(logch)
        verified = False
        for r in message.author.roles:
            if role == r.id:
                verified = True
        
        if not verified:
            try:
                await message.author.kick(reason='Escribir sin estar verificado')
                await log.send(f'{message.author.mention}({message.author.id}) ha sido expulsado Reason: **escribir sin estar verificado**')
                
            except discord.errors.Forbidden:
                await log.send(f'{message.author.mention}({message.author.id}) **Error al expulsar** Reason: **escribir sin estar verificado**')

@commands.Cog.listener()
async def on_voice_state_update(member, after, before):
    if member.guild.id == server_id and not member.bot:
        role = 962725878255714365

        log = await member.guild.fetch_channel(logch)
        verified = False
        for r in member.roles:
            if role == r.id:
                verified = True
        
        if not verified:
            try:
                await member.kick(reason='Conectarse a voz sin estar verificado')
                await member.send('Si quires escribir en Zuteki tienes que verificarte')
                await log.send(f'{member.mention}({member.id}) ha sido expulsado Reason: **Conectarse a voz sin estar verificado**')
                
            except discord.errors.Forbidden:
                await log.send(f'{member.mention}({member.id}) **Error al expulsar** Reason: **Conectarse a voz sin estar verificado**')

@commands.command()
@commands.has_permissions(manage_channels=True)
async def lock(self,ctx):
    perms = ctx.channel.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)