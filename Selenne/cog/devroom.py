from socket import timeout
import discord
from discord.ext import commands

class testers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dev_id = 913949547514974249

    #Commands
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):  ###guild.voice_client.channel.members
        if ctx.guild.id == self.dev_id:
            if ctx.author.id in ctx.guild.voice_client.channel.members.id:
                #Init vars
                self.skips = 0
                self.keeps = 0
                self.usrs = []
                self.vcusers = len(ctx.guild.voice_client.channel.members) - 1
                self.nusers = int(round(self.vcusers * 0.60, 0))

                embed=discord.Embed(title = "Votacion para saltar Canción", description = f'Users in voice: {self.vcusers}\nUsers to Skip: {self.nusers}\n\nSkip Song: {self.skips} | Keep Song: {self.keeps}', color = 0x00fa9a)

                skipbtn = discord.ui.Button(label = 'Skip', style=discord.ButtonStyle.blurple)
                keepbtn = discord.ui.Button(label = 'Keep', style=discord.ButtonStyle.blurple)

                #Functions

                async def skipbtn_func(interaction):
                    if not interaction.user.id in self.usrs:
                        self.usrs.append(interaction.user.id)
                        self.skips += 1
                        embed=discord.Embed(title = "Votacion para saltar Canción", description = f'Users in voice: {self.vcusers}\nUsers to Skip: {self.nusers}\n\nSkip Song: {self.skips} | Keep Song: {self.keeps}', color = 0x00fa9a)
                        await interaction.response.edit_message(embed = embed, view = view)
                        if self.skips == self.nusers:
                            print('Skip Song')
                            await interaction.response.edit_message(embed = embed, view = None)
                        if self.skips + self.keeps == self.vcusers:
                            print('END SURVEY')
                            await interaction.response.edit_message(embed = embed, view = None)

                async def keepbtn_func(interaction):
                    if not interaction.user.id in self.usrs:
                        self.usrs.append(interaction.user.id)
                        self.keeps += 1
                        embed=discord.Embed(title = "Votacion para saltar Canción", description = f'Users in voice: {self.vcusers}\nUsers to Skip: {self.nusers}\n\nSkip Song: {self.skips} | Keep Song: {self.keeps}', color = 0x00fa9a)
                        await interaction.response.edit_message(embed = embed, view = view)
                        if self.skips + self.keeps == self.vcusers:
                            print('END SURVEY')
                            await interaction.response.edit_message(embed = embed, view = None)

                #Link function to btn
                skipbtn.callback = skipbtn_func
                keepbtn.callback = keepbtn_func

                #Display btn
                view = discord.ui.View()
                view.add_item(skipbtn)
                view.add_item(keepbtn)
            
                msg = await ctx.send(embed=embed, view = view)
