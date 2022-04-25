from re import A
import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(em)

version = 'ExtensionsManager: 2.1'
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
                await bot.reload_extension(f'extension.{args}')
                await ctx.send(f'**{name}** reloaded')

            except Exception as error:
                await ctx.send(f'Error while reloading **{name}**\n```{error}```')
        elif mode == 'display':
            ex = list(bot.extensions)
            extensions_list = ''            
            for extension in ex:
                tmp = extension.removeprefix('extension.')
                extensions_list += f'\n- {tmp}'
            await ctx.send(f'```{extensions_list}```')

        elif mode == 'load':
            try:
                await bot.load_extension(f'extension.{args}')
                await ctx.send(f'**{args}** loaded')
            except Exception as error:
                await ctx.send(f'Error while loading **{args}**\n```{error}```')

        elif mode == 'unload':
            try:
                await bot.unload_extension(f'extension.{args}')
                await ctx.send(f'**{args}** unloaded')
            except Exception as error:
                await ctx.send(f'Error while unloading **{args}**\n```{error}```')

        elif mode == 'help':
            await ctx.send(f'```{help}```')

        elif mode == 'v' or mode == 'version':
            await ctx.send(f'Running **{version}**')

        elif mode == 'startup':
            #Comprobar si exsite la extension
            if args == 'manager':
                with open(f'startup_extensions.cfg', 'r') as f:
                    startup_list = f.readlines()
                msg = ''
                for extension in startup_list:
                    msg += '- ' + extension.removeprefix('extension.')
                await ctx.send(f'```{msg}```')
            else:
                try:
                    await bot.load_extension(f'extension.{args}')
                    with open(f'startup_extensions.cfg', 'a') as f:
                        f.write(f'extension.{args}\n')
                    await ctx.send(f'**{args}** successfully added to startup')
                except Exception as error:
                    await ctx.send(f'**Unable to load extension**:\n```{error}```\nCheck if the extension is unloaded or if the extension loads via **s.em load**')

        elif mode == 'removestartup':
            with open(f'startup_extensions.cfg', 'r') as f:
                startup_list = f.readlines()
            if f'extension.{args}\n' in startup_list:
                index = startup_list.index(f'extension.{args}\n')
                startup_list.pop(index)
                w = ' '.join([str(item) for item in startup_list])
                with open(f'startup_extensions.cfg', 'w') as f:
                    f.write(w)
                await ctx.send(f'**{args}** successfully removed from startup')
            else:
                await ctx.send(f'**{args}** Is not in the startup list')

        else:
            await ctx.send(f'Wrong Syntax\n```{help}```')
