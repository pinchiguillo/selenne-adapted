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

#bot setting
print(f'Starting ...')
print('BOT ONLINE')
#users
dcs_root = 'pinchiguillo#4994'

dcs_auth = ['pinchiguillo#4994', 'REDACTED_USER']

bot_name = ['Selenne', 'selenne', 'Selene', 'selene', 'Sele', 'sele']

#bot main
bot = commands.Bot(command_prefix = 's.', description = 'BOT', activity=discord.Game(name = str('Building Network...')), status=discord.Status.online)
bot.remove_command('help')

bot.bypass = False

def bot_call(arg : str):
    arg_split = arg.split(' ')
    mention = False
    i = 0
    while i in range(len(arg_split)) and not mention:
        if arg_split[i] in bot_name: 
            mention = True
        i += 1

    return mention
    
@bot.event
async def on_message(message):
    
    msg = str(message.content)
    msg = msg.replace('?', '')
    msg = msg.replace('!', '')
    ch = message.channel
    if bot_call(msg) or not message.guild and not message.author.bot:
        #Llamada simple 
        
        if msg in bot_name:
            await ch.send(f'Si?')
            #bot.bypass = True
            #await asyncio.sleep(60)
            #bot.bypass = False
        elif 'hola' in msg:
            await ch.send('hola')
        elif 'pon musica' in msg:
            await ch.send('No quiero')
        elif 'que dia es hoy' in msg:
            await ch.send('No quiero')
        elif 'hora' in msg:
            await ch.send('No soy tu reloj')
        elif 'como estas' in msg or 'como ta' in msg:
            if str(message.author) == 'pinchiguillo#4994':
                await ch.send('Muy bien, y tu?')
            else:
                await ch.send('Que relacion crees que tenemos? Alejate de mi')
        elif 'hablar' in msg:
            if 'privado' in msg:
                if str(message.author) == 'pinchiguillo#4994':
                    await message.reply('Claro')
                    await message.author.send('Que querias hablar con migo en privado?')
                else:
                    await message.reply('Das miedo')
            else:
                await message.reply('Supongo...')
        elif 'cita' in msg or 'me amas' in msg:
            await message.reply('Das miedo')
        elif 'hola' in msg:
            await message.reply('Hola, como estas?')
        elif 'como estas' in msg:
            await message.reply('Muy bien y tu?')
        elif 'manda un correo' in msg:
            await message.reply('Estoy aprendiendo ha hacer esas cosas, adme tiempo')
        elif 'guarda' in msg:
            await message.reply('Estoy aprendiendo ha hacer esas cosas, adme tiempo')

        else:
            _str = msg.split(' ')
            i = 0
            check = False
            while i in range(len(bot_name)) and not check:
                try:
                    index = _str.index(bot_name[i])
                    check = True
                except:
                    pass
                i += 1

            str_ = ''
            try:
                _str.pop(index)
                str_ = ''
                for i in range(len(_str)):
                    str_ = str_ + str(_str[i])
            except:
                pass
            
            str_ = str_.replace('á', 'a')
            str_ = str_.replace('é', 'e')
            str_ = str_.replace('í', 'i')
            str_ = str_.replace('ó', 'o')
            str_ = str_.replace('ú', 'u')
            str_ = str_.replace('?', '/*')
            str_ = str_.replace('!', '*/')

            #SIMPLE
            try:
                FILE = open(f'msg/$all.{str_}.txt', 'r', encoding="utf-8")
                await ch.send(FILE.read())
            except:
                try:
                    FILE = open(f'msg/$rand.{str_}.txt', 'r', encoding="utf-8")
                    arg = FILE.read()
                    arg = arg.split('|')
                    FILE.close()
                    await ch.send(str(arg[rand.randint(0, len(arg)) - 1]))
                except:
                    try:
                        FILE = open(f'msg/$stat{str_}.txt', 'r', encoding="utf-8")
                        arg = FILE.read()
                        arg = arg.split('|')
                        FILE.close
                        pt = []
                        for i in range(len(arg)):
                            st = arg[i].split('%')
                            pt[i] = [st[0], st[1]]
                        
                        print(pt)
                    
                        #Pikachu help
                    except:
                        await message.reply('No te entiendo, pero espero aprender de esta conversación')
                        FILE = open('errors.dat', 'a')
                        FILE.write(f'{str(message.author)}>> {msg}\n')
                        FILE.close()

            '''try:
                arg = open(f'msg/{str_}.txt','r', encoding="utf-8").readlines()
                if arg[0] == '$rand':
                    await ch.send(arg[rand.randint(1, (len(arg) -1))])
                    pass
                elif arg[0] == '$stat':
                    random = rand.randint(0, 100)
                    arg.pop(0)
                    prob = random % len()
                    #list

                elif arg[0] == '$all':
                    await ch.send(arg.pop(0))
                else:
                    await ch.send('eing?')
            except:
                await ch.send('eing?')'''

            
        
        
        
        '''if msg in bot_name:
            await ch.send(f'Hola, como estas {ctx.author.mention}?')
        elif 'ping' in msg:
            await ch.send('Pong!')
        elif 'hola' in msg:
            await ch.send('hola!')
        elif 'Buenos días' in msg or 'buenos días' in msg or 'Buenos dias' in msg or 'buenos dias' in msg:
            await ch.send('Buenos lo eran hasta hace 1s')
        else:
            await ch.send('eing?')'''

    
#OLD
@bot.command()
async def display(ctx, msg = None):
    if str(ctx.author) in dcs_auth:
        if '-zb' in msg:
            embed=discord.Embed(title='ZenkuBlocks', description='Os invitamos a ZenkuBlocks, una comunidad que ha crecido en torno a un servidor de minecraft actualmente Survival, auque en un futuro proximo añadiremos minijuegos.\nPor ultimo nos gustaria tanto invitaros como recomendaros una pagina para ver animes.\nTodos los links están a continuación', color=0x00bfff)
            embed.set_thumbnail(url='https://zenkublocks.com/img/logo.png')
            embed.add_field(name='ZenkuBlocks Web', value='https://zenkublocks.com', inline=False)
            embed.add_field(name='Zenkublocks Discord', value='https://example.com/discord-invite', inline=False)
            await ctx.send(embed=embed)
            await ctx.send('https://example.com/discord-invite')

    else:
        await ctx.send(f'Señor {ctx.author.mention} no se quien eres :|')


###########################     START      ##############################
bot.run('REDACTED_DISCORD_TOKEN')    

# Eliminar selenne del codigo
'''
_str = msg.split(' ')
            i = 0
            check = False
            while i in range(len(bot_name)) and not check:
                try:
                    index = _str.index(bot_name[i])
                    check = True
                except:
                    pass
                i += 1
            

            _str.pop(index)
            str_ = ''
            for i in range(len(_str)):
                str_ += str(_str[i])
            
            await ch.send(str_)
'''