import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': '*s.g* or *s.genshin*',
        'specific_display': {
            's.g build [character]': 'Displays the recomended build of a character'
            }
        }

    add_help()

    #ADD CMD
    bot.add_command(g)
    bot.add_command(genshin)

    #Listeners
    bot.add_listener(on_message)

    #END
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

bot_version = 'Selenne 4.8.6'
version = 'GenshinTools: 1.4.1'
ename = 'Genshin Tools'

db_path = 'db/genshin.json'

colours = {'electro':0xb328c1, "cryo":0x1dbacb, "hydro":0x0074e8, "geo":0xd09917, "anemo":0x0bddb3, "pyro":0xe26f05, "dendro":0x1cb041}
elements = {'electro':'<:elemento_electro:982576510890311720> ', "cryo":'<:elemento_cryo:982576511360045086>', "hydro":'<:elemento_hydro:982576510760267816>', "geo":'<:elemento_geo:982576510965792778>', "anemo":'<:elemento_anemo:982576511297138748>', "pyro":'<:elemento_pyro:982576510160502804>', "dendro": "<:elemento_dendro:982576511435538483>"}

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)

def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        global db
        db =  json.load(f)
def save_db():
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5, ensure_ascii = False)

@commands.command()
async def genshin(ctx, mode = None, *, args = None):
    await genshin_core(ctx,mode,args)

@commands.command()
async def g(ctx, mode = None, *, args = None):
    await genshin_core(ctx,mode,args)

async def genshin_core(ctx,mode,args):
    #await ctx.message.delete()
    load_db()
    match mode.lower():
        case 'build': await builds(ctx,args)
        case 'news': pass
        case 'code':pass
        case 'leaks': 
            leaks_role = discord.utils.get(ctx.guild.roles, name=db['leaks'][str(ctx.guild.id)]['role'])
            await ctx.author.add_roles(leaks_role, reason='used s.g leaks')
            ch_id = db['leaks'][str(ctx.guild.id)]['channel']
            await ctx.reply(f'Ya puedes ver los leaks en <#{ch_id}>')
        
        case None: await ctx.send('Wrong Syntax', delete_after=10)
        case _: await ctx.send('Wrong Syntax', delete_after=10)


async def builds(ctx, args):
    load_db()

    #Displays All characters list
    if not args:
        embed = discord.Embed(title = 'Builds - Selenne', color = bot.color)
        characters = {'electro': '', 'cryo': '', 'hydro': '', 'geo': '', 'anemo': '', 'pyro': ''} #, 'dendro': ''
        for key in db['build'].keys():
            element = elements[db['build'][key]['element']]
            characters[db['build'][key]['element']] += f'{element} {key}\n'
                
        for key in characters.keys():
            element = elements[key]
            embed.add_field(name = f'{element} {key.capitalize()} {element}', value=characters[key].removesuffix('\n'), inline=True)
        await ctx.send(embed=embed)
        return
    
    if args == '-all':
        if ctx.author.id in bot.developers:
            for key in db['build'].keys():
                await ctx.send(embed=embedgenerator(key))
            return
        else:
            await ctx.send('You are not allowed to run this command')
            return

    #Check if character in db
    in_db = False
    for key in db['build'].keys():
        if args.lower() in db['build'][key]['alias']:
            in_db = True
            break
    
    if in_db:
        await ctx.send(embed=embedgenerator(key))
    else:
        await ctx.send('This character is not in the DB')

def embedgenerator(key):
    #Build related data
    build = db['build'][key]
    element = elements[build['element']]
    #Creates the Stars
    if build['stars'] == 5: stars = '⭐️⭐️⭐️⭐️⭐️'
    elif build['stars'] == 4: stars = '⭐️⭐️⭐️⭐️'

    #Initial Embed generation
    embed = discord.Embed(title = f'{key} - Build', description = stars, color = colours[build['element']])
    embed.set_thumbnail(url = build['img-url'])

    #Roles statement
    try:
        roles = ''
        for role in build['role']:
            roles += f"{role}, "
        roles = roles.removesuffix(', ')
    except: roles = 'Cant Load'
    embed.add_field(name = f'{element} Roles', value=roles, inline=False)
    
    #Weapons statment
    try:
        weapons = ''
        for weapon in db['build'][key]['weapons']['5']:
            weapons += f'{weapon} (5)\n'
        for weapon in db['build'][key]['weapons']['4']:
            weapons += f'{weapon} (4)\n'
        weapons = weapons.removesuffix('\n')
    except: weapons = 'Cant Load'
    embed.add_field(name = f'{element} Armas', value=weapons, inline=False)
    
    #Artifacts statment
    try:
        artifacts = ''
        for build_ in build['artifacts']['sets']:
            build_ = set_emogi(build_)
            artifacts += f'{build_} \n'
        artifacts = artifacts.removesuffix('\n')
    except: artifacts = 'Cant Load'
    embed.add_field(name = f'{element} Artefactos', value=artifacts, inline=False)
    
    #Artifact stats statment
    try:
        stats = ''
        for part in list(db['build'][key]['artifacts']['stats'].keys()):
            stat = db['build'][key]['artifacts']['stats'][part]
            p = part.capitalize()
            stats += f'**{p}**: {stat}\n'
        stats = stats.removesuffix('\n')
    except Exception as error: stats = 'Cant Load'
    embed.add_field(name = f'{element} Stats Artefactos', value=stats, inline=False)
    
    #Artifact stats priority statment
    try:
        sps = ''
        for sp in db['build'][key]['stats-priority']:
            sps += f'{sp}\n'
        sps = sps.removesuffix('\n')
    except: sps = 'Cant Load'
    embed.add_field(name = f'{element} Prioridad de Stats', value=sps, inline=False)
    
    #Teams statment
    try:
        teams = ''
        for team in db['build'][key]['teams']:
            teams += f'{team}\n'
        teams = teams.removesuffix('\n')
    except: teams = 'Cant Load'
    embed.add_field(name = f'{element} Equipos', value=teams, inline=False)
    
    #Version statment
    try:
        v = db['build'][key]['version']
    except: v = 'Cant Load'
    embed.set_footer(text = f'Ultima revisión de la build en la {v}')
    
    return embed

