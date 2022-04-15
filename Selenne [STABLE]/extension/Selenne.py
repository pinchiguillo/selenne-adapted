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
            
            #Exception:
            else:
                await ch.send('Error al generar una respuesta. El mensaje ha sido guardado en la base de datos.')
                with open('db/AIexceptions.log', 'a') as f:
                    date = datetime.datetime.now()
                    f.write(f'[{date}] \'{message.guild}\':{message.guild.id} ==> \'{message.author}\':{message.author.id}) >> {message.content}\n')
