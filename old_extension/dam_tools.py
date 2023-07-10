import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import os
import yaml
import json

__EXTENSION_NAME__ = 'DAM Tools'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))

    global bot_color, logger
    bot_color = bot.color
    logger = bot.logger
    
    await bot.add_cog(DAM_cog(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
#! ?tag slash group

#! pip install --upgrade

class DAM_cog(commands.Cog):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    def load_data(self):
        with open(os.path.join(os.getcwd(), 'local_db/damcalendar.yaml'), 'r', encoding='utf8') as f:
            return yaml.safe_load(f)
    
    @discord.app_commands.command(name= 'dam')
    @discord.app_commands.describe()
    async def dam(self, interaction: discord.Interaction):
        """Show some DAM I notes"""
        
        with open('local_db/dam_notes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not interaction.user.id in data['users']: 
            await interaction.response.send_message('Lo siento no tienes permiso para ver este contenido', ephemeral=True)
            return

        embed = discord.Embed(title = 'DAM I - Apuntes', description = 'Herramienta desarrollada por ***pinchiguillo*** para cubrir la falta de profesores :)', color=self.bot.color)

        embed.add_field(name = 'Apuntes', value = 'Dentro de este apartado podras encontrar apuntes mas completos sobre todas las asignaturas. Cualquiera puede subir apuntes, de hecho se agradeceria que entre todos colaboraramos a crear esta plataforma', inline = False)
        embed.add_field(name = 'Ejercicios extra', value = 'Por si quieres mas ejercicios y/o los de clase no tienen suficiente dificultad aqui tendras multiples ejercicios extra', inline = False)
        embed.add_field(name = 'Solución de dudas', value = 'Tambien puedes consultar dudas :)', inline = False)
        embed.set_footer(text = 'Herramienta desarrollada por Pinchiguillo')

        view = Notes_Main_View()

        await interaction.response.send_message(embed=embed, view = view, ephemeral=True)

#! EXTRA
class Support_Modal(discord.ui.Modal, title = 'Soporte'):
    
    name = discord.ui.TextInput(
        label = 'Nombre',
        placeholder = '',
        required= True,
    )

    issue = discord.ui.TextInput(
        label='What do you think of this new feature?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        with open('local_db/dam_notes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        try:
            list(data['reportes'][self.name.value]).append([interaction.user.id ,self.issue.value])
        except:
            data['reportes'][self.name.value] = [interaction.user.id ,self.issue.value]

        with open('local_db/dam_notes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        await interaction.response.send_message('Reporte guardado', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong {}'.format(error), ephemeral=True)

class Dudas_Modal(discord.ui.Modal, title = 'Dudas'):
    
    name = discord.ui.TextInput(
        label = 'Nombre',
        placeholder = '',
        required= True,
    )

    dude = discord.ui.TextInput(
        label='Haz la consulta',
        style=discord.TextStyle.long,
        placeholder='Tu duda aqui...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        with open('local_db/dam_notes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        try:
            list(data['dudas'][self.name.value]).append([interaction.user.id ,self.dude.value])
        except:
            data['dudas'][interaction.user.id] = [self.name.value ,self.dude.value]

        with open('local_db/dam_notes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        await interaction.response.send_message('Duda enviada, te responderemos lo antes posible', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong {}'.format(error), ephemeral=True)
#!
class Apuntes_View(discord.ui.View):
    def __init__(self):
        super().__init__()

        #? Selector Classes
        class code_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Estructura basica', description = 'Una pequeña introduccion a la estructura de java', emoji='🟩', value = 'basic_structure'),
                    discord.SelectOption(label = 'Syntaxis (Correcta)', description = 'Practicas saludables en la syntaxis de java', emoji='🟪', value = 'syntax'),
                    discord.SelectOption(label = 'Tipos de Datos', description = 'Introducción a los tipos de datos en java', emoji='🟩', value = 'datatypes'),
                    discord.SelectOption(label = 'Operadores', description = 'Todos los operadores existentes en java', emoji='🟩', value = 'operators'),
                    discord.SelectOption(label = 'Try/Catch', description = 'Control de exepciones', emoji='🟨', value = 'try'),
                    discord.SelectOption(label = 'Funciones', description = 'La base necesaria para crear funciones', emoji='🟩', value = 'functions'),
                    discord.SelectOption(label = 'Bucles while', description = 'Primer tipo de bucle: While (y do-while)', emoji='🟩', value = 'while'),
                    discord.SelectOption(label = 'Bucles for', description = 'Segundo tipo de bucle: for', emoji='🟩', value = 'for'),
                    discord.SelectOption(label = 'Clases - Introduccion', description = 'Proximamente', emoji='⛔', value = 'class_intro'),
                    discord.SelectOption(label = 'Clases - constructores', description = 'Proximamente', emoji='⛔', value = 'class_builder'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/code/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        class html_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Introduccion a HTML', description = 'Una introduccion superficial a HTML', emoji='🟨', value = 'basic_html'),
                    discord.SelectOption(label = 'Estructura de un HTML5', description = 'Estructura basica de HTML', emoji='🟨', value = 'html5'),
                    discord.SelectOption(label = 'Etiquetas', description = 'Todas las etiquetas de HTML', emoji='🟩', value = 'tags'),
                    discord.SelectOption(label = 'Imagenes y Videos', description = 'Proximamente', emoji='🟩', value = 'img-vid'),
                    discord.SelectOption(label = 'Formularios', description = 'Proximamente', emoji='🟩', value = 'form'),
                    discord.SelectOption(label = 'Headers', description = 'Proximamente', emoji='⛔', value = 'headers'),
                    discord.SelectOption(label = 'Divisiones', description = 'Proximamente', emoji='⛔', value = 'div'),
                    discord.SelectOption(label = 'Introduccion a CSS', description = 'Proximamente', emoji='⛔', value = 'intro_css'),
                    discord.SelectOption(label = 'CSS Basico', description = 'Proximamente', emoji='⛔', value = 'basic_css'),
                    discord.SelectOption(label = 'Responsitive', description = 'Proximamente', emoji='⛔', value = 'responsitive'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/html/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        class sisi_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    #discord.SelectOption(label = 'Representacion de la Informacion I', description = 'Proximamente', emoji='⛔', value = 'ifno1'),
                    #discord.SelectOption(label = 'Representacion de la Informacion II', description = 'Proximamente', emoji='⛔', value = 'info2'),
                    #discord.SelectOption(label = 'Representacion de la Informacion III', description = 'Proximamente', emoji='⛔', value = 'info3'),
                    
                    #discord.SelectOption(label = 'Introduccion I', description = 'Proximamente', emoji='⛔', value = 'intro1'),
                    #discord.SelectOption(label = 'Introduccion II', description = 'Proximamente', emoji='⛔', value = 'intro2'),
                    #discord.SelectOption(label = 'Introduccion III - Algebra de Boole', description = 'Proximamente', emoji='⛔', value = 'intro3'),
                    #discord.SelectOption(label = 'Introduccion IV - Computadoras', description = 'Proximamente', emoji='⛔', value = 'intro4'),
                    
                    #discord.SelectOption(label = 'Coma Flotante', description = 'Proximamente', emoji='⛔', value = 'floating_point'),
                    #discord.SelectOption(label = 'Jerarquias de memoria', description = 'Proximamente', emoji='⛔', value = 'memory'),
                    
                    discord.SelectOption(label = 'SubNeting', description = 'Resumen Expres de Sub Netting', emoji='🟩', value = 'subneting'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/sisi/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        class db_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Try/Catch', description = 'Proximamente', emoji='⛔', value = 'try'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/code/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        class ende_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Try/Catch', description = 'Proximamente', emoji='⛔', value = 'try'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/code/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        class eng_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Try/Catch', description = 'Proximamente', emoji='⛔', value = 'try'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/code/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        class fol_selector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Try/Catch', description = 'Proximamente', emoji='⛔', value = 'try'),
                ]

                super().__init__(placeholder='Selecciona un tema', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                try:
                    with open('local_db/dam_apuntes/code/{}.json'.format(self.values[0]), 'r', encoding='utf-8') as f:
                        embed = discord.Embed.from_dict(json.load(f))
                    embed.color = bot_color
                    await interaction.response.edit_message(embed=embed)
                except Exception as e: 
                    await interaction.response.send_message('Apuntes no disponibles', ephemeral=True)

        #!
        class AsignaturaSelector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Programacion', emoji='<:programacion:1042141191925407785>', value = 'code'),
                    discord.SelectOption(label = 'HTML+CSS', emoji='<:html:1042141187823386725>', value = 'html'),
                    discord.SelectOption(label = 'Sistemas Informaticos', emoji='<:sisi:1042141186414092309>', value = 'sisi'),
                    #discord.SelectOption(label = 'Bases de Datos', emoji='<:db:1042141184119812176>', value = 'db'),
                    #discord.SelectOption(label = 'Entornos de Desarrollo', emoji='<:ende:1042141190612594738>', value = 'ende'),
                    #discord.SelectOption(label = 'Ingles', emoji='🗣️', value = 'eng'),
                    #discord.SelectOption(label = 'Formación Profesional', emoji='👷', value = 'fol'),
                    ]

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
                    
        self.add_item(AsignaturaSelector())

class Notes_Main_View(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    
    @discord.ui.button(label = 'Apuntes', style=discord.ButtonStyle.blurple)
    async def apuntes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=None, view = Apuntes_View())

    @discord.ui.button(label = 'Ejercicios', style=discord.ButtonStyle.blurple, disabled=True)#!
    async def ejercicios(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Section Not loaded', ephemeral=True) #! Cambiar a edit

    @discord.ui.button(label = 'Dudas', style=discord.ButtonStyle.blurple)
    async def dudas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Dudas_Modal())

    @discord.ui.button(label = 'Soporte', style=discord.ButtonStyle.danger)
    async def soporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Support_Modal())

    @discord.ui.button(label = 'Calendar', style=discord.ButtonStyle.danger)
    async def calendar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Esta opcion es privada, hablar con **El señor delegado** y convencedlo de que sea publica :)', ephemeral=True)
