import discord
from discord.ext import commands
import asyncio

async def setup(b):
    global bot
    bot = b

    bot.add_command(embed)

version = 'EmbedGenerator: 0.4'

@commands.command()
async def embed(ctx, args = None):
    
    await ctx.message.delete()

    #Init EmbedClass
    bot.embed = discord.Embed(color=bot.color)
    bot.embed.title = bot.nullchar

    #Create Button
    edit_btn = discord.ui.Button(label = 'Edit', style=discord.ButtonStyle.blurple)
    save_btn = discord.ui.Button(label = 'Save', style=discord.ButtonStyle.green)
    del_btn = discord.ui.Button(label = 'delete', style=discord.ButtonStyle.danger)
    

    async def edit_f(interaction):
        if interaction.user == ctx.author:
            await interaction.response.send_message(view=EditorView(), ephemeral=True)

    async def save_f(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(embed=bot.embed, view = None)
    
    async def del_f(interaction):
        if interaction.user == ctx.author:
            await bot.embed_m.delete()

    edit_btn.callback = edit_f
    save_btn.callback = save_f
    del_btn.callback = del_f

    bot.view = discord.ui.View()
    bot.view.add_item(edit_btn)
    bot.view.add_item(save_btn)
    bot.view.add_item(del_btn)
    bot.embed_m = await ctx.send(embed=bot.embed, view=bot.view)

#Editor
class EditorSelector(discord.ui.Select):
    def __init__(self):
        
        options = []

        options.append(discord.SelectOption(label = 'Title'))
        options.append(discord.SelectOption(label = 'Color'))
        options.append(discord.SelectOption(label = 'Body/Description'))
        
        options.append(discord.SelectOption(label = 'Add Field', description= 'Not in this Extension Version'))
        options.append(discord.SelectOption(label = 'Url'))
        options.append(discord.SelectOption(label = 'Icon'))
        options.append(discord.SelectOption(label = 'Author', description= 'Not in this Extension Version'))
        options.append(discord.SelectOption(label = 'Footer'))

        super().__init__(placeholder='Edit', min_values=1, max_values=1, options=options)

    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Title':
            await interaction.response.send_message('Type a message with the title', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                bot.embed.title = reply.content
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')
            
        elif self.values[0] == 'Color':
            await interaction.response.send_message(view=ColourView(), ephemeral=True)
            
        elif self.values[0] == 'Body/Description':
            await interaction.response.send_message('Type a message with the title', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                bot.embed.description = reply.content
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')
        
        if self.values[0] == 'Url':
            await interaction.response.send_message('Type a message with the URL', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                if not 'http' in reply.content:
                    await interaction.response.send_message('That is not an URL', ephemeral=True)
                bot.embed.url = reply.content
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')

        if self.values[0] == 'Icon':
            await interaction.response.send_message('Type a message with the icon URL', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                if not 'http' in reply.content:
                    await interaction.response.send_message('That is not an URL', ephemeral=True)
                bot.embed.set_thumbnail(url = reply.content)
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')

        if self.values[0] == 'Footer':
            await interaction.response.send_message('Type a message with Author', ephemeral=True)
            def check(m):
                return m.channel == interaction.channel
            
            try:
                reply = await bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
                bot.embed.set_footer(text = reply.content)
                await bot.embed_m.edit(embed=bot.embed)
                
            except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')

        else:
            await interaction.response.send_message('Not in this Extension Version', ephemeral=True)

class EditorView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(EditorSelector())

#Colour
class ColourSelector(discord.ui.Select):
    def __init__(self):
        
        options = []

        for key in bot.colours.keys():
            options.append(discord.SelectOption(label = key.capitalize()))

        options.append(discord.SelectOption(label = 'Hex Code', description = 'Not in this Extension Version'))

        super().__init__(placeholder='Colours', min_values=1, max_values=1, options=options)

    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Hex Code':
            await interaction.response.send_message('Not in this Extension Version', ephemeral=True)
            return
        bot.embed.colour = bot.colours[self.values[0].lower()]
        await bot.embed_m.edit(embed=bot.embed)

class ColourView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(ColourSelector())
