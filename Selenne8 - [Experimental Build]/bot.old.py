#inports
from calendar import c
import discord
from discord import activity
from discord import channel 
from discord.ext import commands
from discord.embeds import Embed
from requests import get
import time as t
from datetime import datetime
import random as rand
import asyncio

#Private Improts
#from dcs.functions import f_lib

#bot setting
print(f'Starting ...')

#create bot
#bot = commands.Bot(command_prefix = 's.', description = 'BOT', activity=discord.Game(name = str('Lerning...')), status=discord.Status.do_not_disturb)
bot = commands.Bot(command_prefix = 's.', description = 'BOT', activity=discord.Game(name = str('Retiro Espiritual')), status=discord.Status.do_not_disturb)
bot.remove_command('help')

#Global Var
bot.bot_name = ['selenne', 'selene', 'sele']
bot.bot_auth = ['pinchiguillo#4994']
bot.bypass = False
bot.ignore = open('db/sys/ignore.dat', 'r').readlines()
bot.blacklist = []

#Act toggle
bot.act = False

#bot.bypass_count = 0

#Default data:
zenkublocks = 839310820755243018
dev_srv = 913949547514974249

#Main Code
#BOT-MAIN
@bot.event
async def on_member_join(member):
    bot.blacklist.append(member.id)
    await asyncio.sleep(10)
    try:
        index = bot.blacklist.index(member.id)
        bot.blacklist.pop(index)
    except:
        pass

