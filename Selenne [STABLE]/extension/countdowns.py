import discord
from discord.ext import commands

import json
from datetime import datetime
import  asyncio

async def setup(b):
    global bot
    bot = b

    bot.add_command(c)

version = 'Countdowns: 1.0'
ename = 'Countdowns'

db_path = 'db/countdowns.json'

@commands.command()
async def c(ctx, mode = 'display', name = None, date = None):
    help = 'UNABLE TO LOAD'
    
    if mode == 'display':
        #Load DB
        with open(db_path, 'r') as f:
            db = json.load(f)
        db_keys = list(db.keys())
        
        
        #First launch
        embed = discord.Embed(title = 'Active Countdowns', color = 0xfe2a9b)
        for date_name in db_keys:
            #Create time object from db
            dt_obj = datetime.strptime(db[date_name], '%d/%m/%Y %H:%M')
            
            #Calculate Diference
            diff = dt_obj - datetime.now()

            #Display
            dplay = str(diff).split('.')[0]
            embed.add_field(name = date_name, value=f'Date: **{db[date_name]}**\nTime Until: **{dplay}**', inline=False)

        msg = await ctx.send(embed=embed)
        
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
                date = date = datetime.strptime(date, '%d/%m/%Y %H:%M')
                db[name] = date.strftime("%d/%m/%Y %H:%M")
                await ctx.send(f'**{name}** is now added to the database')
            
            #Create without hour
            except:
                try:
                    date = date = datetime.strptime(date, '%d/%m/%Y')
                    db[name] = date.strftime("%d/%m/%Y %H:%M")
                    await ctx.send(f'**{name}** is now added to the database')
            
            #Exception
                except:
                    await ctx.send(f'**ERROR** wrong Syntax, use the following one: ```dd/mm/yyyy hh:mm```')

    elif mode == 'modify' or mode == 'edit':    #Not Coded
        await ctx.send('Module Disabled')
    elif mode == 'delete':                      #Not Coded
        await ctx.send('Module Disabled')
    elif mode == 'version' or mode == 'v':
        await ctx.send(f'Current Version: **{version}**')
    else:
        await ctx.send(f'Wrong Syntax: **{help}**')
    

