import Selenne
import discord
from discord.ext import commands

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Help'
    extension.version = '2.2'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = bot.help_path

    #? Slash Commands
    extension.slash_command = False

    #? Commands
    extension.cogs = [Help]


    #! DO NOT TOUCH
    #? Check Compatibility
    await extension.check_compatibility()
    await extension.load_cogs()
    await extension.load_views()
    await extension.add_help()
    await extension.sync()
    extension.config.sync()
    await extension.loaded()
async def teardown(bot):
    await extension.remove_help()
    extension.config.sync()
    await extension.unloaded()

#! Extension Code

#? Sample
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
        global color
        color = bot.color

    class Embed(discord.Embed):
        def __init__(self, data:dict = None):
            super().__init__()
            self.title = 'Help - Selenne'
            self.color = color
            
            self.add_data(data)

        def add_data(self, data):
            if data:
                for key in data.keys():
                    self.add_field(name=key, value=data[key], inline=False)

    @commands.hybrid_command(name="help")
    async def help_command(self, ctx, *, args = None):
        '''Displays all the Selenne help'''
        helpembed = self.Embed()
        mt_env = self.Embed()
        
        #Load Help File
        await extension.load_db()
        data = extension.database.data
        #? For Help menu
        if not args:

            #? Text
            helpembed.description = f'''**Menu de Ayuda Selenne**
Actualmente estan cargadas `{len(data.keys())}` extensiones

Ayuda especifica `{self.bot.main_prefix} help <nombre de la extension>`
{self.bot.nullchar}'''

            for key in data.keys():
                helpembed.add_field(name=key, value = data[key]['general_display'], inline=False)

        #? For Specific Help 
        else:
            helpembed.add_data(await extension.get_help(name=args))
            
        #? Menu
        class HelpMenuView(discord.ui.View):
            def __init__(self, data):
                super().__init__()

                #? Selector Class
                class HelpSelector(discord.ui.Select):
                    def __init__(self):
                            
                        options = []

                        for key in data.keys():
                            options.append(discord.SelectOption(label = key, emoji=data[key]['emoji']))

                        super().__init__(placeholder='Selecciona una extension', min_values=1, max_values=1, options=options)

                        
                    async def callback(self, interaction: discord.Interaction):
                        env = mt_env
                        env.add_data(await extension.get_help(name=self.values[0]))
                        await interaction.response.edit_message(embed=env)
                    
                self.add_item(HelpSelector())


        await ctx.send(embed=helpembed, view=HelpMenuView(data))

    @commands.command()
    async def dhelp(self, ctx, args = None):
        # Check if the author is authorithed
        if ctx.author.id in self.bot.developers:
            if not args:
                self.embed.add_field(name = 'Docs', value = '[CLick on me!](https://discordpy.readthedocs.io/en/stable/)', inline=False)
                self.embed.add_field(name = 'Install', value = 'pip install -U git+https://github.com/Rapptz/discord.py', inline=False)
                self.embed.add_field(name = 'Required Extensions', value = 'discord.py 2.0, youtube_dl, PyNaCl', inline=False)
                self.embed.add_field(name = 'Commands Build-In Checks', value = '[CLick on me!](https://discordpy.readthedocs.io/en/stable/)', inline=False)
                self.embed.add_field(name = 'Mentions', value = 'nickname: `<@​​!{id}>`\nrole: `<@​&{id}>`\nchannel: `<#{id}}`\n`@​everyone`\n`@​here`', inline=False)
                self.embed.add_field(name = 'HyperLiks', value = '''"`[Text To Click](https://www.youtube.com/ \"Hovertext\")`"
    - Needs to be a full url (http/https)
    - Hovertext is optional
    - If sent by a bot/user it needs to be in an embed
    - If sent in a webhook you can hyperlink raw text cuz fuck being consistent amirite discord
    - This only works in the embed description and field value
    If you want to hyperlink a title or set_author, you can use the url kwarg''', inline=False)
                self.embed.add_field(name = 'Text Formats', value = '[CLick on me!](https://wikitechnews.net/una-guia-completa-sobre-el-formato-de-texto-de-discord-tachado-negrita-y-mas/)', inline=False)
                self.embed.add_field(name = 'Custom Emogi', value = '```\[custom emoji]```', inline=False)
                self.embed.add_field(name = 'Snowflake Date', value = '[Creation Date](https://snowsta.mp/)', inline=False)
                self.embed.add_field(name = 'Extra', value = '```exec(\'print Hello World\')\neval(\'1 + 1\')```', inline=False)
        else:
            self.embed.description = 'Only Verifyed Selenne Developers Commands'

        await ctx.send(embed=self.embed)

#! HELP NOT ADDED TO DHELP
'https://www.youtube.com/c/TechWithTim/playlists'
'https://www.upgrad.com/blog/how-to-make-chatbot-in-python/'
'https://www.youtube.com/watch?v=c_gXrw1RoKo'

# https://genshin.dev/
# https://genshinlist.com/developer-api
#! Slash Commands https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f

#! NO CHAR FOR DISCORD NAME: '᲼᲼'

#! ---------------------------------------------------------------- FULL FUNCTION ----------------------------------------------------------------
