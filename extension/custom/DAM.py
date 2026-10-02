import sys
sys.dont_write_bytecode = True

import Selenne

#? Discord library and shortcuts
import discord
from discord.ext import commands
from discord import app_commands

#? Required for documentation (can be removed)
from ctypes import Union
import datetime
from typing import Sequence

#? Extra Libraries
import os, json, yaml

#! Extension Name (if not the filename will be used)
__EXTENSION_NAME__ = ''

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))

    global selenne
    selenne = bot

    #! Add cog Classes    
    COGS = []

    for cog in COGS:
        try: await bot.add_cog(cog(bot))
        except Exception as e: bot.logger.error('Failed to load cog: {}: {}'.format(cog.__name__, e))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

if not __EXTENSION_NAME__: __EXTENSION_NAME__ = os.path.splitext(os.path.basename(__file__))[0]

#! Extension Code

#? Sample
class DAM(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

        self.db_path = 'LDB/DAM'

        global db_path
        db_path = self.db_path
    
    @discord.app_commands.command(name = 'dam')
    @discord.app_commands.describe()
    async def dam_slashCommand(self, interaction: discord.Interaction):
        """Notas de DAM del año 2022-2023"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        #? Access lists hold Discord user IDs, so they live in an untracked users.json
        users_file = os.path.join(self.db_path, 'users.json')
        if not os.path.exists(users_file): users_file = os.path.join(self.db_path, 'users.example.json')

        with open(users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if interaction.user.id in data['DAM1']:
            embed = discord.Embed(title = 'DAM I - Apuntes', description = 'Herramienta desarrollada por ***pinchiguillo*** para cubrir la falta de profesores', color=self.bot.color)

        elif interaction.user.id in data['DAM2']:
            embed = discord.Embed(title = 'DAM II - Apuntes', description = 'Herramienta desarrollada por ***pinchiguillo*** para cubrir la falta de profesores :)', color=self.bot.color)

        elif not interaction.user.id in data['admin'].keys():
            await interaction.followup.send('No tienes acceso a las notas de DAM. Contacta con {} para obtener acceso')
            return
        
        if interaction.user.id in data['admin'].keys():
            permissions = data['admin'][interaction.user.id]
        
        embed.add_field(name = 'Apuntes', value = 'Dentro de este apartado podras encontrar miniresumenes que explican las partes mas importantes y esenciales. Tambien incluye tips para aprenderse algunos contenidos', inline = False)
        embed.add_field(name = 'Ejercicios extra', value = 'Por si quieres mas ejercicios y/o los de clase no tienen suficiente dificultad aqui tendras multiples ejercicios extra', inline = False)
        embed.add_field(name = 'Solución de dudas', value = 'Tambien puedes consultar dudas :)', inline = False)
        embed.set_footer(text = 'Herramienta desarrollada por Pinchiguillo')

        await interaction.followup.send(embed=embed, view=MainView(target='DAM1', permissions=permissions))

#! VIEWS
class MainView(discord.ui.View):
    cfg = {
        'apuntes': False,
        'Ejercicios': False,
        'Dudas': False,
        'Soporte': False,
        'Calendar': False,
    }
    
    def __init__(self, target:str=None, permissions:str=None):
        super().__init__()

        self.target = target
        self.permissions = permissions

    @discord.ui.button(label = 'Apuntes', style=discord.ButtonStyle.blurple)
    async def apuntes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=None, view = Apuntes_View())

    @discord.ui.button(label = 'Ejercicios', style=discord.ButtonStyle.blurple, disabled=True)#!
    async def ejercicios(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Section Not loaded', ephemeral=True)

    @discord.ui.button(label = 'Dudas', style=discord.ButtonStyle.blurple)
    async def dudas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Dudas_Modal())

    @discord.ui.button(label = 'Soporte', style=discord.ButtonStyle.danger, disabled=True)#!
    async def soporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Support_Modal())

    @discord.ui.button(label = 'Calendar', style=discord.ButtonStyle.danger, disabled=True)#!
    async def calendar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Esta opcion es privada, hablar con **El señor delegado** y convencedlo de que sea publica :)', ephemeral=True)

class Apuntes_View(discord.ui.View):
    def __init__(self, target:str = None):
        super().__init__()

        self.target = target

        with open(os.path.join(db_path, 'displays.json')) as f:
            displays = json.load(f)[target]

        class AsignaturaSelector(discord.ui.Select):
            def __init__(self):

                options = []
                
                if 'code' in displays: options.append(discord.SelectOption(label = 'Programacion', emoji='<:programacion:1042141191925407785>', value = 'code'))
                if 'html' in displays: options.append(discord.SelectOption(label = 'HTML+CSS', emoji='<:html:1042141187823386725>', value = 'html'))
                if 'sisi' in displays: options.append(discord.SelectOption(label = 'Sistemas Informaticos', emoji='<:sisi:1042141186414092309>', value = 'sisi'))
                if 'db' in displays: options.append(discord.SelectOption(label = 'Bases de Datos', emoji='<:db:1042141184119812176>', value = 'db'))
                if 'ende' in displays: options.append(discord.SelectOption(label = 'Entornos de Desarrollo', emoji='<:ende:1042141190612594738>', value = 'ende'))
                if 'eng' in displays: options.append(discord.SelectOption(label = 'Ingles', emoji='🗣️', value = 'eng'))
                if 'fol' in displays: options.append(discord.SelectOption(label = 'Formación Profesional', emoji='👷', value = 'fol'))

                super().__init__(placeholder='Selecciona una asignatura', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                nview = discord.ui.View()
                match self.values[0]:
                    case 'code': nview.add_item(code_selector())
                    case 'html': nview.add_item(html_selector())
                    case 'sisi': nview.add_item(sisi_selector())
                    case 'db': nview.add_item(db_selector())
                    case 'ende': nview.add_item(ende_selector())
                    case 'eng': nview.add_item(eng_selector())
                    case 'fol': nview.add_item(fol_selector())
                
                embed = discord.Embed(title = 'Lectura',description = '🟩 **Explicado en clase**\n\n🟪 **Contenido extra**\n\n🟨**Contenido recomendable**\n\n🟥 **No explicado en clase**', color=bot_color)
                await interaction.response.edit_message(embed=embed, view=nview)
        
        class ContentSelector(discord.ui.Select):
            def __init__(self, subjetc):
                self.subjetc = subjetc

                with open(os.path.join(db_path, os.path.join(target, os.path.join(subjetc, 'index.json')))) as idxf:
                    idx = json.loads(idxf)

                options = []

                for topic in idx.keys():
                    match idx['topic']['type']:
                        case 'class': emj = '🟩'
                        case 'advice': emj = '🟪'
                        case 'extra': emj = '🟨'
                        case _: emj = '⛔'
                    options.append(
                        discord.SelectOption(label = idx[topic]['title'], description = idx[topic]['description'], emoji=emj, value = topic),
                    )

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open(os.path.join(db_path, f'DAM/{target}/{self.subjetc}/{self.values[0]}.json')) as df: 
                        embed = discord.Embed.from_dict(json.load(df))
                        embed.color = selenne.color
                        await interaction.response.edit_message(embed=embed)
                
                except:
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)
                            
        self.add_item(AsignaturaSelector())