@bot.event
async def on_message(message):

    #Obtener datos
    msg = str(message.content)
    author = message.author
    ch = message.channel

    #Adecuacion de msg
    msg = f_lib.adecuate(msg, accent=False, special_char=False, lower_upper='lower')

    #Detectar si es llamado el bot y eliminar su mencion de la str
    mentioned = f_lib.appear(bot.bot_name, msg)

    #Specific Srv Code
    try:
        if str(message.author.id) != '935557521568038942':
            if message.guild.id == zenkublocks:
                #if True:
                if not ch.permissions_for(message.author).administrator or not ch.permissions_for(message.author).manage_messages:
                    #Bloquear spam
                    if 'http' in msg:
                        if 'https://example.com' in msg:
                            pass
                        elif 'discordapp' in msg:
                            pass
                        elif 'tenor' in msg:
                            pass
                        else:
                            m1 = await message.reply('No permitimos envio de links de spam, si crees que tu link no es spam contacta con moderacion')
                            await message.delete()
                            await asyncio.sleep(5)
                            await m1.delete()
                        if message.author.id in bot.blacklist:
                            await message.author.ban()
                    #AutoRespuestas
                    if 'ip' in msg or 'uno' in msg:
                        if 'srv' in msg or 'server' in msg or 'servidor' in msg or '?' in msg:
                            await ch.send('Visita <#852968579350396960>, para saber como unirse al servidor')
                    elif 'ayuda' in msg:
                        await ch.send('Si es algun problema tecnico relacionado con el servidor usa <#839314844267315201>')
                    elif 'bug' in msg or 'error' in msg:
                        await message.reply('Visita <#839314844267315201> para que te podamos brinar apoyo tecnico desde el Staff')
                    elif 'descarg' in msg:
                        if 'mod' in msg:
                            await ch.send('El pack de mods lo puedes descargar desde <#842908439285202944>')
                        elif 'pack' in msg:
                            await ch.send('El pack de texturas del servidor se descarga autmotaicamente al unirse al servidor si tienes activada esta opcion en las configuraciones del juego\nFuera de eso no puedes descargarlo para usarlo fuera de nuestro servidor')
                    elif 'proteccion' in msg:
                        if 'permisos' in msg:
                            await message.reply('pon ```/ps add [user]```')
                        if 'añad' in msg and 'jugador' in msg:
                            await message.reply('pon ```/ps add [user]```')
                        if 'comprar' in msg or 'obten' in msg or 'cons' in msg:
                            await message.reply('pon ```/ps get [tipo]```Tienes de tres niveles cada uno mas grande que el anterior')
    except:
        pass

    #Main BOT
    
    if f_lib.appear(['siri', 'alexa', 'cortana'], msg):
        await message.reply('No me vuelvas a hablar, estas muerto para mi')
    elif f_lib.appear(['enneles', 'eneles', 'eles'], msg):
        await message.reply('ohcered led nelbah em euq atsug em im a orep otneis oL') #Lo siento pero a mi me gusta que me hablen del derecho
    elif mentioned and not message.author.bot or bot.bypass and not message.author.bot or not message.guild and not message.author.bot:
        if bot.act:
            print(message.author.id)
            print(bot.ignore)
            print(str(message.author.id).removesuffix('\n') in bot.ignore)

            
            if not str(message.author.id).removesuffix('\n') in bot.ignore:

                #Activar/Desactivar Bypass
                if msg in bot.bot_name:
                    await ch.send('Si?')
                    bot.bypass = True
                    #bot.bypass_count += 1
                    await asyncio.sleep(25)
                    #bot.bypass_count -= 1
                    if bot.bypass == True :
                        bot.bypass = False
                        #bot.bypass_count -= 1
                        await ch.send('Hola?')
                        await asyncio.sleep(1)
                        await ch.send('Me abandono :(')
                elif 'adios' in msg or 'ads' in msg:
                    await ch.send(f'Adios {author.mention}')
                    bot.bypass = False
                #musica - dev
                elif 'musica' in msg or 'pon' in msg:
                    await ch.send('Todavia no he aprendido ha poner musica, ten paciencia')
                #aprender - beta
                elif 'aprende' in msg:
                    await ch.send(f'Luego en un rato me pongo a aprenderlo')
                    f = open('db/lern.dat', 'a')
                    save = str(msg).removeprefix('aprende ')
                    f.write(f'{author} >> {save}\n')
                    f.close()
                #agenda - dev
                elif 'guarda' in msg or 'apunta' in msg or 'recuerda' in msg:
                    '''if 'guarda' in msg:
                        if 'corazon' in msg or 'kokoro' in msg:
                            await message.reply('Tu eres tonto?')
                        elif f_lib.appear(['cuchillo', 'navaja', 'bate', 'bazuka', 'arco', 'pistola', 'metralleta', 'escopeta'], msg):
                            await message.reply('Aqui cada uno se guarda sus armas')'''
                    if False:pass
                    else:
                        #save = str(message.content)
                        save = msg
                        try:
                            save = f_lib.pop_str(save, bot.bot_name)
                            #save = f_lib.pop_str(save, ['guarda' , 'apunta', 'recuerda'])
                            try:
                                FILE = open(f'db/diary/{str(author)}', 'a')
                                FILE.write(f'{save}\n')
                                FILE.close()
                                m1 = await message.reply('Ya lo he guardado')
                            except:
                                m1 = await message.reply('No he podido guardar eso')
                                print('ALERT: error.save in cmd.diary.save')
                        except:
                            m1 = await message.reply('No he podido guardar eso')
                            print('ALERT: error.adecuate in cmd.diary.save')

                        await asyncio.sleep(10)
                        await message.delete()
                        await m1.delete()
                elif 'agenda' in msg:
                    if 'limpia' in msg or 'borra' in msg or 'vacia' in msg:
                        f = open(f'db/diary/{str(author)}', 'w')
                        f.write('')
                        f.close()
                        await ch.send(f'Ya te he vaciado la agenda')
                    else:
                        try:
                            f = open(f'db/diary/{str(author)}', 'r')
                            content = f.read()
                            f.close()
                            if content == '':
                                content = 'Agenda vacia'
                        except:
                            content = 'Agenda vacia'
                        embed=discord.Embed(title='Diary', description=content, color=0x00ff9d)
                        embed.set_author(name=author)
                        diary = await ch.send(embed=embed)
                        await asyncio.sleep(25)
                        await diary.delete()
                        await message.delete()
                #El continental publi
                elif 'pon' in msg:
                    if 'publi' in msg:    
                        if 'zenkublocks' in msg:
                            embed=discord.Embed(title='ZenkuBlocks', description='Os invitamos a ZenkuBlocks, una comunidad que ha crecido en torno a un servidor de minecraft actualmente Survival, auque en un futuro proximo añadiremos minijuegos.\nPor ultimo nos gustaria tanto invitaros como recomendaros una pagina para ver animes.\nTodos los links están a continuación', color=0x00bfff)
                            embed.set_thumbnail(url='https://zenkublocks.com/img/logo.png')
                            embed.add_field(name='ZenkuBlocks Web', value='https://zenkublocks.com', inline=False)
                            embed.add_field(name='Zenkublocks Discord', value='https://example.com/discord-invite', inline=False)
                            await ch.send(embed=embed)
                            await ch.send('https://example.com/discord-invite')
                        else:
                            await ch.send('No se quienes son, no voy ha hacer publicidad de alguien que no conozco')
                    elif 'inv' in msg:
                        if 'zenkublocks' in msg:
                            await ch.send('https://example.com/discord-invite')
                    else:
                        ch.send('Que pongo?')
                #Poner su link
                elif 'unete a mi srv' in msg:
                    await message.reply('Invitame con este link, https://discord.com/api/oauth2/authorize?client_id=935557521568038942&permissions=8&scope=bot\nAh, ya que continuamente estoy añadiendo mas funciones necesito administrador para evitar problemas\nSry')
                #Genshin - Beta (Bugged)
                elif 'genshin' in msg or 'banner' in msg or 'gacha' in msg or 'build' in msg:
                    if 'build' in msg:
                        if 'warframe' not in msg:
                            try:
                                #Adecuacion de imput
                                try:
                                    msg = f_lib.pop_str(msg, bot.bot_name)
                                except:
                                    pass
                                character = msg.removeprefix('build ')
                                try:
                                    character_f = str(character).replace(' ', '')
                                except:
                                    pass
                                #Obtener datos de archivo y construir embed
                                try:
                                    f = open(f'db/builds/{character_f}.dat', 'r')
                                    data = f.read()
                                    f.close()
                                    #obtener variables
                                    data = data.split('|')
                                    element = data[1].removesuffix('\n')
                                    role = data[2].removesuffix('\n')
                                    img = data[3].removesuffix('\n')
                                    weapon = data[4].removesuffix('\n')
                                    artifacts = data[5].removesuffix('\n')
                                    talents = data[6].removesuffix('\n')
                                    team = data[7].removesuffix('\n')
                                    version = data[8].removesuffix('\n')

                                    #Generar Embed
                                    if element == 'Anemo':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0x00ff9d)
                                    elif element == 'Pyro':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0xff5900)
                                    elif element == 'Cryo':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0xffffff)
                                    elif element == 'Hydro':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0x0084ff)
                                    elif element == 'Geo':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0xc19210)
                                    elif element == 'Electro':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0x8f1eb8)
                                    elif element == 'Dendro':
                                        embed=discord.Embed(title = f'{character.upper()} - Build', description = f'Roles: {role}', color = 0x1a8604)

                                    embed.set_thumbnail(url = img)
                                    embed.add_field(name = 'Weapon', value = weapon, inline = False)
                                    embed.add_field(name = f'Artifacts', value = artifacts, inline = False)
                                    embed.add_field(name = f'Talents', value = talents, inline = False)
                                    embed.add_field(name = f'Teams', value = team, inline = False)
                                    embed.set_footer(text = f'Game version: {version}')
                                    await ch.send(embed = embed)

                                    
                                # Error al abrir archivo / No se encuentra el objetivo en la DB
                                except:
                                    if character == 'build':
                                        await ch.send('Se buildear cosas, pero no se leer mentes, dime que quieres que te ayude a buildear')
                                    else:
                                        await ch.send(f'No se como buildear {character}')
                        #Error de Syntaxis
                            except:
                                await ch.send('Aprende syntaxis porque no te entiendo')
                    elif 'ace' in msg and 'gacha' in msg:
                        await message.reply('Tu ere tonto?')
                    elif 'codigo' in msg:
                        f = open(f'db/genshin/codigos.dat', 'r')
                        await ch.send(f.read())
                        f.close()
                    elif 'fecha' in msg:
                        f = open(f'db/genshin/fecha.dat', 'r')
                        await ch.send(f.read())
                        f.close()
                    elif 'banner' in msg or 'gacha' in msg:
                        if 'tirar' in msg:
                            f = open(f'db/genshin/tirar.dat', 'r')
                            await ch.send(f'{f.read()}')
                            f.close()
                        else:
                            f = open(f'db/genshin/banner.dat', 'r')
                            await ch.send(f.read())
                            f.close()
                    elif 'lore' in msg:
                        await ch.send('Dentro de poco empezare a contar sobre el lore de genshin impact')
                    else:
                        await ch.send('No se a que te refieres')
                #Warframe - Pre 1
                elif 'warframe' in msg:
                    if 'build' in msg:
                        await ch.send('No se buildear en warframe, ni pienso aprender por ahira')
                    else:
                        await ch.send('Warfame, tremendo juego')
                #Abandonar Srv
                elif 'nos vamos' in msg:
                    if not message.guild:
                        await ch.send('Estamos en un chat privado, quieres que me vaya?')
                    elif str(author) == 'pinchiguillo#4994' :
                        await message.reply('Vale')
                        await asyncio.sleep(1)
                        await ch.send('Adios gente')
                        await message.guild.leave()
                    else:
                        await message.reply('No me voy a ir porque tu me lo digas')
                
                #Execute CMD - ALFA
                elif 'execute' in msg or 'ejecuta comando' in msg or 'ejecuta' in msg:
                    if str(author) in bot.bot_auth:
                        m1 = await ch.send('Usuario reconocido en la base de datos privada del sistema')
                        await asyncio.sleep(1)
                        m2 = await ch.send('Conectando con la red DCS...')
                        await asyncio.sleep(4)
                        m3 = await ch.send('Ejecutando comando en el servidor principal')
                        await asyncio.sleep(4)
                        m4 = await ch.send('Comando Ejecutado con exito')


                        await asyncio.sleep(10)
                        await message.delete()
                        await m1.delete()
                        await m2.delete()
                        await m3.delete()
                        await m4.delete()
                
                #Ignora
                elif 'ignora' in msg:
                    if str(author) in bot.bot_auth:
                        #Adecuacion de variables
                        _str = f_lib.pop_str(msg, bot.bot_name)
                        _str = f_lib.pop_str(msg, ['ignora', 'ignorar'])
                        _str = _str.split()

                        #buscar usuario
                        usr_index = f_lib.char_list('@', _str, pos=True)
                        usr = _str[usr_index]

                        usr = usr.removeprefix('<@')
                        usr = usr.removesuffix('>')

                        if 'deja' in msg:
                            ind = bot.ignore.index(str(usr))
                            bot.ignore.pop(ind)
                            await message.reply('Ya he dejado de ignorarlo')
                        else:
                            bot.ignore.append(str(usr))
                            await message.reply('Entendido, ahora lo voy a ignorar')
                        FILE = open('db/sys/ignore.dat', 'w')
                        for i in range(len(bot.ignore)):
                            FILE.write(f'{bot.ignore[i]}\n')
                        FILE.close
                    else:
                        await ch.send('No creo que seas alguien capaz de decirme a quien tengo que ignorar')

                #Zona de dialogos
                elif 'quieres' in msg:
                    if 'ser' in msg:
                        if 'mia' in msg:
                            await message.reply('Emm, no creo que tengamos esa relacion')
                        elif 'mi' in msg:
                            if 'amiga' in msg:
                                await message.reply('Puedo darte una oportunidad')
                            elif 'novia' in msg:
                                await message.reply('No creo que nos conozcamos lo suficiente')
                            elif 'esposa' in msg or 'mujer' in msg:
                                await message.reply('Las cosas en orden, priemero intenta que sea tu novia')
                            elif 'waifu' in msg:
                                await message.reply('No pienso ser una mas en tu lista de waifus')
                            else:
                                await message.reply('Tu que?')
                        else:
                            await message.reply('Yo quiero ser muchas cosas')
                    elif 'casarte' in msg:
                        await message.reply('No, buscate a otra')
                    else:
                        await message.reply('Dinero, quiero dinero')
                elif ' amas' in msg:
                    await message.reply('Todavia no entiendo bien, pero se lo que significa amas, asi que no')
                elif 'donde' in msg:
                    if 'ver' in msg or 'veo' in msg:
                        if 'anime' in msg:
                            await message.reply('En una plataforma oficial, sin duda')
                        else:
                            await message.reply('Ver el que?, estrellas?')
                    elif 'esta' in msg:
                        await message.reply('Suspendi geografia, no me preguntes de geografia')
                    elif 'jugar' in msg:
                        if 'minecraft' in msg:
                            await message.reply('En ZenkuBlocks')
                        else:
                            await message.reply('Jugar a que?')
                    else:
                        await message.reply('...')
                elif 'haz' in msg and not 'luz' in msg:
                    if 'debere' in msg:
                        await message.reply('Claro, pero primero me haces los mios')
                        await asyncio.sleep(1)
                        await ch.send('Son muy simples, crear un motor de simulacion que acepte todas las teorias fisicas actuales')
                        await asyncio.sleep(4)
                        await ch.send('Simple')

                    await ch.send('No voy ha hacerte nada extraño')
                elif 'ver' in msg or 'visto' in msg:
                    await ch.send('Ver lo que es ver, no veo nada')
                elif 'trae' in msg:
                    await ch.send('Hazlo tu, no es que me de pereza pero deberias alejarte del ordenador y moverte un poco')
                elif 'estas' in msg:
                    await ch.send('NO, no te voy a contar nada personal')
                elif 'parece' in msg:
                    await ch.send('No voy a exponer mis opiniones en publico porque ultimamente la gente es de cristal')
                
                #Exception
                else:
                    await message.reply('Todavia no se como responder a eso')
                pass
        else:
            await ch.send('Lo siento, ahora no estoy de humor para hablar')
###########################     END      ##############################
print('BOT ONLINE')
bot.run('REDACTED_DISCORD_TOKEN')

'''''
embed=discord.Embed(title=f'{character.upper()} - Build', description=f'Roles:{character_roles}', color=0x00ff55)
embed.set_thumbnail(url=character_url)
embed.add_field(name='Weapon', value=character_weapon, inline=False)
embed.add_field(name=f'Build {i}: {build_type}', value=character_build[i], inline=False)
embed.set_footer(text=Mejor build)
await ctx.send(embed=embed)
'''