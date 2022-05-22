import discord
from discord.ext import commands

import json
import datetime
import  asyncio

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    global extension_help
    
    extension_help = {
        'general_display': '*s.countdown* or *s.c*',
        'specific_display': {
            's.c': 'Displays the Countdowns Table',
            's.c display': 'Displays the Countdowns Table',
            's.c add': 'Adds a new Countdown (**ALFA**)',
            's.c modify': 'Modifyes a Countdown (**ALFA**)',
            's.c delete': 'Deletes a Countdown (**ALFA**)',
            's.c version': 'Displays Countdown Version'
            }
        }

    add_help()

    #ADD CMD
    bot.add_command(c)
    bot.add_command(countdown)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

version = 'Countdowns: 1.3.1'
ename = 'Countdowns'

db_path = 'db/countdowns.json'

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)


@commands.command()
async def c(ctx, mode = 'display', name = None, *, date = None):
    await main_cmd(ctx=ctx, mode=mode, name=name, date=date)

@commands.command()
async def countdown(ctx, mode = 'display', name = None, *, date = None):
    await main_cmd(ctx=ctx, mode=mode, name=name, date=date)


#General Function
async def main_cmd(ctx, mode = 'display', name = None, *, date = None):
    help = '''**s.c** or **s.countdown**
```
s.c => Displays the countdowns
s.c display =>  Displays the countdowns
s.c add => Creates a new Countcown
s.c delete => Deletes a Countdown
s.c version => Shows the Countdowns version
```
'''
    
    if mode == 'display':
        #Load DB
        with open(db_path, 'r') as f:
            db = json.load(f)
        db_keys = list(db.keys())
        
        #Function
        def dp(time = None):
            #First launch
            embed = discord.Embed(title = 'Active Countdowns', color = 0xfe2a9b)
            for date_name in db_keys:
                #Create time object from db
                dt_obj = datetime.datetime.strptime(db[date_name], '%d/%m/%Y %H:%M')
                
                #Calculate Diference
                diff = dt_obj - datetime.datetime.now()

                #Display
                zero = datetime.timedelta(seconds=0)
                if diff < zero:
                    dplay = '**Passed**'
                else:
                    dplay = str(diff).split('.')[0]
                embed.add_field(name = date_name, value=f'Date: **{db[date_name]}**\nTime Until: **{dplay}**', inline=False)
            
            if time:
                embed.set_footer(text = 'Refresh Time: ' + str(60 - time) + 's')
            return embed

        #Dispolay
        msg = await ctx.send(embed=dp())
        for i in range(60):
            await msg.edit(embed=dp(i))
            await asyncio.sleep(1)
        
        await msg.edit(embed=dp())

    elif mode == 'add':
        #Load DB
        with open(db_path, 'r') as f:
            db = json.load(f)
        
        #Check if in DB
        try:
            db[name]
            await ctx.send('This Date Name is already in use. Please try with an other name')
        except KeyError:
            #Create with hour
            try:
                date = date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
                db[name] = date.strftime("%d/%m/%Y %H:%M")
                await ctx.send(f'**{name}** is now added to the database')
            
            #Create without hour
            except:
                try:
                    date = date = datetime.datetime.strptime(date, '%d/%m/%Y')
                    db[name] = date.strftime("%d/%m/%Y %H:%M")

                    await ctx.send(f'**{name}** is now added to the database')
            
            #Exception
                except:
                    await ctx.send(f'**ERROR** wrong Syntax, use the following one: ```dd/mm/yyyy hh:mm```')

            with open(db_path, 'w') as f:
                json.dump(db, f, indent=5)

    elif mode == 'modify' or mode == 'edit':    #Not Coded
        await ctx.send('Module Disabled')
    elif mode == 'delete' or mode == 'del':
        if ctx.author.id == bot.owner:
            with open(db_path, 'r') as f:
                db = json.load(f)
            try:
                db[name]
                del db[name]
                with open(db_path, 'w') as f:
                    json.dump(db, f, indent=5)
                await ctx.send(f'**{name}** Deleted')
            except KeyError:
                await ctx.send(f'**{name}** is not in the database')
        else:
            await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS')

    elif mode == 'version' or mode == 'v':
        await ctx.send(f'Current Version: **{version}**')

    else:
        await ctx.send(f'Wrong Syntax: **{help}**')
