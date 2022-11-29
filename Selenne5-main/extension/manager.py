import Selenne
import discord
from discord.ext import commands
from typing import Optional

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Extensions Manager'
    extension.version = '2.5'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = True
    extension.help.general_display = f'Use `{bot.main_prefix}em` to manage the bot current extensions.\n**ONLY BOT STAFF**'
    extension.help.specific_display = {
        f'{bot.main_prefix}em reload <extension>': 'Reloads an extension, if use -last reloads the last extension loaded',
        f'{bot.main_prefix}em display': 'Displays all the active extensions',
        f'{bot.main_prefix}em load <extension>': 'Loads an extension',
        f'{bot.main_prefix}em unload <[extension>': 'Unloads an extension',
        f'{bot.main_prefix}em version': 'Displays Extensions Manager Current Version',
        f'{bot.main_prefix}em startup <extension> -add': 'Adds the extension to the startup list',
        f'{bot.main_prefix}em startup <extension> -remove': 'Removes the extension to the startup list'
        }
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/system/startup.json'

    #? Slash Commands
    extension.slash_command = False

    #? Commands
    extension.cogs = [ExtensionManager]
    extension.views = []


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
    await extension.unloaded()

#! Extension Code

#? Sample
class ExtensionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.hybrid_command(name='extension', aliases = ['em'])
    @discord.app_commands.describe(
        mode = 'The action you want to realice with the extension',
        extension = 'The extension',
        parameters = 'Extra parameters'
    )
    async def extension_command(self, ctx, mode: Optional[str] = 'help', extension: Optional[str] = 'manager', parameters: Optional[str] = ''):
        '''Manage Selenne Extensions'''
        
        #Check if autoriced
        if not ctx.author.id in self.bot.developers:
            await ctx.send('You are not autoriced')
            return

        #Loads Startup Data
        await self.extension.load_db()

        #Pre preate embed
        embed = embed=discord.Embed(title = 'Extensions Manager', color=self.bot.color)

        #? Mode Selector
        match mode.lower():
            case 'reload':
                #Find last extension loaded
                if not extension:
                    extension = 'manager'
                elif extension in ['-last', 'last','-l', 'l']:
                    if self.bot.last_load:
                        extension = self.bot.last_load
                    else: embed.description = 'No last load saved'

                #? Main
                try:
                    await self.bot.reload_extension(f'extension.{extension}')
                    self.bot.last_load = extension
                    embed.description = f'**{extension}** reloaded'
                except Exception as error:
                    embed.description = f'Error while reloading **{extension}**\n```{error}```'
            case 'display':
                extensions = ''            
                for extension in list(self.bot.extensions):
                    tmp = extension.removeprefix('extension.').capitalize()
                    extensions += f'\n- {tmp}'
                
                embed.description = extensions   
            case 'load':
                if '-debug' in parameters:
                    self.bot.log.info(f'{self._version}: \'-debug\' tag located') #!
                    extension = extension.replace('-debug', '').removesuffix(' ')
                    self.bot.log.info(f'{self._version}: \'-debug\' tag replaced') #!
                    await self.bot.load_extension(f'extension.{extension}')
                else:
                    try:
                        #Load Extension
                        await self.bot.load_extension(f'extension.{extension}')
                        
                        #Dysplay Msg
                        embed.description = f'**{extension}** loaded'
                        
                        self.bot.last_load = extension
                    except Exception as error:
                        embed.description = f'Error while loading **{extension}**\n```{error}```'
                        self.bot.log.error(f'Error while loading {extension}: {error}')
            case 'unload':
                if f'extension.{extension}' in self.extension.database.data['extensions']['systematic']:
                    embed.description = f'***{extension}*** **cant be unloaded**'
                else:
                    try:
                        #Unload Extension
                        await self.bot.unload_extension(f'extension.{extension}')

                        #Dysplay msg
                        embed.description = f'**{extension}** unloaded'
                        
                    except Exception as error:
                        embed.description = f'Error while unloading **{extension}**\n```{error}```'
            case 'help': #!
                    embed.description = 'No disponible'
            case 'version' | 'v': embed.description = f'Current version: **{extension.name}: {extension.version}**'
            case 'startup':
                parameters = list(parameters.split(' '))
                match parameters[0].removeprefix('-'):
                    case 'add':
                        #Comprobar si exsite la extension
                        if not f'extension.{extension}' in self.extension.database.data['extensions']['systematic'] and not f'extension.{extension}' in self.extension.database.data['extensions']['normal']:
                            #Intentar cargar extension
                            try:
                                await self.bot.load_extension(f'extension.{extension}')
                                self.extension.database.data['extensions']['normal'].append(f'extension.{extension}')
                                self.extension.unload_db()

                                #Dysplay msg and log
                                embed.description = f'**{extension}** successfully added to startup'
                                self.bot.log.info(f'extension.{extension} added to startup')
                            except Exception as error:
                                embed.description = f'**Unable to load extension**:\n```{error}```\nCheck if the extension is unloaded or if the extension loads via **s.em load**'
                                
                                self.bot.log.error(f'while adding extension.{extension} to startup ERROR: {error}')
                        else: 
                            embed.description = f'{extension} alrready in startup'                  
                    case 'remove':
                        #Comprobar si exsite la extension
                        if f'extension.{extension}' in self.extension.database.data['extensions']['normal']:
                            #Intentar descargar cargar extension
                            try:
                                try:
                                    await self.bot.unload_extension(f'extension.{extension}')
                                except:pass
                                
                                self.extension.database.data['extensions']['normal'].pop(extension.database.data['extensions']['normal'].index(f'extension.{extension}'))
                                self.extension.save_db()

                                #Dysplay msg and log
                                embed.description = f'**{extension}** successfully removed from startup'
                                self.bot.log.info(f'extension.{extension} removed form startup')
                            except Exception as error:
                                embed.description = f'**Unable to remove extension from startup**:\n```{error}```'
                                
                                self.bot.log.error(f'while removing extension.{extension} to startup ERROR: {error}')
                        else: 
                            embed.description = f'{extension} not in startup'
                    case _: embed.description = 'Wrong Syntax'

            case _: 
                embed.description = 'Wrong Syntax, try using `s.help Extensions Manager`'


        #Send embed to discord
        try:
            await ctx.send(embed=embed)
        except:
            self.bot.log.error(f'WHILE GENERATING EMBED:{embed.description}')
            embed.description = 'Error while sending embed, content saved to log'
            await ctx.send(embed=embed)