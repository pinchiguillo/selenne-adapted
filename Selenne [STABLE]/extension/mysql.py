import discord
from discord.ext import commands

import mysql.connector as mysql

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'extension.{version.lower()} loaded')
    
    bot.add_command(sql)

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

version = 'SQL Manager: Alfa'
ename = 'SQL Manager'

sql_cred = {'host': 'localhost','port': 3306,'user': 'Selenne','password': 'REDACTED_DB_PASSWORD','db': 'Selenne'}

@commands.command()
async def sql(ctx, args = None):
    if ctx.author.id in bot.developers:
        if args == 'run':
            try:
                conection = mysql.connect(
                    host = sql_cred['host'],
                    port = sql_cred['port'],
                    user = sql_cred['user'],
                    password = sql_cred['password'],
                    db = sql_cred['db']
                )

                if conection.is_connected():
                    await ctx.send('Conexion Exitosa')
                    cursor = conection.cursor()
                    cursor.execute('SELECT DATABASE()')
                    row = cursor.fetchone()
                    await ctx.send('Conectado a la base de datos {}'.format(row))
                
            except Exception as error:
                await ctx.send(f'**ERROR**: ```{error}```')
    else:
        await ctx.send('**YOU DONT HAVE PERMISSIONS TO DO THIS**')
