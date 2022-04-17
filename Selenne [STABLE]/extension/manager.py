import discord
from discord.ext import commands

async def setup(b):
    global bot
    bot = b
    
    bot.add_command(em)

version = 'ExtensionsManager: 1.1'
ename = 'Extensions Manager'

@commands.command()
async def em(ctx, mode = None, *, args = 'manager'):
    if ctx.author.id == bot.owner:
        help = '- reload [extension] => Reloads the whole extension(if no args reloads Extension manager)\n- display => Displays all the active extensions\n- load [extension] => loads an extension\n- unload [extension] => unloads an extension\n- version  => displays Extensions Manager Current Version\n- v => displays Extensions Manager Current Version'
        if mode == 'reload':
            name = args
            if args == 'manager':
                name = 'Extension Manager'
            try:
                await bot.reload_extension(f'extension.{args}')
                await ctx.send(f'**{name}** reloaded')

            except:
                await ctx.send(f'Error while reloading **{name}**')
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
            except:
                await ctx.send(f'Error while loading **{args}**')

        elif mode == 'unload':
            try:
                await bot.unload_extension(f'extension.{args}')
                await ctx.send(f'**{args}** unloaded')
            except:
                await ctx.send(f'Error while unloading **{args}**')

        elif mode == 'help':
            await ctx.send(f'```{help}```')

        elif mode == 'v' or mode == 'version':
            await ctx.send(f'Running **{version}**')

        else:
            await ctx.send(f'Wrong Syntax\n```{help}```')
