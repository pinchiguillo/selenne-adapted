import discord
from discord.ext import commands
import asyncio

async def setup(b):
    global bot
    bot = b

    bot.add_command(embed)

version = 'EmbedGenerator: Alfa'



@commands.command()
async def embed(ctx, args = None):
    
    #Init EmbedClass
    bot.embed = discord.Embed(color=bot.color)
    bot.embed.title = 'No Title'

    #Create Button
    edit_btn = discord.ui.Button(label = 'Edit', style=discord.ButtonStyle.blurple)
    save_btn = discord.ui.Button(label = 'Save', style=discord.ButtonStyle.green)
    

    async def edit_f(interaction):
        await interaction.response.send_message(view=ClassSelectorView(), ephemeral=True)

    async def save_f(interaction):
        await interaction.response.edit_message(embed=bot.embed, view = None)

    edit_btn.callback = edit_f
    save_btn.callback = save_f

    bot.view = discord.ui.View()
    bot.view.add_item(edit_btn)
    bot.view.add_item(save_btn)
    bot.embed_m = await ctx.send(embed=bot.embed, view=bot.view)

class ClassSelector(discord.ui.Select):
    def __init__(self):
        
        options = []

        options.append(discord.SelectOption(label = 'Title'))
        options.append(discord.SelectOption(label = 'Color'))
        options.append(discord.SelectOption(label = 'Body/Description'))
        options.append(discord.SelectOption(label = 'Add Field'))

        super().__init__(placeholder='Edit', min_values=1, max_values=1, options=options)

    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Title':
            await interaction.response.send_message('Type a message with the title', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                print('AWAIT MESSAGE')
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                print(reply)
                bot.embed.title = reply.content
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')
            
        elif self.values[0] == 'Color':
            await interaction.response.send_message('Color Editor', ephemeral=True)
            
        elif self.values[0] == 'Body/Description':
            await interaction.response.send_message('Type a message with the title', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                print('AWAIT MESSAGE')
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                print(reply)
                bot.embed.description = reply.content
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')

        elif self.values[0] == 'Add Field':
            await interaction.response.send_message('Field Editor', ephemeral=True)

class ClassSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(ClassSelector())


colours = {"green":0x00ff11,"yellow":0xfaff00,"red":0xff0000,"blue":0x00b3ff,"purple":0x8c00ff}