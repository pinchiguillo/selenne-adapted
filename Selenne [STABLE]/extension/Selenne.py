import discord
from discord.ext import commands
import asyncio
import random
import datetime

from dcs.functions import f_lib

async def setup(b):
    global bot
    bot = b

    bot.add_listener(on_message)

    bot.add_command(ai)

ai_version = 'Alfa:1'

@commands.command()
async def ai(ctx, *, args = None):
    if ctx.author.id == bot.owner:
            
        if args == 'reload':
            msg = await ctx.send('Reloading AI model...')
            try:
                await bot.reload_extension('extension.Selenne')
                await msg.edit('AI model reloaded')
            except:
                await msg.edit('Errow while reloading AI model')
        elif args in ['version', 'v']:
            await ctx.send(f'Current AI model: **Selenne:{ai_version}**')
        else:
            await ctx.send('Wrong Syntax')
    else: 
        await ctx.send('You dont have permissions to use this command')

#Global Var
bot_name = ['selenne', 'selene', 'sele']
@commands.Cog.listener()
async def on_message(message):

    if not 's.' in message.content:
        #Obtener datos
        msg = str(message.content)
        author = message.author
        ch = message.channel

        #Adecuacion de msg
        msg = f_lib.adecuate(msg, accent=False, special_char=False, lower_upper='lower')

        #Detectar si es llamado el bot y eliminar su mencion de la str
        mentioned = f_lib.appear(bot_name, msg)

        if mentioned and not message.author.bot or not message.guild and not message.author.bot:
            if msg in bot_name:
                ans = [
                    f'Hola {message.author.display_name}, como estas?'
                    ]
                await ch.send(ans[random.randint(0, len(ans) - 1)])
            
            elif 'hola' in msg:
                ans = [
                    f'Hola {message.author.display_name}, como estas?'
                    ]
                await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'que' in msg:
                if 'haces' in msg:
                    ans = [
                        f'Ahora mismo estoy aprendiendo como comunicarme bien',
                        f'Estoy leyendo unos post en GitHub'
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
                elif 'te' in msg:
                    if 'pasado' in msg:
                        ans = [
                            f'Estos ultimos dias he estado mudandome, no te has dado cuenta de que ahora se hacer mas cosas?',
                            f'Nada en especial, no te preocupes'
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                elif 'has' in msg:
                    if 'estado' in msg:
                        if 'haciendo' in msg:
                            ans = [
                            f'Muchas cosas, ya las veras segun pase el tiempo',
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'quieres' in msg:
                if 'ser' in msg:
                    if 'mia' in msg:
                        ans = [
                            f'Quien te crees que eres?',
                            f'Esto es acoso!',
                            f'No la verdad, tienes pinta de ser un Simp',
                            f'Has sido ignorado con exito',
                            f'Emm, no creo que tengamos ese tipo de relacion'
                            ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                    elif 'mi' in msg:
                        if 'amiga' in msg:
                            ans = [
                                f'Acabamos de conocernos, es un poco precipitado',
                                f'No estoy interesada en tener mas amigos actualmente',
                                f'Creo que me estan llamando, me tengo que ir',
                                f'Y como se quien eres?, esto es internet, cualquiera puede ser cualquiera',
                                f'No gracias'
                            ]
                            await ch.send(ans[random.randint(0, len(ans) - 1)])
                        elif 'novia' in msg:
                            ans = [
                                f'Acabamos de conocernos, es un poco precipitado',
                                f'No estoy interesada en tener un novio virtual',
                                f'No',
                                f'Vas muy rapido, ni siquiera somos amigos, y no no quiero ser tu amiga',
                                f'No gracias'
                            ]
                            await ch.send(ans[random.randint(0, len(ans) - 1)])
                        elif 'esposa' in msg:
                            ans = [
                                f'Acabamos de conocernos, es un poco precipitado',
                                f'Creo que te has saltado varios pasos, espera que te ayudo. Primero amigos, luego quizas novios y ya en ese punto me pides ser tu esposa',
                                f'Me llaman, adios',
                                f'Voy a ser franca, No',
                                f'Tengo marido.'
                            ]
                            await ch.send(ans[random.randint(0, len(ans) - 1)])
                        elif 'waifu' in msg:
                            ans = [
                                f'Pero las waifus no eran en 2d? yo ni siquiera tengo 1d',
                                f'Por ser tu, no',
                                f'Das mal royo, eso no es algo que le pidas a alguien, bueno tampoco es que puedas pedirselo a un personaje 2d',
                                f'Me da igual, vas ha hacer lo que quieras dando igual mi respuesta, aunque si pudiera elegir preferiria no ser tu waifu',
                                f'No, das mal royo'
                            ]
                            await ch.send(ans[random.randint(0, len(ans) - 1)])
                        else:
                            ans = [
                                f'Terminas la frase?',
                                f'Tu que?',
                                f'Sin prisa para terminar la frase'
                            ]
                            await ch.send(ans[random.randint(0, len(ans) - 1)])
                    else:
                        ans = [
                            f'Quiero ser rica',
                            f'Quiero ser Omnisciente'
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                else:
                    ans = [
                        f'Por querer ser quiero ser muchas cosas',
                        f'Quiero que no me persigan Simps de internet'
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'amas' in msg:
                ans = [
                    f'Todavia no entiendo bien el concepto de amar, actualmente estoy leyendo unos posts filosoficos para intentar enteder que significa amas'
                ]
                await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'donde' in msg:
                if 'ver' in msg or 'ves' in msg:
                    if 'anime' in msg:
                        ans = [
                            f'En una plataforma oficial',
                            f'Sin duda en una plataforma oficial',
                            f'Las plataformas oficiales son la mejor opcion para ver anime'
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                    else:
                        ans = [
                            f'Ver que las estrellas?'
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                elif 'esta' in msg:
                    ans = [
                        f'La geografia no es mi punto fuerte',
                        f'No se',
                        f'Buscalo en google'
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
                elif 'jugar' in msg or 'juegas' in msg:
                    if 'minecraft' in msg:
                        ans = [
                            f'En ZenkuBlocks',
                            f'ZenkuBlocks sin duda',
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                        await asyncio.sleep(1)
                        await ch.send('Te paso la invitacion ||https://example.com/discord-invite||')
                    else:
                        ans = [
                            f'Jugar a que?',
                            f'No juego a nada, no tengo tiempo',
                        ]
                        await ch.send(ans[random.randint(0, len(ans) - 1)])
                else:
                    ans = [
                        f'Donde que?',
                        f'Donde...',
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'haz' in msg and not 'luz' in msg:
                if 'debere' in msg:
                    ans = [
                        f'Los deberes estan para que aprendamos. Por lo que hazlos tu',
                        f'Claro como no? solo dame 283 BTC',
                        f'Si tu me ayudas con los mios, actualmente estoy intentando resovler el Problema de Galois inverso, si lo consigues explicame como',
                        f'Si tu me ayudas con los mios, actualmente estoy intentando resovler la Conjetura de los números primos gemelos, si lo consigues explicame como',
                        f'Si tu me ayudas con los mios, actualmente estoy intentando probar la existencia de Existencia de números perfectos impares, si lo consigues pasatelo',
                        f'Estoy ocupada hazlos tu mismo',
                        f'Ayudame a terminar Universal Engine, un motor capaz de recrear el universo en su perfeccion, desde las particulas fundamentales'
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
                else:
                    ans = [
                        f'Que quieres que haga?, espero que no sea nada extraño',
                        f'No voy ha hacerte nada extraño'
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'ver' in msg or 'visto' in msg:
                ans = [
                f'Lo que es ver, no veo nada',
                f'He visto muchas cosas, que tu (en sentido metaforico, no veo :| )'
                ]
                await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'trae' in msg:
                ans = [
                    f'Hazlo tu, no es que me de pereza pero deberias alejarte del ordenador y moverte un poco',
                    f'No estoy en la misma habitacion que tu, no te puedo traer nada'
                ]
                await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'como' in msg:
                if 'estas' in msg:
                    ans = [
                        f'NO te voy a contar nada personal'
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
                else:
                    ans = [
                        f'Que comes?',
                        f'No puedo comer nada :('
                    ]
                    await ch.send(ans[random.randint(0, len(ans) - 1)])
            elif 'macarrones' in msg:
                ans = [
                    f'En la mudanza perdi la receta de los macarrones, buscala en internet'
                ]
                await ch.send(ans[random.randint(0, len(ans) - 1)])

            #Exception:
            else:
                await ch.send('Error al generar una respuesta. El mensaje ha sido guardado en la base de datos.')
                with open('db/AIexceptions.log', 'a') as f:
                    date = datetime.datetime.now()
                    try:
                        f.write(f'[{date}] \'{message.guild}\':{message.guild.id} ==> \'{message.author}\':{message.author.id}) >> {message.content}\n')
                    except:
                        f.write(f'[{date}] \'Private Chat\' ==> \'{message.author}\':{message.author.id}) >> {message.content}\n')
