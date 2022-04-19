import discord
from discord.ext import commands

import json
import asyncio

async def setup(b):
    global bot
    bot = b


    bot.add_command(tl)

version = 'MyTierList: 1.0'
ename = 'MyTierList'

db_path = 'db/mytierlist.json'

@commands.command()
async def tl(ctx, mode = 'help', *, name = None):
    help = '''```s.tl lista [lista] => Muestra una determinada lista o si [lista] esta vacio muestra el nombre de todas las listas que has creado
s.tl create [name] => Crea una lista. Desupues siguiendo el modelo mostrado el siguiente mensaje que mandes generara la lista
s.tl delete [name] => Elimina una lista
s.tl version => Muestra la version de MyTierList que se esta utilizando

(En futuras versiones se habilitara para poder ver listas de otros usuarios)
```'''
    
    if mode == 'list':
        if not name:#Open DB
            with open(db_path, 'r') as f:
                db = json.load(f)

            #Per User DB
            user_db = db[str(ctx.author.id)]
            user_db_keys = list(user_db.keys())

            #Display
            d = '**, **'.join([str(item) for item in user_db_keys])
            d = '**' + d + '**'
            embed = discord.Embed(title = 'Your Tierlsits', description = d, color = 0xfe2a9b)
            await ctx.send(embed=embed)
        else:
            with open(db_path, 'r') as f:
                db = json.load(f)
            try:
                user_db = db[str(ctx.author.id)]
                user_db_keys = list(user_db.keys())
                if not user_db_keys:
                    return
            except:
                await ctx.send('You dont have any TierLists')
            try:
                tierlist = user_db[name]
            except:
                print(f'There is no list named {name}')

            tierlist_keys = list(tierlist.keys())

            des = ''
            #Display            
            for rank in tierlist_keys:
                rk = tierlist[rank]
                com = w = '**, **'.join([str(item) for item in rk])
                com = '**' + rank + '** : *' + com + '*\n\n'
                des += com

            embed = discord.Embed(title = f'**Tierlist:** {name}', description = des, color = 0xfe2a9b)
            await ctx.send(embed=embed)

    elif mode == 'create':
        teemplate = '''```S+: Anime1, Anime2 , ...
S: Anime1, Anime2, ...
A: Anime1, Anime2, ...
B: Anime1, Anime2, ...
C: Anime1, Anime2, ...
F: Anime1, Anime2, ...```
        '''
        #Comprobar si existe la lista
        with open(db_path, 'r') as f:
            db = json.load(f)
        
        try:
            db[str(ctx.author.id)]
        except KeyError:
            db[str(ctx.author.id)] = {}

        try:
            db[str(ctx.author.id)][name]
            print(f'You alrready have a list named **{name}**')
            return
        except KeyError:
            pass
        
        #Esperar contenido
        await ctx.send(f'The next message will create a tierlist, use this teemplate in order to create your tierlist{teemplate}')
        
        #Esperar Respuesta
        def check(m):
             return m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send('Has tardado demasiado en mandar el mensaje')

        print('S1')
        #Save Table
        args = reply.content
        args = args.split('\n')
        tierlist =  {}
        tierlist['S+'] = args[0].removeprefix('S+: ').split(', ')
        tierlist['S'] = args[1].removeprefix('S: ').split(', ')
        tierlist['A'] = args[2].removeprefix('A: ').split(', ')
        tierlist['B'] = args[3].removeprefix('B: ').split(', ')
        tierlist['C'] = args[4].removeprefix('C: ').split(', ')
        tierlist['F'] = args[5].removeprefix('F: ').split(', ')

        db[str(ctx.author.id)][name] = tierlist

        with open(db_path, 'w') as f:
            json.dump(db, f, indent=5)
        
        await ctx.send(f'Se ha creado con exito **{name}**')

    elif mode == 'delete' or mode == 'del':
        #Comprobar si existe la lista
        with open(db_path, 'r') as f:
            db = json.load(f)

        try:
            db[str(ctx.author.id)][name]
        except KeyError:
            print(f'You dont have a tierlist named **{name}**')
            return
        
        #Eliminar y guardar tabla actualizada
        del db[str(ctx.author.id)][name]
        with open(db_path, 'w') as f:
            json.dump(db, f, indent=5)
        await ctx.send(f'The Tierlist has been deleted {name}')
        
    elif mode == 'version' or mode == 'v':
        await ctx.send(f'Current Version: **{version}**')
    else:
        await ctx.send(f'Wrong Syntax: **{help}**')

