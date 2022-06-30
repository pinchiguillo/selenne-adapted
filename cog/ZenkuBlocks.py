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
            embed.add_field(name="news", value="use ```s.news -help``` for more information", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def news_text(self, ctx, *, body=None):
        if ctx.guild.id == self.ZenkuBlocks:
            bot = self.bot
            channel = bot.get_channel(self.ZenkuBlocks_news_ch)
            await channel.send(body)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def private(self, ctx, auth : discord.Member, body):
        if ctx.guild.id == self.ZenkuBlocks:
            await auth.send(body)

    @commands.command()
    @commands.has_permissions(administrator = True)
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
    @commands.has_permissions(administrator = True)
    async def news(self, ctx, *, args = 'help'):
        if ctx.guild.id == self.ZenkuBlocks:
            channel = self.bot.get_channel(self.ZenkuBlocks_news_ch)
            if '-text' in args:
                msg = args.removeprefix('-text')
                await channel.send(msg)

            elif '-embed' in args:
                await ctx.send('Unconfigured')
            elif '-survey' in args:
                await ctx.send('Unconfigured')
            else:
                h = f'''```s.news -text [text]```\nEnvia un anuncio simple de texto al canal <#{self.ZenkuBlocks_news_ch}>
                \n```s.news -embed [embed args]```\nEnvia un embed al canal <#{self.ZenkuBlocks_news_ch}>
                \n```s.news -survey [text]```\nCrea una encuesta en el canal <#{self.ZenkuBlocks_news_ch}>
                '''

                embed=discord.Embed(title="ZenkuBlocks News Command", description=h, color = 0x0091ff)
                await ctx.reply(embed=embed)

    '''@commands.command()
    #@commands.has_role(root_role)
    async def _news(self, ctx, i1, i2 = '', i3 = ''):
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
'''
