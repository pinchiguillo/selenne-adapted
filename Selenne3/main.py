#DCS BOT V4.3 - Selenne
#Desarrollado por DCS Network
#
#CODE:
#Import

from colorama import Fore, init
import json
import discord
from discord import activity
from discord import channel 
from discord.ext import commands
from discord.embeds import Embed
import asyncio
from datetime import datetime

from dcs.AI import reg
from dcs.functions import f_lib

#Inicializar bot
init()
print(f'{Fore.YELLOW}Iniciando bot...{Fore.RESET}')
#Cargar archivo de configuracion principal
try:
    main_config = reg.read('config.json')
    print(f'{Fore.GREEN}Configuracion inicial cargada{Fore.RESET}')
except:
    print(f'{Fore.RED}ERROR: No se puedo cargar el archivo de configuracion inicial{Fore.RESET}')
    exit()
#Obtencion de datos
bot_version = main_config['BOT_version']

print(f'{Fore.BLUE}Booting bot {Fore.MAGENTA}{bot_version}{Fore.RESET}')
bot = commands.Bot(
    command_prefix = main_config["cmd_prefix"],
    description = main_config["description"],
    activity=discord.Game(name = str(main_config["activity"])),
    status=discord.Status.do_not_disturb)
print(f'{Fore.BLUE}Loading Main Vars...{Fore.RESET}')
#Global vars
bot.bot_prefix = main_config["cmd_prefix"]
bot.sys_dir = main_config['bot.sys_dir']
bot.bot_name = main_config["bot.bot_name"]
bot.bot_auth = main_config["bot.bot_auth_enforce"]
bot.bot_auth = bot.bot_auth + reg.get_user_with(reg.read(bot.sys_dir + '/users.json'), var = 'auth', value = True)
bot.bot_ignore = reg.get_user_with(reg.read(bot.sys_dir + '/users.json'), var = 'ignored', value = True)
print(f'{Fore.BLUE}Loading Per Bot Vars...{Fore.RESET}')
bot.bypass = False
bot.act = main_config['active']
print(f'{Fore.BLUE}Loading Per Server Vars...{Fore.RESET}')
#No Updated

#                                                                               Internal Functions
def save_log(author, guild, msg:str):
    with open(bot.sys_dir + '/logs.log', 'a', encoding='utf-8') as file:
            date = datetime.now()
            file.write(f'[{date}]:{guild.id}({guild}) : {author.id}({author})>> {msg}\n')

#                                                                               ON READY MODULE
print(f'{Fore.MAGENTA}Loading boot functions...{Fore.RESET}')
@bot.event
async def on_ready():
    print(f'{Fore.GREEN}BOT ONLINE{Fore.RESET}')

print(f'{Fore.GREEN}DONE{Fore.RESET}')
#                                                                               MAIN BOT MODULE
print(f'{Fore.MAGENTA}Loading bot.main...{Fore.RESET}')
@bot.event
async def on_message(message):
    #Detectar que no es un bot
    if not message.author.bot and not message.author.id in bot.bot_ignore:
        #Inicializar Variables
        ch = message.channel
        guild = message.guild
        author = message.author
        msg = message.content

        #Comprobar si el usuario esta en la DB y si no añadirlo
        if not reg.read(bot.sys_dir + '/users.json', author.id):
            reg.create(bot.sys_dir + '/users.json', author.id, str(author), 0, False, '', False)
            print(f'{Fore.YELLOW}Nuevo usuario detectado{Fore.RESET}')
            save_log(author, guild, 'Nuevo usuario añadido a la base de datos')
        else:
            author_data = reg.read(bot.sys_dir + '/users.json', author.id)

        #COMMANDS MODULE
        if bot.bot_prefix in msg and bool(author_data['auth']):
            if f'{bot.bot_prefix}help' == msg:
                embed=discord.Embed(title = f'CMD List', description = f' All avilable commands below', color = int(main_config['bot_color'], 16))
                embed.add_field(name = f'ERROR', value = 'Unable to get CMD.list', inline = False)
                save_log(author, guild, 'CMD:Help')
                await message.reply(embed=embed)
            if f'{bot.bot_prefix}reload' == msg:
                bot.bot_prefix = main_config["cmd_prefix"]
                bot.sys_dir = main_config['bot.sys_dir']
                bot.bot_name = main_config["bot.bot_name"]
                bot.bot_auth = main_config["bot.bot_auth_enforce"]
                bot.bot_auth = bot.bot_auth + reg.get_user_with(reg.read(bot.sys_dir + '/users.json'), var = 'auth', value = True)
                bot.bot_ignore = reg.get_user_with(reg.read(bot.sys_dir + '/users.json'), var = 'ignored', value = True)
                ms = await message.reply('Configuracion recargada')
                print(f'{Fore.CYAN}{author.id} reloaded config{Fore.RESET}')
                save_log(author, guild, 'CMD:reload')
                await asyncio.sleep(5)
                await message.delete()
                await ms.delete()
            if f'{bot.bot_prefix}config.display' == msg:
                embed=discord.Embed(title = f'Config', description = f'', color = int(main_config['bot_color'], 16))
                embed.add_field(name = f'ERROR', value = 'Unable to get config.display', inline = False)
                await ch.send(embed=embed)
                save_log(author, guild, 'CMD:config.display')
        else:
            #Adecuacion de msg
            msg = f_lib.adecuate(msg, accent=False, special_char=False, lower_upper='lower')

            #Detectar si es llamado el bot y eliminar su mencion de la str
            mentioned = f_lib.appear(bot.bot_name, msg)
            
            #Detectar mencion
            if mentioned or bot.bypass or not guild:
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
                #Aprende - outdated
                elif 'aprende' in msg:
                    await ch.send(f'Luego en un rato me pongo a aprenderlo')
                    f = open('db/lern.log', 'a')
                    save = str(msg).removeprefix('sele aprende ')
                    date = datetime.now()
                    f.write(f'[{date}]:{guild.id}({guild}) : {author.id}({author})>> {msg}\n')
                    f.close()

print(f'{Fore.GREEN}DONE{Fore.RESET}')
#                                                                               Adittional COGS
print(f'{Fore.MAGENTA}Loading daditional cogs...{Fore.RESET}')

print(f'{Fore.GREEN}DONE{Fore.RESET}')
#                                                                               ON JOIN MODULE
print(f'{Fore.MAGENTA}Loading On Join Parameters...{Fore.RESET}')
@bot.event
async def on_member_join(member):
    pass

print(f'{Fore.GREEN}DONE{Fore.RESET}')
#                                                                           BOT UPLOAD -- DO NOT TOUCH
print(f'{Fore.BLUE}Launching Bot...{Fore.RESET}')
try:
    bot.run(main_config['TOCKEN'])
except:
    print(f'{Fore.RED}CRITICAL ERROR: Bot cant launch{Fore.RESET}')

"""
apagar bot
await bot.logout()
"""

#await prune_members(*, days, compute_prune_count=True, roles=None, reason=None)
#days (int) – The number of days before counting as inactive.

#reason (Optional[str]) – The reason for doing this action. Shows up on the audit log.

#compute_prune_count (bool) – Whether to compute the prune count. This defaults to True which makes it prone to timeouts in very large guilds. In order to prevent timeouts, you must set this to False. If this is set to False, then this function will always return None.

#roles (Optional[List[abc.Snowflake]]) – A list of abc.Snowflake that represent roles to include in the pruning process. If a member has a role that is not specified, they’ll be excluded.