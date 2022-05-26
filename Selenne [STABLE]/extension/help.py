import discord
from discord.ext import commands
import json

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(help)
    bot.add_command(dhelp)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'Help: 1.0.2'
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
async def dhelp(ctx, args = None):
    helpembed = discord.Embed(title = 'Help - Selenne', color = bot.color)
    if ctx.author.id in bot.developers:
        if not args:
            helpembed.add_field(name = 'Docs', value = '[CLick on me!](https://discordpy.readthedocs.io/en/stable/)', inline=False)
            helpembed.add_field(name = 'Install', value = 'pip install -U git+https://github.com/Rapptz/discord.py', inline=False)
            helpembed.add_field(name = 'Required Extensions', value = 'discord.py 2.0, youtube_dl, PyNaCl', inline=False)
            helpembed.add_field(name = 'Commands Build-In Checks', value = '[CLick on me!](https://discordpy.readthedocs.io/en/stable/)', inline=False)
            helpembed.add_field(name = 'Mentions', value = 'nickname: `<@​​!{id}>`\nrole: `<@​&{id}>`\nchannel: `<#{id}}`\n`@​everyone`\n`@​here`', inline=False)
            helpembed.add_field(name = 'HyperLiks', value = '''"`[Text To Click](https://www.youtube.com/ \"Hovertext\")`"
- Needs to be a full url (http/https)
- Hovertext is optional
- If sent by a bot/user it needs to be in an embed
- If sent in a webhook you can hyperlink raw text cuz fuck being consistent amirite discord
- This only works in the embed description and field value
If you want to hyperlink a title or set_author, you can use the url kwarg''', inline=False)
            helpembed.add_field(name = 'Text Formats', value = '[CLick on me!](https://wikitechnews.net/una-guia-completa-sobre-el-formato-de-texto-de-discord-tachado-negrita-y-mas/)', inline=False)
            helpembed.add_field(name = 'Extra', value = '```exec(\'print Hello World\')\neval(\'1 + 1\')```', inline=False)
    else:
        helpembed.description = 'Only Verifyed Selenne Developers Commands'

    await ctx.send(embed=helpembed)


'https://www.youtube.com/c/TechWithTim/playlists'
'https://www.upgrad.com/blog/how-to-make-chatbot-in-python/'
'https://www.youtube.com/watch?v=c_gXrw1RoKo'