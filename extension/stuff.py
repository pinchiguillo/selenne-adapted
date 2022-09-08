import discord
from discord.ext import commands

from discord.ui import Select,View, Button

import random
import json

async def setup(b):
    global bot
    bot = b
    bot.log.warning(f'{__name__} outdated')


    bot.add_command(countdown_date_to_be_reached_in_days_hours_minutes_and_seconds_Made_by_Pinchiguillo)
    bot.add_command(loop)
    bot.add_command(fish)
    bot.add_command(fechas)
    bot.add_command(encuesta)
    bot.add_command(bitcheck)
    bot.add_command(pisa83)
    bot.add_listener(on_member_join)


def teardown(bot):
    bot.log.info(f'{__name__} unloaded')

@commands.command()
async def sao(ctx):
    embed=discord.Embed(title = 'Sword Art Online', description = 'Datos temporales de Sword Art Online (Aincrad)', color=0x00d5ff)
    embed.add_field(name = 'Fecha de Inicio', value = '06/11/2022 13:00', inline=True)
    embed.add_field(name = 'Tiemo Restante', value = '[error:data.cant.load]', inline=True)
    embed.add_field(name = '■', value = '■', inline=False)
    embed.add_field(name = 'Fecha de Finalización', value = '07/1/2024 14:55', inline=True)
    embed.add_field(name = 'Tiempo Restante', value = '[error:data.cant.load]', inline=True)
    await ctx.send(embed=embed)

@commands.command()
async def countdown_date_to_be_reached_in_days_hours_minutes_and_seconds_Made_by_Pinchiguillo(ctx):
    await ctx.send('Prueba a usar s.c :)')

@commands.command()
async def loop(ctx, times:int, msg:str):
    if ctx.author.id in bot.developers:
        for i in range(times):
            await ctx.send(msg)
    else:
        await ctx.send('You are not allowed to use this command')

#@loop.error()

#!#####################            Fish DEV 
def gen_view():
        view = discord.ui.View()
        for i in range(5):
            for j in range(5):
                if random.random() <= bot.winrate: winner = True
                else: winner = False
                view.add_item(FishButton(i,j, winner))
        return view

@commands.command()
async def fish(ctx):

    #Global Vars
    bot.marklist = []
    bot.fish_embed = discord.Embed(title = f'Start Fishing', color = bot.color)
    bot.basket = dict()
    bot.game = True

    #Configuracion
    bot.fishing_attempts = 7
    bot.winrate = 0.4
    bot.wildlife = ['Fish', 'Carp', 'Boot', 'Rooster', 'Turbot', 'Sole', 'Bass']

    bot.fish_embed.description = f'Fishing Attemps remaining: {bot.fishing_attempts}'
    await ctx.send(embed=bot.fish_embed, view=gen_view())

class FishButton(discord.ui.Button): #class FishButton(discord.ui.Button['FishArea']):
    def __init__(self, x: int, y: int, winner:bool):
        super().__init__(style=discord.ButtonStyle.secondary, label=bot.nullchar, row=y)
        self.x = x
        self.y = y
        self.winner = winner

        self.style = discord.ButtonStyle.primary

        self.row = y

        if [self.x,self.y] in bot.marklist:
            self.disabled = True


        if not bot.game: self.disabled = True

    async def callback(self, interaction: discord.Interaction):

        bot.marklist.append([self.x, self.y])
        
        bot.fishing_attempts -= 1
        bot.fish_embed.description = f'Fishing Attemps remaining: {bot.fishing_attempts}'

        if self.winner:
            bot.fish_embed.description += f'\n\nYou caught a fish!\n\n'
            
            #Add to basket
            try:
                catch = random.choice(bot.wildlife)
                null = bot.basket[catch]

                bot.basket[catch] +=1
            except KeyError:
                bot.basket[catch] = 1
        else:
            bot.fish_embed.description += f'\n\nLooks like that\'s not a fish\n\n'

        #Basket
        basket = ''
        for item in bot.basket.keys():
            basket += f'{item} x {bot.basket[item]}\n'

        bot.fish_embed.description += f'Basket:\n{basket}'


        
        #END GAME FUNCTION
        if bot.fishing_attempts <= 0:
            bot.game = False
            bot.fish_embed.title= 'You are done fishing!'

        await interaction.response.edit_message(embed = bot.fish_embed, view=gen_view())

