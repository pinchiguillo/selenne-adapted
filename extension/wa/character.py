import extension.wa.core
import discord
import json

async def register(bot, ctx, args):
    #Create the button
    view = discord.ui.View()
    class Register_btn(discord.ui.Button):
        def __init__(self):
            super().__init__(style=discord.ButtonStyle.blurple, label='Register')

        async def callback(self, interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message('If you want to register use your own command', ephemeral=True)
                return
            
            with open('data/classes.json', 'r', encoding='utf-8') as f:
                classes = json.load(f)
            #ClassSelectorView
            class ClassSelectorView(discord.ui.View):
                def __init__(self):
                    super().__init__()

                    class ClassSelector(discord.ui.Select):
                        def __init__(self):
                            
                            
                            options = []

                            for character in classes:
                                options.append(discord.SelectOption(label = character, description = classes[character]['simple']), emoji=core.emoji(classes[character]['emoji']))

                            super().__init__(placeholder='Choose your class', min_values=1, max_values=1, options=options)

                        async def callback(self, interaction: discord.Interaction):
                            
                            select_btn = discord.ui.Button(label = f'Select {self.values[0]} class', style=discord.ButtonStyle.blurple)
                            view = discord.ui.View()
                            view.add_item(select_btn)
                            await interaction.response.send_message(classes[self.values[0]]['description'], ephemeral=True, view=view)

                    self.add_item(ClassSelector())

            embed = discord.Embed(title = "Create WA account", description = 'Selecciona Una Clase', color = bot.color)
            await interaction.response.send_message(embed=embed, view=self.ClassSelectorView(), ephemeral=True)
            await interaction.message.delete()

        
    #Display everything
    await ctx.send('Te damos la bienvenida a WA:Project *Discord Version*, un mundo donde podras vivir una aventura epica!\nPara empezar pulsa al boton **Register** que esta debajo', view=view)

async def delete_profile(bot, ctx, args):pass
async def profile(bot, ctx, args):pass
async def inventory(bot, ctx, args):pass
async def config(bot, ctx, args):
    await ctx.send(f'Welcome {ctx.author.mention} to the account configuration page')