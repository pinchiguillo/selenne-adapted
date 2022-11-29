from asyncio.log import logger
import Selenne
import discord
from discord.ext import commands

import requests

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Fun'
    extension.version = '1.0'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = True
    extension.help.general_display = f'`{bot.main_prefix}help Fun` para obtener mas informacion'
    extension.help.specific_display = {
        f'{bot.main_prefix}image <type>': 'Envia una imagen aleatoria del tipo especificado',
        f'{bot.main_prefix}emilia': 'Envia una obra de arte',
        f'{bot.main_prefix}rem': '...',
        f'{bot.main_prefix}jojos': 'Envia una jojo pose',
        f'{bot.main_prefix}waifu': 'Envia una imagen de una waifu aleatoria',
        f'{bot.main_prefix}silver': 'Obras de arte'
    }
    extension.help.emoji = '🎉'

    #? Databases
    extension.database.storage_type = 'json'
    extension.database.path = 'db/system/startup.json'


    #? Commands
    extension.cogs = [ImageLib]


    #! DO NOT TOUCH
    #? Check Compatibility
    await extension.check_compatibility()
    await extension.load_cogs()
    await extension.load_views()
    await extension.add_help()
    await extension.loaded()
async def teardown(bot):
    await extension.remove_help()
    await extension.unloaded()

#! Extension Code

#? Sample
class ImageLib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
        self._nfw = ['neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe']
        global logger
        logger = self.bot.log

    def get_url(group, type='sfw'):
        try: return requests.get(f'https://api.waifu.pics/{type}/{group}').json()['url']
        except: logger.error('Failed to get url: {}'.format(type=type))

    @commands.command(aliases = ['img', 'i'])
    async def image(self, ctx, args = None):
        if args not in self._nfw:
            s = '\n- '.join(self._nfw)
            s = '- ' + s
            await ctx.send(embed=discord.Embed(title = 'Selenne ImageLib', description=s, colour=self.bot.color))
            return
        res = requests.get(f'https://api.waifu.pics/sfw/{args}')
        url = res.json()['url']
        embed = discord.Embed(colour=self.bot.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command() #! NOT BUILD
    async def emilia(self, ctx, args = None):
        await ctx.send('I always knew that you were the chosen one')

    @commands.command() #! NOT BUILD
    async def rem(self, ctx, args = None):
        await ctx.send('Did you mean Emilia?')

    @commands.command() #! NOT BUILD
    async def jojos(self, ctx, args = None):
        await ctx.send('Este comando estara disponible cuando me termine JoJos')

    @commands.command() 
    async def waifu(self, ctx, args = None):
        res = requests.get('https://api.waifu.pics/sfw/waifu')
        url = res.json()['url']
        embed = discord.Embed()
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases = ['nani', 'nani?', 'WHAT', 'WTF', 'wtf']) #! NOT BUILD
    async def what(self, ctx, args = None):
        await ctx.send('Wtf Bro')

    @commands.command() #! NOT BUILD
    async def fbi(self, ctx, args = None):
        await ctx.send('FBI digame?')

    @commands.command(aliases = ['whitehair']) #! NOT BUILD
    async def silver(self, ctx, args = None):
        await ctx.send('I see a man of culture')

class InteractionLib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
    
    @commands.command()
    async def pat(self, ctx, user:discord.Member):pass

    @commands.command()
    async def kiss(self, ctx, user:discord.Member):pass

    @commands.command()
    async def poke(self, ctx, user:discord.Member):pass

    @commands.command()
    async def kick(self, ctx, user:discord.Member):pass

    @commands.command()
    async def kill(self, ctx, user:discord.Member):pass

    @commands.command()
    async def slap(self, ctx, user:discord.Member):pass

    @commands.command()
    async def bite(self, ctx, user:discord.Member):pass

    @commands.command()
    async def handhold(self, ctx, user:discord.Member):pass

    @commands.command()
    async def highfive(self, ctx, user:discord.Member):pass


#! USING https://waifu.pics/docs API