from re import A
import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(em)

version = 'ExtensionsManager: 2.2'
ename = 'Extensions Manager'

@commands.command()
async def em(ctx, mode = None, *, args = 'manager'):
    if ctx.author.id in bot.developers:
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
            try:
                #Reload the Extension
                await bot.reload_extension(f'extension.{args}')
                
                #Display Msg
                embed=discord.Embed(title = 'ExtensionsManager', description = f'**{name}** reloaded', color = bot.color)
                await ctx.send(embed=embed)

            except Exception as error:
                embed=discord.Embed(title = 'ExtensionsManager', description = f'Error while reloading **{name}**\n```{error}```', color = bot.color)
                await ctx.send(embed=embed)

        elif mode == 'display':
            ex = list(bot.extensions)
            extensions_list = ''            
            for extension in ex:
                tmp = extension.removeprefix('extension.')
                extensions_list += f'\n- {tmp}'
            
            embed=discord.Embed(title = 'ExtensionsManager', description = extensions_list, color = bot.color)
            await ctx.send(embed=embed)

        elif mode == 'load':
            try:
                #Load Extension
                await bot.load_extension(f'extension.{args}')
                
                #Dysplay Msg
                embed=discord.Embed(title = 'ExtensionsManager', description = f'**{args}** loaded', color = bot.color)
                await ctx.send(embed=embed)
            except Exception as error:
                embed=discord.Embed(title = 'ExtensionsManager', description = f'Error while loading **{args}**\n```{error}```', color = bot.color)
                await ctx.send(embed=embed)

        elif mode == 'unload':
            try:
                #Unload Extension
                await bot.unload_extension(f'extension.{args}')

                #Dysplay msg
                embed=discord.Embed(title = 'ExtensionsManager', description = f'**{args}** unloaded', color = bot.color)
                await ctx.send(embed=embed)
            except Exception as error:
                embed=discord.Embed(title = 'ExtensionsManager', description = f'Error while unloading **{args}**\n```{error}```', color = bot.color)
                await ctx.send(embed=embed)

        elif mode == 'help':
            embed=discord.Embed(title = 'ExtensionsManager', description = help, color = bot.color)
            await ctx.send(embed=embed)

        elif mode == 'v' or mode == 'version':
            embed=discord.Embed(title = 'ExtensionsManager', description = f'Running **{version}**', color = bot.color)
            await ctx.send(embed=embed)

        elif mode == 'startup':
            #Comprobar si exsite la extension
            if args == 'manager':
                with open(f'startup_extensions.cfg', 'r') as f:
                    startup_list = f.readlines()
                msg = ''
                for extension in startup_list:
                    msg += '- ' + extension.removeprefix('extension.')
                
                #Dysplay msg
                embed=discord.Embed(title = 'ExtensionsManager', description = msg, color = bot.color)
                await ctx.send(embed=embed)
            else:
                try:
                    await bot.load_extension(f'extension.{args}')
                    with open(f'startup_extensions.cfg', 'a') as f:
                        f.write(f'extension.{args}\n')
                    
                    #Dysplay msg
                    embed=discord.Embed(title = 'ExtensionsManager', description = f'**{args}** successfully added to startup', color = bot.color)
                    await ctx.send(embed=embed)
                except Exception as error:
                    embed=discord.Embed(title = 'ExtensionsManager', description = f'**Unable to load extension**:\n```{error}```\nCheck if the extension is unloaded or if the extension loads via **s.em load**', color = bot.color)
                    await ctx.send(embed=embed)

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
                embed=discord.Embed(title = 'ExtensionsManager', description = f'**{args}** successfully removed from startup', color = bot.color)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title = 'ExtensionsManager', description = f'**{args}** Is not in the startup list', color = bot.color)
                await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title = 'ExtensionsManager', description = f'Wrong Syntax\n```{help}```', color = bot.color)
            await ctx.send(embed=embed)
