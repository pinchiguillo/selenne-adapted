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
import datetime as dt

#Unike
from discord.ui import Button, View

from dcs.AI import reg
from dcs.functions import f_lib

from discord.ui import Button, View

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

@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx):
    await ctx.send('Starting Purge...')
    roles_ = []
    roles_.append(discord.utils.get(ctx.guild.roles, name='Tester'))
    roles_.append(discord.utils.get(ctx.guild.roles, name='Muted'))
    await ctx.guild.prune_members(days = 7, compute_prune_count = False, roles = roles_, reason='AFK')
    await ctx.send('Done')

@bot.command()
async def hello(ctx):
    print('btn')
    button = Button(label = 'Click Me!', style = discord.ButtonStyle.green)
    view = View()
    view.add_item(button)
    await ctx.send('Hi', view = view)

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