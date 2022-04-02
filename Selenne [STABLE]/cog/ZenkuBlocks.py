import discord
from discord.ext import commands

class all(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.ZenkuBlocks = 839310820755243018
        self.root_role = 839313179401519154
        self.ZenkuBlocks_bot_ch = 875523911138312202
        self.ZenkuBlocks_news_ch = 842908439285202944
        self.ZenkuBlocks_purge_ch = 887773936320913469

    @commands.Cog
    #@commands.has_role(root_role)
    async def ophelp(self, ctx):
        if ctx.guild.id == self.ZenkuBlocks:
            embed=discord.Embed(title="Ayuda Admins", description="Listado de comandos que requieren administrador", color=0x00ccff)
            embed.add_field(name="news", value="use z/news -help", inline=False)
            embed.add_field(name="reboot", value="reinicia el bot", inline=False)
            embed.add_field(name="proximamente", value="proximamente", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    #@commands.has_role(root_role)
    async def online(self, ctx):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_news_ch)
            embed=discord.Embed(title="Server Online", color=discord.Color.green())
            await channel.send(embed=embed)
            await ctx.send('Mensaje enviado a Canal de Anuncios')

    @commands.command()
    #@commands.has_role(root_role)
    async def news_embed(self, ctx, _title, body):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            try:
                channel = bot.get_channel(self.ZenkuBlocks_news_ch)
                embed = discord.Embed(title = _title, description=body, color=discord.Color.blue())
                await channel.send(embed=embed)
            except:
                await ctx.send('The channel is not selected')

    @commands.command()
    #@commands.has_role(root_role)
    async def news_text(self, ctx, *, body=None):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_news_ch)
            await channel.send(body)

    @commands.command()
    #@commands.has_role(root_role)
    async def private(self, ctx, auth : discord.Member, body):
        if ctx.guild.id == self.ZenkuBlocks:
            await auth.send(body)

    @commands.command()
    #@commands.has_role(root_role)
    async def survey(self, ctx, mention, body):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_news_ch)
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
    async def bug(self, ctx, body):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_purge_ch)
            author = ctx.message.author
            embed = discord.Embed(title = 'BUG REPORT', description=body, color=discord.Color.red())
            embed.add_field(name = 'Author', value = author, inline = False)
            await channel.send(embed=embed)
            await ctx.send('Gracias por el reporte!')

    @commands.command()
    async def suggest(self, ctx, body):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_purge_ch)
            author = ctx.message.author
            embed = discord.Embed(title = 'Suggest', description=body, color=discord.Color.green())
            embed.add_field(name = 'Author', value = author, inline = False)
            await channel.send(embed=embed)
            await ctx.send('Gracias por la sugerencia!')

    @commands.command()
    #@commands.has_role(root_role)
    async def news(self, ctx, i1, i2 = '', i3 = ''):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_news_ch)
            
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

            
            #otp
            if preview == True:
                embed=discord.Embed(title='Message sent to #【📢】anuncios', description=otp, color=discord.Color.blue())
                embed.add_field(name='User', value=ctx.message.author, inline=True)
                await ctx.send(embed=embed)
