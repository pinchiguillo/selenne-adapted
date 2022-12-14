import sys
sys.dont_write_bytecode = True

import Selenne

import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional

__EXTENSION_NAME__ = 'Game-Dev-Tools'

#? Configuration
async def setup(bot:Selenne.Core):
    bot.logger.info('{} loaded'.format(__EXTENSION_NAME__))
    
    global bot_color, bot_database
    bot_color = bot.color
    bot_database = bot.database
    
    await bot.add_cog(GameALFA_cog(bot))

async def teardown(bot:Selenne.Core): bot.logger.info('{} unloaded'.format(__EXTENSION_NAME__))

#! Extension Code

#? Sample
class GameALFA_cog(discord.ext.commands.GroupCog, group_name = 'game', group_description = 'Tools that the game have (Will evolve to the game)'):
    def __init__(self, bot:Selenne.Core):
        self.bot = bot

    forge = app_commands.Group(name = 'forge', description = 'The Forge!')

    @forge.command(name= 'create')
    @discord.app_commands.describe()
    async def game_forge_view(self, interaction: discord.Interaction):
        """Create a new item in the Game Forge"""

        cursor = self.bot.database.cursor(buffered=True)
        SQL = "SELECT * FROM `blacksmith` WHERE `id` LIKE '000000000000000000'"
        cursor.execute(SQL)
        if len(cursor.fetchall()) == 0:
            embed = discord.Embed(title = 'Game Forge', description = 'Parece que no tienes cuenta de forjador, si quieres crear una haz click en crear cuenta.\n**Todos los datos se asociaran a tu id de discord guardado en nuestras bases de datos (no las de discord)**', color=self.bot.color)

            await interaction.response.send_message(embed=embed, view = Create_Account_View(), ephemeral=True)

        embed = discord.Embed(title = 'Game Forge', description = 'Bienvenido a la Forja!', color=self.bot.color)
        await interaction.response.send_message(embed=embed, view=Forge_View(), ephemeral=True)
    
    @forge.command(name= 'view')
    @discord.app_commands.describe()
    async def game_forge_view(self, interaction: discord.Interaction):
        """Show the created items in the forge"""
        await interaction.response.send_message('Not avilable', ephemeral=True)


class Forge_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

        #? Selector Classes

        class ItemTypeSelector(discord.ui.Select):
            def __init__(self):
                            
                options = [
                    discord.SelectOption(label = 'Class', emoji='<:class:1051088754724573184> ', value = 'game.entity.player.class'),
                    discord.SelectOption(label = 'Skill', emoji='<:skill:1051088757597667328> ', value = 'game.skill'),
                    discord.SelectOption(label = 'Entity', emoji='<:entity:1051088759191519262>', value = 'game.entity'),
                    discord.SelectOption(label = 'Item', emoji='<:item:1051088753239793674>', value = 'game.item'),
                    discord.SelectOption(label = 'Weapon', emoji='<:weapon:1051088760470773891> ', value = 'game.item.weapon'),
                    discord.SelectOption(label = 'Armour', emoji='<:armour:1051088762215600128>', value = 'game.item.armour'),
                    discord.SelectOption(label = 'Artifact', emoji='<:artifact:1051088755949314048> ', value = 'game.item.artifact'),
                    ]

                super().__init__(placeholder='Selecciona un tipo de item', min_values=1, max_values=1, options=options)

                        
            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title = 'Forge', description = 'Antes de continuar, en el juego no se encontrara una referencia directa hacia quien ha diseñado el item, no obstante el credito se entregara via referencias en el lore.', color=bot_color)
                
                await interaction.response.edit_message(embed=embed, view=Create_Game_View(self.values[0]))
                    
        self.add_item(ItemTypeSelector())

class Create_Account_View(discord.ui.View):
    def __init__(self):
        super().__init__()


    @discord.ui.button(label = 'Create Account', style=discord.ButtonStyle.green)
    async def game_forge_create_account(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Create_Account_Modal())

class Create_Account_Modal(discord.ui.Modal, title = 'Crear Cuenta de Forjador'):
    
    name = discord.ui.TextInput(
        label = 'Nombre',
        placeholder = '',
        required= True,
    )
    async def on_submit(self, interaction: discord.Interaction):

        cursor = bot_database.cursor(buffered=True)
        SQL = "INSERT INTO `blacksmith` (`id`, `name`) VALUES ('{}', '{}');".format(interaction.user.id, self.name.value)
        cursor.execute(SQL)

        await interaction.response.send_message('Welcome to the Forge!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong {}'.format(error), ephemeral=True)

