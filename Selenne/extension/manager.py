from re import A
from tracemalloc import Traceback
import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'{version.lower()} loaded')

    bot.add_command(em)
    bot.last_load = None

def teardown(bot):
    bot.log.info(f'{version.lower()} unloaded')

version = 'Extensions.Manager: 2.3.3'
ename = 'Extensions Manager'

@commands.command()
async def em(ctx, mode = None, *, args = 'manager'):
    if ctx.author.id in bot.developers:
        if mode in ['reload', 'load', 'unload', 'startup', 'removestartup']: bot.log.info(f'{ctx.author.display_name}({ctx.author.id}) used s.em {mode} {args}')
        embed = embed=discord.Embed(title = 'Extensions Manager', color=bot.color)
        help = '''- reload [extension] => Reloads the whole extension(if no args reloads Extension manager)
- display => Displays all the active extensions
- load [extension] => loads an extension
- unload [extension] => unloads an extension
- version  => displays Extensions Manager Current Version
- v => displays Extensions Manager Current Version
- startup => Adds the extension to the startup list
- removestartup => Removes the extension to the startup list'''
        if mode == 'reload':
            name = args
            if args == 'manager':
                name = 'Extension Manager'
            elif args == 'last' or args == '-l' or args == 'l':
                if bot.last_load:
                    args = bot.last_load
                    name = bot.last_load
                else:
                    embed.description = 'No last load saved'
            try:
                #Reload the Extension
                await bot.reload_extension(f'extension.{args}')
                
                #Display Msg
                embed.description = f'**{name}** reloaded'
                
                bot.last_load = args

            except Exception as error:
                embed.description = f'Error while reloading **{name}**\n```{error}```'
                

        elif mode == 'display':
            ex = list(bot.extensions)
            extensions_list = ''            
            for extension in ex:
                tmp = extension.removeprefix('extension.')
                extensions_list += f'\n- {tmp}'
            
            embed.description = extensions_list
            

        elif mode == 'load':
            try:
                #Load Extension
                await bot.load_extension(f'extension.{args}')
                
                #Dysplay Msg
                embed.description = f'**{args}** loaded'
                
                bot.last_load = args
            except Exception as error:
                embed.description = f'Error while loading **{args}**\n```{error}```'
                

        elif mode == 'unload':
            if args == 'manager':
                embed.description = f'***{ename}*** **cant be unloaded**'
                
                return
            try:
                #Unload Extension
                await bot.unload_extension(f'extension.{args}')

                #Dysplay msg
                embed.description = f'**{args}** unloaded'
                
            except Exception as error:
                embed.description = f'Error while unloading **{args}**\n```{error}```'
                

        elif mode == 'help':
            embed.description = help, color = bot.color
            

        elif mode == 'v' or mode == 'version':
            embed.description = f'Running **{version}**'
            

        elif mode == 'startup':
            #Comprobar si exsite la extension
            if args == 'manager':
                with open(f'startup_extensions.cfg', 'r') as f:
                    startup_list = f.readlines()
                msg = ''
                for extension in startup_list:
                    msg += '- ' + extension.removeprefix('extension.')
                
                #Dysplay msg
                embed.description = msg
                
            else:
                try:
                    await bot.load_extension(f'extension.{args}')
                    with open(f'startup_extensions.cfg', 'a') as f:
                        f.write(f'extension.{args}\n')
                    
                    #Dysplay msg
                    embed.description = f'**{args}** successfully added to startup'
                    
                    bot.log.info(f'extension.{args} added to startup')
                except Exception as error:
                    embed.description = f'**Unable to load extension**:\n```{error}```\nCheck if the extension is unloaded or if the extension loads via **s.em load**'
                    
                    bot.log.error(f'while adding extension.{args} to startup ERROR: {error}')

        elif mode == 'removestartup':
            with open(f'startup_extensions.cfg', 'r') as f:
                startup_list = f.readlines()
            if f'extension.{args}\n' in startup_list:
                index = startup_list.index(f'extension.{args}\n')
                startup_list.pop(index)
                w = ' '.join([str(item) for item in startup_list])
                with open(f'startup_extensions.cfg', 'w') as f:
                    f.write(w)
                
                #Dysplay msg
                embed.description = f'**{args}** successfully removed from startup'
                
                bot.log.info(f'extension.{args} removed from startup')
            else:
                embed.description = f'**{args}** Is not in the startup list'
                

        else:
            embed.description = f'Wrong Syntax\n```{help}```'
            

        try:
            await ctx.send(embed=embed)
        except:
            bot.log.critical(f'WHILE GENERATING EMBED:{embed.description}')
            embed.description = 'Error while sending embed, content saved to log'
            await ctx.send(embed=embed)
            
