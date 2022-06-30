import discord
from discord.ext import commands

from discord.ui import Select,View, Button

import random

async def setup(b):
    global bot
    bot = b
    bot.log.warning(f'{__name__} outdated')


    bot.add_command(countdown_date_to_be_reached_in_days_hours_minutes_and_seconds_Made_by_Pinchiguillo)
    bot.add_command(loop)
    bot.add_command(fish)

    

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
