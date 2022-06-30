import discord
from discord.ext import commands

import asyncio

async def setup(b):
    global bot
    bot = b

    bot.add_command(alist)
    bot.add_command(al)

    bot.add_command(ex)


version = 'DCS.Alist: Pre-Alfa'
ename = 'DCS Alist'

alist_db = 'db/dcs/alist'
alist_sh = {
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
        'seen': f'{alist_db}/anime/seen.dat'
    }
}

@commands.command()
async def alist(ctx, typ = None, *, args):
    await alist_main(ctx, typ, args)

@commands.command()
async def al(ctx, typ = None, *, args):
    await alist_main(ctx, typ, args)

async def alist_main(ctx, typ, args):
    if ctx.author .id == bot.owner:
        if not typ:
            await ctx.send('**Specify a type, **Manga/Manhwa** or **Anime**')
        
        if typ.lower() == 'manga' or typ.lower() == 'manhwa':
            db = []
            check = 0

            #Load all db
            for file in alist_sh['manga']:
                with open(alist_sh['manga'][file], 'r', encoding='utf-8') as f:
                    db.append(f.read())
            
            #Search in all db
            for i in range(len(db)):
                if args + '\n' in db[i]:
                    check += 1

            #Save if not in db
            if check >= 1:
                await ctx.send('This **Manga**/**Manhwa** is already saved')
            else:
                with open(alist_sh['manga']['brute'], 'a', encoding='utf') as f:
                    f.write(f'{args}\n')
                await ctx.send('Saved')

        elif typ.lower() == 'anime':
            db = []
            check = 0

            #Load all db
            for file in alist_sh['anime']:
                with open(alist_sh['anime'][file], 'r', encoding='utf-8') as f:
                    db.append(f.read())
            
            #Search in all db
            for i in range(len(db)):
                if args + '\n' in db[i]:
                    check += 1

            #Save if not in db
            if check >= 1:
                await ctx.send('This **Anime** is already saved')
            else:
                with open(alist_sh['anime']['brute'], 'a', encoding='utf') as f:
                    f.write(f'{args}\n')
                await ctx.send('Saved')

        else:
            await ctx.send('Not a valid type, use **Manga/Manhwa** or **Anime**')



    else:
        await ctx.author('**YOU DONT HAVE PERMISSIONS**')

@commands.command()
async def ex(ctx):
    if ctx.author.id in bot.developers:
        prt = None
        try:
            #

            await ctx.send('**Done**')
            if prt:
                await ctx.send(f'```{prt}```')
        except Exception as error:
            await ctx.send(f'```{error}```')
