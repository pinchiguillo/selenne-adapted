import discord
from discord.ext import commands

import asyncio

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')

    bot.add_command(picklib)

    bot.add_listener(on_message)
    bot.add_listener(on_member_join)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'DCS: Alfa'
ename = 'DCS API'

server_id = 866477454468841472
channel_id = 927376122281357322
picklib_db = 'db/dcs/picklib/'

alist_db = 'db/dcs/alist'
alist = {
    'manga':{
        'brute': f'{alist_db}/brute/manga.dat',
        'want': f'{alist_db}/manga/want.dat',
        'active': f'{alist_db}/manga/active.dat',
        'reading': f'{alist_db}/manga/reading.dat',
        'finished': f'{alist_db}/manga/finished.dat'
    },
    'anime':{
        'brute': f'{alist_db}/brute/anime.dat',
        'want': f'{alist_db}/anime/want.dat',
        'season': f'{alist_db}/anime/season.dat',
        'active': f'{alist_db}/anime/active.dat',
        'seen': f'{alist_db}/amime/seen.dat'
    }
}

@commands.command()
async def ping(ctx):
    ctx.send('Pong')

@commands.Cog.listener()
async def on_member_join(member):
    if not member.guild.id == server_id:
        return
    
    msg = await member.send('Bienvenido a DCS, por motivos de seguridad necesito que me digas el codigo de acceso. Tienes 10 minutos')
    def check(m):
        return not m.guild and m.author == member
    try:
        reply = await bot.wait_for('message', timeout=600.0, check=check)
    except:
        pass
    finally:
        if reply.content:
            await member.send('Bienvenido!')
            loggedRole = discord.utils.get(member.guild.roles, name="Member")
            await member.add_roles(loggedRole, reason='Logged')

@commands.Cog.listener()
async def on_message(message):
    if message.author.bot:
        return
    if message.guild.id == server_id and message.channel.id == channel_id:
        if not 'https:' in message.content:
            msg = await message.reply('Not a Link')
            await asyncio.sleep(5)
            await message.delete()
            await msg.delete()
            return
        
        with open(picklib_db + 'brute.dat', 'r', encoding='utf-8') as f:
            if f'{message.content}\n' in f.readlines():
                msg = await message.reply('Link Alrready in db')
                await asyncio.sleep(5)
                await message.delete()
                await msg.delete()
                return
            
        with open(picklib_db + 'brute.dat', 'a', encoding='utf-8') as f:
            f.write(f'{message.content}\n')
        await asyncio.sleep(1)
        await message.delete()

@commands.command()
async def picklib(ctx, mode = 'help', *, args = None):
    if not ctx.author.id == bot.owner:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')
        return
    
    keywords = {'instagram': 'https://www.instagram.com','pixiv': 'https://www.pixiv.net', 'pin': 'https://pin.it/'}

    if mode == 'short':
    #Load List
        with open(picklib_db + 'brute.dat', 'r', encoding='utf-8') as f:
            full_list = f.readlines()
        
        
        #Shortlists
        instagram_list = []
        pixiv_list = []
        pin_list = []
        ex_list = []

        for url in full_list:
            if keywords['instagram'] in url:
                st = url.find("https:")
                url = url[st:]
                instagram_list.append(url)
            if keywords['pixiv'] in url:
                st = url.find("https:")
                url = url[st:]
                pixiv_list.append(url)
            if keywords['pin'] in url:
                st = url.find("https:")
                url = url[st:]
                pin_list.append(url)
        
        with open(picklib_db + 'instagram.dat', 'a', encoding='utf-8') as f:
            f.write(''.join([str(item) for item in instagram_list]))
        with open(picklib_db + 'pixiv.dat', 'a', encoding='utf-8') as f:
            f.write(''.join([str(item) for item in pixiv_list]))
        with open(picklib_db + 'pin.dat', 'a', encoding='utf-8') as f:
            f.write(''.join([str(item) for item in pin_list]))
        
        with open(picklib_db + 'brute.dat', 'w', encoding='utf-8') as f:
            f.write('')
        with open(picklib_db + 'log.dat', 'a', encoding='utf-8') as f:
            f.write(''.join([str(item) for item in full_list]))


        with open(picklib_db + 'picklib.log'):
            pass

        await ctx.send('DB Shorted')

    if mode == 'download':
        pass 

    else:
        await ctx.send('Wrong Syntax')

@commands.command()
async def alist(ctx, typ = None, *, args):
    if ctx.author .id == bot.owner:
        if not typ:
            await ctx.send('**Specify a type, **Manga/Manhwa** or **Anime**')
        
        if typ.lower() == 'manga' or typ.lower() == 'manhwa':
            pass
        elif typ.lower() == 'anime':
            pass
        else:
            await ctx.send('Not a valid type, use **Manga/Manhwa** or **Anime**')

        await ctx.send(f'```{args}```')


    else:
        await ctx.author('**YOU DONT HAVE PERMISSIONS**')