def set_emogi(build):
    build = build.replace('Doncella Amada', 'Doncella Amada <:Set_Doncella_Amada:982105860543238144>')
    build = build.replace('Virtuoso Corredor de Lava', 'Virtuoso Corredor de Lava <:Set_Virtuoso_Corredor_de_Lava:982105860396417055>')
    build = build.replace('Domador de_Truenos', 'Domador de_Truenos <:Set_Domador_de_Truenos:982105859784069202>')
    build = build.replace('Sombra Verde Esmeralda', 'Sombra Verde Esmeralda <:Set_Sombra_Verde_Esmeralda:982040697421037619>')
    build = build.replace('Bruja Carmesí en Llamas', 'Bruja Carmesí en Llamas <:Set_Bruja_Carmesi_en_Llamas:982040697257468005>')
    build = build.replace('Llamas Albinas', 'Llamas Albinas <:Set_Llamas_Albinas:982040697161015376>')
    build = build.replace('Furia del Trueno', 'Furia del Trueno <:Set_Furia_del_Trueno:982040697064529920>')
    build = build.replace('Petra Arcaica', 'Petra Arcaica <:Set_Petra_Arcaica:982040695214862367>')
    build = build.replace('Caballería Sanguinaria', 'Caballería Sanguinaria <:Set_Caballera_Sanguinaria:982040695034478632>')
    build = build.replace('Corazón de las Profundidades', 'Corazón de las Profundidades <:Set_Corazon_de_las_Profundidades:982040694619275264>')
    build = build.replace('Nómada del Invierno', 'Nómada del Invierno <:Set_Nomada_del_Invierno:982040690584342628>')
    build = build.replace('Perla Oceánica', 'Perla Oceánica <:Set_Perla_Oceanica:982040142372036659>')
    build = build.replace('Orquesta del Errante', 'Orquesta del Errante <:Set_Orquesta_del_Errante:982040140694310932>')
    build = build.replace('Ritual Antiguo de la Nobleza', 'Ritual Antiguo de la Nobleza <:Set_Ritual_Antiguo_de_la_Nobleza:982040139666710571>')
    build = build.replace('Retroceso del Meteorito', 'Retroceso del Meteorito <:Set_Retroceso_del_Meteorito:982040139540856832>')
    build = build.replace('Cáscara de Sueños Opulentos', 'Cáscara de Sueños Opulentos <:Set_Cascara_de_Sueos_Opulentos:982039615546478622>')
    build = build.replace('Eco del Sacrificio', 'Eco del Sacrificio <:Set_Eco_del_Sacrificio:982039615370321980>')
    build = build.replace('Deceso del Cinabrio', 'Deceso del Cinabrio <:Set_Deceso_del_Cinabrio:982039615177379860>')
    build = build.replace('Reminiscencia de la Purificación', 'Reminiscencia de la Purificación <:Set_Reminiscencia__Purificacion:982039614774718594>')
    build = build.replace('Tenacidad de la Geoarmada', 'Tenacidad de la Geoarmada <:Set_Tenacidad_de_la_Geoarmada:982039612061024256>')
    build = build.replace('Emblema del Destino', 'Emblema del Destino <:Set_Emblema_del_Destino:982039608802046014>')
    build = build.replace('Final del Gladiador', 'Final del Gladiador <:Set_Final_del_Gladiador:982038569113767957>')

    return build


#! LEAKS

@commands.Cog.listener()
async def on_message(message):
    
    #? Obtener Leaks y publicar
    if message.guild.id == 981601237562716180 and message.channel.id == 992042941537329163:
        leak = message.content.replace('@Leaks Ping', '')

        imgs = list()
        for element in message.attachments:
            imgs.append(await element.to_file())


        #Load guilds
        load_db()
        for guild in db['leaks'].keys():
            g = await bot.fetch_guild(int(guild))
            ch = await g.fetch_channel(db['leaks'][guild]['channel'])
            id = db['leaks'][guild]['role']
            await ch.send(f'**Nuevo Leak** ||<@​&{id}>||\n\n{leak}', files=imgs)
