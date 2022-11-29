from hashlib import new
import Selenne
import discord
from discord.ext import commands

import os
import asyncio
import random

#? Configuration
async def setup(bot):
    global extension
    extension = Selenne.Extension(bot)
    
    #? Basic Info
    extension.name = 'Selenne Life'
    extension.version = 'Alfa'
    extension.bot_version = 'Selenne 5.3'
    extension.link_version()
    
    #? Help config
    extension.help.enabled = False
    extension.help.general_display = ''
    extension.help.specific_display = {}
    #extension.help.emoji = ''

    #? Databases
    extension.database.storage_type = 'json_dir'
    extension.database.path = 'db/slib'
    extension.database.start()


    #? Commands
    extension.cogs = [SL_Manager, Character, Economy]


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

class SL_Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
    
    #! COMMANDS
    @commands.command(aliases = ['slsetup'])
    @commands.has_permissions(administrator=True)
    async def sl_setup(self, ctx):
        embed = discord.Embed(title='Selenne Life', description = '**Cargando...**', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        cfg_display = f'`{self.bot.main_prefix}slconfig`'

        if not extension.database.create_table(ctx.guild.id):
            embed.description = f'***Selenne Life*** ya esta configurado.\n\nUsa {cfg_display} para configurar ***Selenne Life***'
            await msg.edit(embed=embed)
            return
        #? Graphical Interface
        embed.description = 'Bienvenido al menu de configuracion de ***Selenne Life***\n\n**Cargando...**'
        await msg.edit(embed=embed)
        await asyncio.sleep(random.randint(3,5))
        
        #? Moneda
        default_coin = '~~***S***~~'
        embed.description = f'Lo primero es crear una moneda, por defecto es el ***Selenium*** ({default_coin}).\n\nEscribe a continuacion la moneda quie quieres que se use en ***{ctx.guild}***\n\nSi quieres que siga siendo {default_coin} escribe `Selenium`'
        await msg.edit(embed=embed)

        #* Espera de mensaje
        def check(m):
            return m.channel == ctx.channel
        try:
            reply = await self.bot.wait_for('message', timeout=60.0, check=check)
            await reply.delete()
        except asyncio.TimeoutError:
            embed.description = f'Has tardado demasiado en mandar el mensaje y se ha cancelado el setup\n\n Usa otra vez `{self.bot.main_prefix}.sl_setup` para configurar ***Selenne Life***'
            os.rmdir(os.path.join(extension.database.path, str(ctx.guild.id)))
            await msg.edit(embed=embed)
            return
        
        if reply.content == 'Selenium': coin_icon = default_coin
        else: coin_icon = reply.content
        embed.description = f'La moneda de {ctx.guild} es {coin_icon}\n\n**Cargando...**'
        await msg.edit(embed=embed)
        await asyncio.sleep(random.randint(2,4))

        #? White/Black List and List
        embed.description = f'***Selenne Life*** puede restringir la ganancia de recursos a ciertos canales, esto se puede modificar mas adelante en {cfg_display}\n\nActualmente estan disponibles dos medios de control:\n**Whitelist**: solo en los canales selecionados se ganaran recursos\n**BlackList**: en todos los canales menos en los seleccionados se ganaran recursos\n\nSi quiere que este disponible pulsa en **Sin Filtro**'
        class FilterView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.timeout = 60

                #? Selector Class
                class FilterSelector(discord.ui.Select):
                    def __init__(self):

                        options = {'Whitelist': '🏳️', 'Blacklist': '🏴', 'Sin Filtro': '❌'}

                        _options = []
                        for option in options.keys():
                            _options.append(discord.SelectOption(label = option, emoji=options[option]))

                        super().__init__(placeholder='Selecciona un filtro', min_values=1, max_values=1, options=_options)
                    
                    async def callback(self, interaction: discord.Interaction):
                        global ans
                        ans = self.values[0]
                        self.view.stop()

                self.add_item(FilterSelector())
        view = FilterView()
        await msg.edit(embed=embed, view=view)
        await view.wait()
        if not ans:
            embed.description = f'Has tardado demasiado en elegir filtro y se ha cancelado el setup\n\n Usa otra vez `{self.bot.main_prefix}.sl_setup` para configurar ***Selenne Life***'
            os.rmdir(os.path.join(extension.database.path, str(ctx.guild.id)))
            await msg.edit(embed=embed, view=None)
            return
        embed.description = f'**{ans}** selected\n\n**Cargando...**'
        await msg.edit(embed=embed, view=None)

        channels = list()
        if ans != 'Sin Filtro':
            embed.description = f'Envia los canales que quieres que formen parte de la **{ans}** mencionandolos y separados por un espacio.' 
            await msg.edit(embed=embed)

            #* Get Answere
            try:
                reply = await self.bot.wait_for('message', timeout=60.0, check=check)
                await reply.delete()
            except asyncio.TimeoutError:
                embed.description = f'Has tardado demasiado en mandar el mensaje y se ha cancelado el setup\n\n Usa otra vez `{self.bot.main_prefix}.sl_setup` para configurar ***Selenne Life***'
                os.rmdir(os.path.join(extension.database.path, str(ctx.guild.id)))
                await msg.edit(embed=embed)
                return
            
            channels = reply.content.split(' ')
            _channels = list()
            
            m = 'Se han añadido los canales '
            for channel in channels:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                _channels.append(channel)
                m += f'{channel.mention}, '

            m = m.removesuffix(',')
            m += f'a la **{ans}**\n\n**Cargando...**'
            embed.description = m
            await msg.edit(embed=embed)
            channels = _channels
            await asyncio.sleep(random.randint(1,5))

        #? Item Packs
        db_output = extension.database.get('items')
        packages = db_output['packages']
        package_count = len(packages)
        embed.description = f'En ***Selenne Life*** existe un sistema de items los cuales el usuario puede ir recolectando ya sea comerciando con otros usuarios del mismo servidor, como comprandolos en la tienda, o mandando mensajes.\nCon el fin de dotar a los servidores de la mayor personalizacion se puede elegir entre `{package_count}` packs de items.\n\nEl pack de items escogido puede cambiarse desde {cfg_display} pero esto **solo afecta a la generacion de items** si un usuario tiene un item ya no disponible este podra ser comerciado'
        class ItemPacksView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.timeout = 120

                #? Selector Class
                class PackageSelector(discord.ui.Select):
                    def __init__(self):


                        options = []
                        for package in packages:
                            options.append(discord.SelectOption(label = package['name'], emoji=package['emoji']))

                        super().__init__(placeholder='Selecciona un Pack de items', min_values=1, max_values=1, options=options)
                    
                    async def callback(self, interaction: discord.Interaction):
                        global package
                        package = self.values[0]
                        self.view.stop()

                self.add_item(PackageSelector())  
        view = ItemPacksView()
        await msg.edit(embed=embed,view=view)
        await view.wait()
        embed.description = f'Has seleccionado ***{package}***\n\n**Cargando...**'
        await msg.edit(embed=embed,view=None)
        await asyncio.sleep(random.randint(5,7))

        #? Saving Data
        extension.database.create(f'{ctx.guild.id}/config', {
            'coin_icon': coin_icon,
            'whitelist/blacklist': ans,
            'channel_list': [channel.id for channel in channels],
            'item_pack': package,
            'notifications': False,
            'inmigration': False
            })
        extension.database.create_table(f'{ctx.guild.id}/bank')

        #? Setup complete
        embed.description = f'Ya has terminado de configurar ***Selenne Life***!\n\n Para realizar cualquier cambio de configuracion usar {cfg_display}'
        await msg.edit(embed=embed)

    @commands.command(aliases = ['slcfg'])
    @commands.has_permissions(administrator=True)
    async def slconfig(self, ctx):
        embed = discord.Embed(title='Selenne Life', description = '**Cargando...**', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        menus = {'Menu Principal': '🌍', 'Economia': '💵', 'Restricciones': '⛔', 'Items': '📦', 'Notificaciones': '📩', 'Inmigracion': '🏳️'}
        class MenusSelectorView(discord.ui.View):
            def __init__(self, active_menu=None):
                super().__init__()
                self.timeout = 120

                #? Selector Class
                class MenusSelector(discord.ui.Select):
                    def __init__(self, active_menu=None):
                        options = []
                        for menu in menus.keys():
                            if menu == active_menu: options.append(discord.SelectOption(label = menu, emoji=menus[menu], default=True))
                            else: options.append(discord.SelectOption(label = menu, emoji=menus[menu]))
                            

                        super().__init__(placeholder='Selecciona un menu', min_values=1, max_values=1, options=options)

                    async def callback(self, interaction: discord.Interaction):
                        global active_menu
                        active_menu = self.values[0]
                        print()
                        embed.description = '**Cargando...**'
                        await interaction.response.edit_message(embed=embed, view=None)
                        self.view.stop()
                self.add_item(MenusSelector(active_menu))
                class ExitBtn(discord.ui.Button):
                    def __init__(self):
                        super().__init__(style=discord.ButtonStyle.danger, label='Exit')
                    
                    async def callback(self, interaction: discord.Interaction):
                        global active_menu
                        active_menu = None
                        embed.description = '**Cargando...**'
                        await interaction.response.edit_message(embed=embed, view=None)
                        self.view.stop()
                if active_menu == 'Menu Principal': self.add_item(ExitBtn())

        #? Obtener database y si no terminar comando
        data = extension.database.get(f'{ctx.guild.id}/config')
        if not data:
            embed.description = f'***Selenne Life*** no esta configurado en este servidor, usa `{self.bot.main_prefix}slsetup`'
            await msg.edit(embed=embed)
            return
        
        #? Procesamiento de la database

        ch = 'No Data'
        embed.description =  f'''Bienvenido al menu de configuracon de ***Selenne Life***

**Configuracion actual**
**Moneda**: {data['coin_icon']}
**Restricciones**: `{data['whitelist/blacklist']}`
**Pack de Items**: *{data['item_pack']}*
**Notificaciones**: `{data['notifications']}`
**Inmigracion**: `{data['inmigration']}`
'''
        view = MenusSelectorView('Menu Principal')
        await msg.edit(embed=embed, view=view)
        await view.wait()
        while True:
            if not active_menu: break

            match active_menu:
                case 'Menu Principal':
                    data = extension.database.get(f'{ctx.guild.id}/config')
                    embed.description =  f'''Bienvenido al menu de configuracon de ***Selenne Life***

**Configuracion actual**
**Moneda**: {data['coin_icon']}
**Restricciones**: `{data['whitelist/blacklist']}`
**Pack de Items**: *{data['item_pack']}*
**Notificaciones**: `{data['notifications']}`
**Inmigracion**: `{data['inmigration']}`
'''
        
                case 'Economia': embed.description = 'Economy Menu'
                case 'Restricciones': embed.description = 'Restriction Menu'
                case 'Items': embed.description = 'Items Menu'
                case 'Notificaciones': embed.description = 'Notifications Menu'
                case 'Inmigracion': embed.description = '**Inmigracion no esta disponible actualmente**'

            #? Resend the view
            view = MenusSelectorView(active_menu)
            await msg.edit(embed=embed, view=view)
            await view.wait()    
        embed.description = 'Se ha cerrado el menu de configuracion de ***Selenne Life***'
        await msg.edit(embed=embed, view=None, delete_after=5)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        try: open(f'{extension.database.path}/{message.guild.id}/config.json') 
        except: return
        data = extension.database.get(f'{message.guild.id}/{message.author.id}')
        if not data:
            extension.database.create(f'{message.guild.id}/{message.author.id}', {
                'name': message.author.display_name,
                'level': 0,
                'xp': [0, 100],
                'money': 0,
                'inventory': {},
                'guild': None,
                'friends': [],
                'skills': {
                    'fishing': 0,
                    'minning': 0,
                    'hunting': 0,
                    'crafting': 0
                }
            })
            extension.database.create(f'{message.guild.id}/bank/{message.author.id}', {
                'money': 0,
                'log': []
            })
            
            return
        if data['xp'][0] >= data['xp'][1]: 
            new_xp = [data['xp'][0] - data['xp'][1], int(round(((data['level'] + 1)**1.25) * 100, 0))]
            extension.database.edit(f'{message.guild.id}/{message.author.id}', {'xp': new_xp})
            extension.database.edit(f'{message.guild.id}/{message.author.id}', {'level': data['level'] + 1})
            nl = data['level'] + 1
            await message.channel.send(f'Felicidades {message.author.mention} ahora eres **Nivel {nl}**', delete_after=5)

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
        self.embed = discord.Embed(title='Selenne Life', description = '**Cargando...**', color=self.bot.color)
    
    @commands.command()
    async def sl(self, ctx):
        embed = discord.Embed(title='Selenne Life', description = '**Cargando...**', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        data = extension.database.get(f'{ctx.guild.id}/{ctx.author.id}')
        guild_cfg = extension.database.get(f'{ctx.guild.id}/config')
        if not data:
            embed.description = 'Selenne Life no esta habilitado en este servidor'
            await msg.edit(embed=embed)
            return
        embed.description = f'''Bienvenido **{ctx.author.display_name}**
**Nivel de cuenta**: {data['level']} ({data['xp'][0]}/{data['xp'][1]})
**Dinero**: {data['money']} {guild_cfg['coin_icon']}
**Gremio**: {data['guild']}

**Habilidades**
{self.bot.nullchar}*Pesca nivel {data['skills']['fishing']}*
{self.bot.nullchar}*Mineria nivel {data['skills']['minning']}*
{self.bot.nullchar}*Caza nivel {data['skills']['hunting']}*
{self.bot.nullchar}*Crafteo nivel {data['skills']['crafting']}*

**Actualmente la configuracion de usuario esta deshabilitada**
'''
        await msg.edit(embed=embed, delete_after=60)

    @commands.Cog.listener()
    async def on_message(self, message):
        data = extension.database.get(f'{message.guild.id}/{message.author.id}')
        guild = extension.database.get(f'{message.guild.id}/config')
        if not data: return
        val = random.randint(1,5)
        #self.bot.log.info(f'{message.author.display_name} ha ganado {val} xp')
        extension.database.edit(f'{message.guild.id}/{message.author.id}', {'xp': [data['xp'][0] + val, data['xp'][1]]})
        if guild['notifications']: await message.channel.send(f'has ganado {val} experiencia!', delete_after=5)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension
        self.nodata = '**No Data**'

    @commands.command(aliases= ['eco', 'economy'])
    async def sleconomy(self, ctx):
        embed = discord.Embed(title='Selenne Life', description = '**Cargando...**', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        #? Lista de menus
        menus = {
            'Pagina Principal': '⛩️',
            'Ranking': '🥇',
            'Banco': '🏦',
            'Transferencia': '💱',
            'Registro': '📔'
        }
        main_menu = 'Pagina Principal'

        #.? View Object
        class MenusSelectorView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.timeout = 120

                #? Selector Class
                class MenusSelector(discord.ui.Select):
                    def __init__(self):
                        options = []
                        for menu in menus.keys():
                            if menu == active_menu: options.append(discord.SelectOption(label = menu, emoji=menus[menu], default=True))
                            else: options.append(discord.SelectOption(label = menu, emoji=menus[menu]))
                            

                        super().__init__(placeholder='Selecciona un menu', min_values=1, max_values=1, options=options)

                    async def callback(self, interaction: discord.Interaction):
                        global view_otp
                        view_otp = self.values[0]
                        embed.description = '**Cargando...**'
                        await interaction.response.edit_message(embed=embed, view=None)
                        self.view.stop()
                self.add_item(MenusSelector())
                class ExitBtn(discord.ui.Button):
                    def __init__(self):
                        super().__init__(style=discord.ButtonStyle.danger, label='Exit')
                    
                    async def callback(self, interaction: discord.Interaction):
                        global view_otp
                        view_otp = None
                        embed.description = '**Cargando...**'
                        await interaction.response.edit_message(embed=embed, view=None)
                        self.view.stop()
                if active_menu == 'Pagina Principal': self.add_item(ExitBtn())

        #? Bucle de interaccion
        active_menu = main_menu
        view = MenusSelectorView()
        while True:
            #? Different Menus Code
            match active_menu:
                case 'Pagina Principal' : embed.description = '''Bienvenido al menu de gestion economico
**Algo**
'''
                case 'Ranking' : embed.description = f'''Actualmente estas en el puesto {self.nodata} en {ctx.guild.id}
El ranking internacional no se encuentra disponible

**Los mas ricos de** ***{ctx.guild}***
**1** *{self.nodata}*
**2** *{self.nodata}*
**3** *{self.nodata}*
**4** *{self.nodata}*
**5** *{self.nodata}*
'''
                case 'Banco' : 
                    embed.description = f'''Bienvenido al ***Banco de {ctx.guild}***
**Saldo**: {self.nodata} {self.nodata}

**Ultimas Transacciones:**
{self.nodata}
'''             
                case 'Transferencia' : embed.description = 'Actualmente las transferencias no estan disponibles'
                case 'Registro' : embed.description = '**No disponible**'

            #? Output Code DO NOT TOUCH
            active_menu = None 
            await msg.edit(embed=embed, view=view)
            await view.wait()
            active_menu = view_otp
            view = MenusSelectorView()
            if not active_menu: break
            
        #? END
        embed.description = 'Se ha cerrado el menu'
        await msg.edit(embed=embed, view=None, delete_after=5)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        data = extension.database.get(f'{message.guild.id}/{message.author.id}')
        guild = extension.database.get(f'{message.guild.id}/config')
        if not data: return
        if random.random() < 0.2:
            val = round(1 + random.random(), 2)
            #self.bot.log.info(f'{message.author.display_name} ha ganado {val} dinero')
            extension.database.edit(f'{message.guild.id}/{message.author.id}', {'money': data['money'] + val})
            if guild['notifications']: await message.channel.send(f'has ganado {val} dinero!', delete_after=5)

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        data = extension.database.get(f'{message.guild.id}/{message.author.id}')
        guild = extension.database.get(f'{message.guild.id}/config')
        if not data: return

class Activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

class Commerce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        data = extension.database.get(f'{message.guild.id}/{message.author.id}')
        guild = extension.database.get(f'{message.guild.id}/config')
        if not data: return

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension = extension

    @commands.command()
    async def extension(self, ctx, args = None):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        data = extension.database.get(f'{message.guild.id}/{message.author.id}')
        guild = extension.database.get(f'{message.guild.id}/config')
        if not data: return
