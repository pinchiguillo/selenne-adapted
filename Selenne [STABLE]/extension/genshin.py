import discord
from discord.ext import commands
import json

from regex import D

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': 'cmd',
        'specific_display': {
            'cmd': 'use'
            }
        }

    #add_help()

    #ADD CMD
    bot.add_command(g)
    bot.add_command(genshin)

    #END
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

version = 'GenshinTools: 1.1'
ename = 'Genshin Tools'

db_path = 'db/genshin.json'

colours = {'electro':0xb328c1, "cryo":0x1dbacb, "hydro":0x0074e8, "geo":0xd09917, "anemo":0x0bddb3, "pyro":0xe26f05}
elements = {'electro':'<:elemento_electro:982576510890311720> ', "cryo":'<:elemento_cryo:982576511360045086>', "hydro":'<:elemento_hydro:982576510760267816>', "geo":'<:elemento_geo:982576510965792778>', "anemo":'<:elemento_anemo:982576511297138748>', "pyro":'<:elemento_pyro:982576510160502804>'}

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
        return json.load(f)
def save_db(db:dict):
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
    db = load_db()
    save_db(db)
    match mode.lower():
        case 'build':
            if not args:
                embed = discord.Embed(title = 'Buidls - Selenne', color = bot.color)
                blds = ''
                for key in db['build'].keys():
                    element = elements[db['build'][key]['element']]
                    blds += f"{element} {key}\n"
                blds = blds.removesuffix('\n')
                embed.description = blds
                await ctx.send(embed=embed)
            in_db = False
            for key in list(db['build'].keys()):
                if args.lower() in db['build'][key]['alias']:
                    build = db['build'][key]
                    in_db = True
                    break
            if not in_db:
                await ctx.send(f'*{args}* is not in the db')
                return
            try:
                element = elements[db['build'][key]['element']]
                embed = discord.Embed(title = f'{key} - Build', color = colours[db['build'][key]['element']])
                embed.set_thumbnail(url=db['build'][key]['img-url'])
                roles = ''
                for role in db['build'][key]['role']:
                    roles += f"{role}, "
                roles = roles.removesuffix(', ')
                embed.add_field(name = f'{element} Roles', value=roles, inline=False)
                    
                weapons = ''
                for weapon in db['build'][key]['weapons']['5']:
                    weapons += f'{weapon} (5)\n'
                for weapon in db['build'][key]['weapons']['4']:
                    weapons += f'{weapon} (4)\n'
                weapons = weapons.removesuffix('\n')
                embed.add_field(name = f'{element} Armas', value=weapons, inline=False)

                builds = ''
                for build in db['build'][key]['artifacts']['sets']:
                    build = set_emogi(build)
                    builds += f'{build} \n'
                builds = builds.removesuffix('\n')
                embed.add_field(name = f'{element} Artefactos', value=builds, inline=False)
                stats = ''
                for part in list(db['build'][key]['artifacts']['stats'].keys()):
                    stat = db['build'][key]['artifacts']['stats'][part]
                    p = part.capitalize()
                    stats += f'**{p}**: {stat}\n'
                builds = builds.removesuffix('\n')
                embed.add_field(name = f'{element} Stats Artefactos', value=stats, inline=False)

                sps = ''
                for sp in db['build'][key]['stats-priority']:
                    sps += f'{sp}\n'
                sps = sps.removesuffix('\n')
                embed.add_field(name = f'{element} Prioridad de Stats', value=sps, inline=False)

                teams = ''
                for team in db['build'][key]['teams']:
                    teams += f'{team}\n'
                teams = teams.removesuffix('\n')
                embed.add_field(name = f'{element} Equipos', value=teams, inline=False)

                v = db['build'][key]['version']
                embed.set_footer(text = f'Ultima revision de la build en la {v}')

            
            except Exception as error:
                await ctx.send('Error while generating the embed', delete_after=10)
                bot.log.error(f'Genshin-Builds: {error}')
                return

            await ctx.send(embed=embed)
        
        case None: await ctx.send('Wrong Syntax', delete_after=10)
        case _: await ctx.send('Wrong Syntax', delete_after=10)


def set_emogi(build):
    build = build.replace('Doncella Amada', 'Doncella Amada <:Set_Doncella_Amada:982105860543238144>')
    build = build.replace('Virtuoso Corredor de Lava', 'Virtuoso Corredor de Lava <:Set_Virtuoso_Corredor_de_Lava:982105860396417055>')
    build = build.replace('Domador de_Truenos', 'Domador de_Truenos <:Set_Domador_de_Truenos:982105859784069202>')
    build = build.replace('Sombra Verde Esmeralda', 'Sombra Verde Esmeralda <:Set_Sombra_Verde_Esmeralda:982040697421037619>')
    build = build.replace('Bruja Carmesi en Llamas', 'Bruja Carmesi en Llamas <:Set_Bruja_Carmesi_en_Llamas:982040697257468005>')
    build = build.replace('Llamas Albinas', 'Llamas Albinas <:Set_Llamas_Albinas:982040697161015376>')
    build = build.replace('Furia del Trueno', 'Furia del Trueno <:Set_Furia_del_Trueno:982040697064529920>')
    build = build.replace('Petra Arcaica', 'Petra Arcaica <:Set_Petra_Arcaica:982040695214862367>')
    build = build.replace('Caballera Sanguinaria', 'Caballera Sanguinaria <:Set_Caballera_Sanguinaria:982040695034478632>')
    build = build.replace('Corazón de las Profundidades', 'Corazón de las Profundidades <:Set_Corazon_de_las_Profundidades:982040694619275264>')
    build = build.replace('Nomada del Invierno', 'Nomada del Invierno <:Set_Nomada_del_Invierno:982040690584342628>')
    build = build.replace('Perla Oceanica', 'Perla Oceanica <:Set_Perla_Oceanica:982040142372036659>')
    build = build.replace('Orquesta del Errante', 'Orquesta del Errante <:Set_Orquesta_del_Errante:982040140694310932>')
    build = build.replace('Ritual Antiguo de la Nobleza', 'Ritual Antiguo de la Nobleza <:Set_Ritual_Antiguo_de_la_Nobleza:982040139666710571>')
    build = build.replace('Retroceso del Meteorito', 'Retroceso del Meteorito <:Set_Retroceso_del_Meteorito:982040139540856832>')
    build = build.replace('Cascara de Sueos Opulentos', 'Cascara de Sueos Opulentos <:Set_Cascara_de_Sueos_Opulentos:982039615546478622>')
    build = build.replace('Eco del Sacrificio', 'Eco del Sacrificio <:Set_Eco_del_Sacrificio:982039615370321980>')
    build = build.replace('Deceso del Cinabrio', 'Deceso del Cinabrio <:Set_Deceso_del_Cinabrio:982039615177379860>')
    build = build.replace('Reminiscencia de la Purificación', 'Reminiscencia de la Purificación <:Set_Reminiscencia__Purificacion:982039614774718594>')
    build = build.replace('Tenacidad de la Geoarmada', 'Tenacidad de la Geoarmada <:Set_Tenacidad_de_la_Geoarmada:982039612061024256>')
    build = build.replace('Emblema del Destino', 'Emblema del Destino <:Set_Emblema_del_Destino:982039608802046014>')
    build = build.replace('Final del Gladiador', 'Final del Gladiador <:Set_Final_del_Gladiador:982038569113767957>')

    return build
