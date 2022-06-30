import discord
from discord.ext import commands

import asyncio

async def setup(b):
    global bot
    bot = b
    bot.log.info(f'{__name__} loaded')

    bot.add_command(online)
    bot.add_command(news_embed)
    bot.add_command(news_text)
    bot.add_command(survey)
    bot.add_command(news)

def teardown(bot):
    bot.log.info(f'{__name__} unloaded')

server_id = 839310820755243018

newsch = 842908439285202944
servercolor = 0x660000

@commands.command()
@commands.has_permissions(administrator=True)
async def online(ctx):
    if ctx.guild.id == server_id:
        channel = bot.get_channel(newsch)
        embed=discord.Embed(title="Server Online", color=discord.Color.green())
        await channel.send(embed=embed)
        await ctx.send('Mensaje enviado a Canal de Anuncios')

#News - Makes a post in News Channel
@commands.command()
@commands.has_permissions(administrator=True)
async def news_embed(ctx, _title, body):
    if ctx.guild.id == server_id:
        try:
            channel = bot.get_channel(newsch)
            embed = discord.Embed(title = _title, description=body, color=discord.Color.blue())
            await channel.send(embed=embed)
        except:
            await ctx.send('The channel is not selected')

@commands.command()
@commands.has_permissions(administrator=True)
async def news_text(ctx, *, body=None):
    if ctx.guild.id == server_id:
        channel = bot.get_channel(newsch)
        await channel.send(body)


@commands.command()
@commands.has_permissions(administrator=True)
async def survey(ctx, mention, body):
    if ctx.guild.id == server_id:
        channel = bot.get_channel(newsch)
        try:
            body =  body + '\n'
            embed=discord.Embed(title="Survey - Encuesta", description=body, color=0xffee00)
            embed.add_field(name="✅", value="Lo quiero!\n", inline=True)
            embed.add_field(name="❎", value="No", inline=True)
            msg = await channel.send(mention,embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❎')
        except:
            await channel.send('Lo escribiste mal!, el formato es z/survey @mention "cuerto", (revisa las comillas)')
    
@commands.command()
@commands.has_permissions(administrator=True)
async def news(ctx, i1, i2 = '', i3 = ''):
    if ctx.guild.id == server_id:
        channel = bot.get_channel(newsch)
        
        if i1 == '-text':
            otp = i2
            preview = True
            await channel.send(otp)

        if i1 == '-embed':
            embed=discord.Embed(title=i2, description=i3, color=discord.Color.blue())
            preview = False
            await channel.send(embed=embed)

        if i1 == '-premade':
            otp = ':loudspeaker: Anuncio |\n\n¡Hey Comunidad ZenkuBlocks!\n\n➤\n' + i2 + '\n\nAtte: ZenkuBlocks Staff.-'
            preview = True
            await channel.send(otp)

        if i1 == '-survey':
            try:
                embed=discord.Embed(title="Survey - Encuesta", description=i3, olor=0xffee00)
                embed.add_field(name="✅", value="Lo quiero!\n", inline=True)
                embed.add_field(name="❎", value="No", inline=True)
                msg = await channel.send(i2, embed=embed)
                await msg.add_reaction('✅')
                await msg.add_reaction('❎')
            except:
                await channel.send('Lo escribiste mal!, el formato es z/news "cuerpo", (revisa las comillas)')
            preview = False

        if i1 == '-help':
            embed=discord.Embed(title="Ayda z/news", description="z/news envia comandos al canal #【📢】anuncios.", color=0x00ccff)
            embed.add_field(name="z/news [msg]", value="envia un mensaje a #【📢】anuncios", inline=False)
            embed.add_field(name="z/news -text [msg]", value="envia un menaje a #【📢】anuncios", inline=False)
            embed.add_field(name="z/news -embed [title] [body]", value="envia un embed a #【📢】anuncios", inline=False)
            embed.add_field(name="z/news -premade [body]", value="envia un usuario utilizando el formato estandar del servidor #【📢】anuncios", inline=False)
            embed.add_field(name="z/news -survey [mention] [msg]", value="crea una encuesta en #【📢】anuncios", inline=False)
            await ctx.send(embed=embed)

        else:
            otp = i1 + i2
            await channel.send(otp)

        if preview == True:
            embed=discord.Embed(title='Message sent to #【📢】anuncios', description=otp, color=discord.Color.blue())
            embed.add_field(name='User', value=ctx.message.author, inline=True)
            await ctx.send(embed=embed)
