import discord
from discord.ext import commands

import json

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(help)
    #bot.add_command(adminhelp)
    #bot.add_command(developerhelp)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'Help: 1.0.1'
ename = 'Help'

db_path = 'db/system/help.json'

@commands.command()
async def help(ctx, *, args = None):
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)
    
    #Load Help File
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)

    if not args:
        
        for key in db.keys():
            helpembed.add_field(name=key, value = db[key]['general_display'], inline=False)
        
    else:
        if db[args]['specific_display']:
            try:
                for key in db[args]['specific_display'].keys():
                    helpembed.add_field(name=key, value = db[args]['specific_display'][key], inline=False)
            
            except:
                helpembed.description = 'Cant found that extension'
        else: helpembed.description = f'{args} Doesnt have specific help'


    await ctx.send(embed=helpembed)

@commands.command()
async def adminhelp(ctx, args = None):
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)

    await ctx.send(embed=helpembed)

@commands.command()
async def developerhelp(ctx, args = None):
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)

    helpembed.description = 'Only Verifyed Selenne Developers Commands'
    helpembed.add_field(name = '```s.reboot```', value = 'Reboots the whole bot')

    await ctx.send(embed=helpembed)



#Developers help: 
'https://gist.github.com/Painezor/eb2519022cd2c907b56624105f94b190'

#Install dpy2.0
'pip install -U git+https://github.com/Rapptz/discord.py'

#Request: youtube_dl, PyNaCl

#Mentions:
nickname = '<@​​!{id}>'
role = '<@​&{id}>'
channel = '<#{id}}'
'@​everyone'
'@​here'