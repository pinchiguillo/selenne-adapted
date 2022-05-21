from re import A
import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'{version.lower()} loaded')

    bot.add_command(em)

def teardown(bot):
    bot.log.info(f'{version.lower()} unloaded')

version = 'Extensions.Manager: 2.2.2'
ename = 'Extensions Manager'

@commands.command()
async def em(ctx, mode = None, *, args = 'manager'):
    if ctx.author.id in bot.developers:
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
            try:
                #Reload the Extension
                await bot.reload_extension(f'extension.{args}')
                
                #Display Msg
                embed.description = f'**{name}** reloaded'
                await ctx.send(embed=embed)

            except Exception as error:
                embed.description = f'Error while reloading **{name}**\n```{error}```'
                await ctx.send(embed=embed)

        elif mode == 'display':
            ex = list(bot.extensions)
            extensions_list = ''            
            for extension in ex:
                tmp = extension.removeprefix('extension.')
                extensions_list += f'\n- {tmp}'
            
            embed.description = extensions_list
            await ctx.send(embed=embed)

        elif mode == 'load':
            try:
                #Load Extension
                await bot.load_extension(f'extension.{args}')
                
                #Dysplay Msg
                embed.description = f'**{args}** loaded'
                await ctx.send(embed=embed)
            except Exception as error:
                embed.description = f'Error while loading **{args}**\n```{error}```'
                await ctx.send(embed=embed)

        elif mode == 'unload':
            if args == 'manager':
                embed.description = f'***{ename}*** **cant be unloaded**'
                await ctx.send(embed=embed)
                return
            try:
                #Unload Extension
                await bot.unload_extension(f'extension.{args}')

                #Dysplay msg
                embed.description = f'**{args}** unloaded'
                await ctx.send(embed=embed)
            except Exception as error:
                embed.description = f'Error while unloading **{args}**\n```{error}```'
                await ctx.send(embed=embed)

        elif mode == 'help':
            embed.description = help, color = bot.color
            await ctx.send(embed=embed)

        elif mode == 'v' or mode == 'version':
            embed.description = f'Running **{version}**'
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
                embed.description = msg
                await ctx.send(embed=embed)
            else:
                try:
                    await bot.load_extension(f'extension.{args}')
                    with open(f'startup_extensions.cfg', 'a') as f:
                        f.write(f'extension.{args}\n')
                    
                    #Dysplay msg
                    embed.description = f'**{args}** successfully added to startup'
                    await ctx.send(embed=embed)
                    bot.log.info(f'extension.{args} added to startup')
                except Exception as error:
                    embed.description = f'**Unable to load extension**:\n```{error}```\nCheck if the extension is unloaded or if the extension loads via **s.em load**'
                    await ctx.send(embed=embed)
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
                await ctx.send(embed=embed)
                bot.log.info(f'extension.{args} removed from startup')
            else:
                embed.description = f'**{args}** Is not in the startup list'
                await ctx.send(embed=embed)

        else:
            embed.description = f'Wrong Syntax\n```{help}```'
            await ctx.send(embed=embed)