@commands.command()
async def fechas(ctx):
    with open('db/fechas.txt', 'r', encoding='utf-8') as f:
        fechas = f.readlines()

    view = View()
    embed = discord.Embed(title='Fechas EVAU', color=bot.color)
    class btn(discord.ui.Button):
        def __init__(self, name):
            super().__init__(style=discord.ButtonStyle.secondary, label=name)
            self.style = discord.ButtonStyle.primary
            with open('db/fechas.txt', 'r', encoding='utf-8') as f:
                self.fechas = f.readlines()
            self.hide = True
            


        async def callback(self, interaction: discord.Interaction):

            if self.hide:
                self.fecha = self.fechas[random.randint(0, len(fechas))] 
                embed.description = self.fecha.split('.')[0]
                self.hide = False
            else:
                embed.description = self.fecha
                self.hide = True

            await interaction.response.edit_message(embed = embed)

    view.add_item(btn('Siguiente'))

    await ctx.send(embed=embed, view=view)

@commands.command()
async def bitcheck(ctx, bits:int):
    _bits = 0
    while True:
        cap = 2**_bits < bits
        print(f'Bits: {_bits}: {cap}')
        if not cap:
            await ctx.send(f'Your number uses `{_bits + 1}` bytes of memory')
            return
        
        _bits += 1

@commands.command()
async def encuesta(ctx):
    #! Dev Room: 913949547514974249
    #! Zuteki: 959659781960917002
    
    #? Cargar datos servidor
    try:
        with open(f'db/surveys/{ctx.guild.id}.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.send('This server does not have active surveys')
        return
    
    #? Create default embed
    desc = data['embed']['desciption']
    embed = discord.Embed(title = data['embed']['title'], description = f'{desc}\n{bot.nullchar}', color = bot.color)

    def add_fields(embed, fields):
        _embed = embed
        for option in fields.keys():
            _embed.add_field(name=option, value = f'Votos: `{fields[option]}`')
        return _embed

    _embed = add_fields(embed, data['options'])

    #? Create view
    class VoteView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.timeout = 1296000

            #? Adds buttons
            #for option in data['options'].keys():
            
            class Vote_Button(discord.ui.Button): #class FishButton(discord.ui.Button['FishArea']):
                def __init__(self, option):
                    super().__init__(style=discord.ButtonStyle.success, label=option)
                    self.option = option

                        
                async def callback(self, interaction: discord.Interaction):
                    with open(f'db/surveys/{ctx.guild.id}.json', 'r', encoding='utf8') as f:
                        data = json.load(f)
                    if interaction.user.id in data['users']:
                        await interaction.response.send_message('Ya has votado!', ephemeral=True)

                    else:
                        data['options'][self.option] += 1
                        data['users'].append(interaction.user.id)

                        with open(f'db/surveys/{ctx.guild.id}.json', 'w', encoding='utf8') as f:
                            json.dump(data, f, indent=5)
                        
                        desc = data['embed']['desciption']
                        embed = discord.Embed(title = data['embed']['title'], description = f'{desc}\n{bot.nullchar}', color = bot.color)

                        _embed = add_fields(embed, data['options'])

                    await interaction.response.edit_message(embed = _embed)

                    

            for option in data['options'].keys():
                self.add_item(Vote_Button(option=option))
    
    
        

    await ctx.send(embed=_embed, view=VoteView())

@commands.command()
async def pisa83(ctx):
    embed=discord.Embed(title="Bon Dia", description="Ha entrado usted en nuestro servidore pase bona tarde", color=0xdf942a)
    embed.set_image(url='https://c.tenor.com/bcsxIQ9v_AIAAAAC/darkness-konosuba.gif')
    await ctx.send(embed=embed)

@commands.Cog.listener()
async def on_member_join(member):
    if not member.guild.id == 890329598565429299: return

    embed=discord.Embed(title = 'Bon Dia', description = f'{member.mention} ha entrado usted en nuestro servidore pase bona tarde', color=0xdf942a)
    embed.set_image(url='https://c.tenor.com/bcsxIQ9v_AIAAAAC/darkness-konosuba.gif')
    await member.guild.get_channel(1012502968593023006).send(embed=embed)
    await member.add_roles(discord.utils.get(member.guild.roles, name="Campesino"), reason='Default Role')