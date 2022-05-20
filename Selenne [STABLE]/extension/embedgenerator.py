import discord
from discord.ext import commands
import asyncio

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    bot.add_command(embed)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'EmbedGenerator: 1.0'

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

    bot.view = discord.ui.View(timeout = 600)
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

        if self.values[0] == 'Add Field':
            await interaction.response.send_message(view=FieldView(), ephemeral=True)

        else:
            await interaction.response.send_message('Not in this Extension Version', ephemeral=True)

class EditorView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.timeout = 600
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

#Field
class FieldCreator(discord.ui.Select):
    def __init__(self):
        
        options = []

        options.append(discord.SelectOption(label = 'Title', description = 'Must be filled'))
        options.append(discord.SelectOption(label = 'Body', description = 'Must be filled'))

        super().__init__(placeholder='Options', min_values=1, max_values=1, options=options)
        bot.embed_field = {'Title': None, 'Body': None}
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Type the {self.values[0]}', ephemeral=True)
        def check(m):
            return m.channel == interaction.channel
            
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
            await reply.delete()
        except asyncio.TimeoutError:
                await interaction.response.send_message('Has tardado demasiado en mandar el mensaje')

        bot.embed_field[self.values[0]] = reply.content
        
class FieldView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(FieldCreator())

        #Save Button
        save_btn = discord.ui.Button(label = 'Add Field', style=discord.ButtonStyle.blurple)
        
        async def save_f(interaction):
            bot.embed.add_field(name = bot.embed_field['Title'], value = bot.embed_field['Body'], inline=False)
            await bot.embed_m.edit(embed=bot.embed)

        save_btn.callback = save_f
        
        self.add_item(save_btn)