class Create_Game_View(discord.ui.View):
    def __init__(self, create:str):
        self.__create__ = create
        super().__init__()

    @discord.ui.button(label = 'Agree', style = discord.ButtonStyle.green, disabled = True)
    async def game_forge_create_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        match self.__create__:
            case 'game.entity.player.class': 
                data = {
                    'name': 'None',
                    'description': 'None',
                    'stats': 'None',
                    'skills': 'None',
                }
                embed = Embeds.Class(data)
                view = Views.Class(data)
            case 'game.skill':
                data = {}
                embed = Embeds.Skill(data)
                view = None
            case 'game.entity':
                data = {}
                embed = Embeds.Entity(data)
                view = None
            case 'game.item':
                data = {}
                embed = Embeds.Item(data)
                view = None
            case 'game.item.weapon':
                data = {}
                embed = Embeds.Weapon(data)
                view = None
            case 'game.item.armour':
                data = {}
                embed = Embeds.Armour(data)
                view = None
            case 'game.item.artifact':
                data = {}
                embed = Embeds.Artifact(data)
                view = None
        
        await interaction.response.edit_message(embed=embed, view=view)

class Embeds():
    def Class(data:dict):  
        embed = discord.Embed(title='Creador de clases', color=bot_color)
        embed.add_field(name='Nombre', value=data['name'], inline=False)
        embed.add_field(name='Descripcion', value=data['description'], inline=False)
        embed.add_field(name='Stats', value=data['stats'], inline=False)
        embed.add_field(name='Habilidades', value=data['skills'], inline=False)

        return embed
    def Skill(data:dict): 
        embed = discord.Embed(title='Creador de habilidades', color=bot_color)
        #embed.add_field(name='', value='', inline=False)

        return embed
    def Entity(data:dict):
        embed = discord.Embed(title='Creador de entidades', color=bot_color)
        #embed.add_field(name='', value='', inline=False)

        return embed
    def Item(data:dict):
        embed = discord.Embed(title='Creador de items', color=bot_color)
        #embed.add_field(name='', value='', inline=False)

        return embed
    def Weapon(data:dict):
        embed = discord.Embed(title='Creador de armas', color=bot_color)
        #embed.add_field(name='', value='', inline=False)

        return embed
    def Armour(data:dict):
        embed = discord.Embed(title='Creador de armaduras', color=bot_color)
        #embed.add_field(name='', value='', inline=False)

        return embed
    def Artifact(data:dict):
        embed = discord.Embed(title='Creador de artefactos', color=bot_color)
        #embed.add_field(name='', value='', inline=False)

        return embed

class Views():
    class Class(discord.ui.View):
        def __init__(self, data:dict):
            self.__data__ = data
            super().__init__()

        class Edit_Modal(discord.ui.Modal, title = 'Edit general data'):
            def __init__(self, data:dict):
                self.__data__ = data
                super().__init__()
            
            name = discord.ui.TextInput(
                label = 'Nombre',
                placeholder = '',
                required= True,
            )
            description = discord.ui.TextInput(
                label = 'Descripcion',
                placeholder = '',
                required= True,
            )
            skills = discord.ui.TextInput(
                label = 'Habilidades',
                placeholder = '',
                required= True,
            )
            async def on_submit(self, interaction: discord.Interaction):
                self.__data__['name'] = self.name.value
                self.__data__['description'] = self.description.value
                self.__data__['skills'] = self.skills.value
                await interaction.response.edit_message(embed=Embeds.Class(self.__data__), view=Views.Class(self.__data__))
                    
            async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
                await interaction.response.send_message('Oops! Something went wrong {}'.format(error), ephemeral=True)

        class Edit_Stats_Modal(discord.ui.Modal, title = 'Crear Cuenta de Forjador'):    
            name = discord.ui.TextInput(
                label = 'Nombre',
                placeholder = '0',
                required= False,
            )
            
            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.send_message('Welcome to the Forge!', ephemeral=True)

            async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
                await interaction.response.send_message('Oops! Something went wrong {}'.format(error), ephemeral=True)        

        @discord.ui.button(label = 'Edit', style=discord.ButtonStyle.green)
        async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(self.Edit_Modal(self.__data__))

        @discord.ui.button(label = 'Edit Stats', style=discord.ButtonStyle.green, disabled=True)
        async def edit_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(self.Edit_Stats_Modal())
        
        @discord.ui.button(label = 'Save', style=discord.ButtonStyle.green)
        async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
            #! SAVE
            await interaction.response.edit_message(view=None)
