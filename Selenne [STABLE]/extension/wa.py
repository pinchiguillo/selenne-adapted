import discord
from discord.ext import commands
import asyncio
import json

async def setup(b):
    global bot
    bot = b

    bot.add_command(wa)

version = 'WA: PRE-ALFA'

db_path = 'db/WA/'

with open(db_path + 'classes.json', 'r') as f:
    classes = json.load(f)

@commands.command()
async def wa(ctx, cmd = 'help', *, args = None):
    #Check if the user has an account
    try:
        with open(f'{db_path}/WA/users/{ctx.author.id}.usr', 'r') as f:
            file = f.read()
    except FileNotFoundError:
        #Create Button
        register_btn = discord.ui.Button(label = 'Register', style=discord.ButtonStyle.blurple)
        
        #Button Function
        async def register_f(interaction):
            embed = discord.Embed(title = "Create WA account", description = 'Selecciona Una Clase', color = bot.color)
            await interaction.response.send_message(embed=embed, view=ClassSelectorView(), ephemeral=True)
            #FIN
            await interaction.message.delete()

        register_btn.callback = register_f

        #Send Message
        view = discord.ui.View()
        view.add_item(register_btn)
        await ctx.send(f'Hola {ctx.author.display_name}, parece que quieres entrar a **WA** pero no tienes personaje.\nPara crear tu personaje haz click en **Register**.', view=view)
    else:
        await ctx.send('**Bienvenido!**')


class ClassSelector(discord.ui.Select):
    def __init__(self):
        
        
        options = []

        for character in classes:
            options.append(discord.SelectOption(label = character, description = classes[character]['simple']))

        super().__init__(placeholder='Choose your class', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        
        select_btn = discord.ui.Button(label = f'Select {self.values[0]} class', style=discord.ButtonStyle.blurple)
        view = discord.ui.View()
        view.add_item(select_btn)
        await interaction.response.send_message(classes[self.values[0]]['description'], ephemeral=True, view=view)

class ClassSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(ClassSelector())
        

