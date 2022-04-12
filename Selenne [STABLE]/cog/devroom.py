import discord
from discord.ext import commands

class testers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dev_id = 913949547514974249

    #Commands
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):
        if ctx.guild.id == self.dev_id:
            #Init vars
            self.skips = 0
            self.keeps = 0
            self.usrs = []
            self.vcusers = len(self.vc.members) - 1
            nusers = int(round(self.vcusers * 0.60, 0))

            embed=discord.Embed(title = "Votacion para saltar Canción", description = f'Users in voice: {self.vcusers}\nUsers to Skip: {nusers}\n\nSkip Song: {self.skips} | Keep Song: {self.keeps}', color = 0x00fa9a)

            skipbtn = discord.ui.Button(label = 'Skip', style=discord.ButtonStyle.blurple)
            keepbtn = discord.ui.Button(label = 'Keep', style=discord.ButtonStyle.blurple)

            #Functions

            async def skipbtn_func(interaction):
                if not interaction.user.id in self.usrs:
                    self.usrs.append(interaction.user.id)
                    self.skips += 1
                    embed=discord.Embed(title = "Votacion para saltar Canción", description = f'Users in voice: {self.vcusers}\nUsers to Skip: {nusers}\n\nSkip Song: {self.skips} | Keep Song: {self.keeps}', color = 0x00fa9a)
                    await interaction.response.edit_message(embed = embed, view = view)
                    if self.skips == self.vcusers:
                        pass

            async def keepbtn_func(interaction):
                if not interaction.user.id in self.usrs:
                    self.usrs.append(interaction.user.id)
                    self.keeps += 1
                    embed=discord.Embed(title = "Votacion para saltar Canción", description = f'Users in voice: {self.vcusers}\nUsers to Skip: {nusers}\n\nSkip Song: {self.skips} | Keep Song: {self.keeps}', color = 0x00fa9a)
                    await interaction.response.edit_message(embed = embed, view = view)

            
            skipbtn.callback = skipbtn_func
            keepbtn.callback = keepbtn_func

            view = discord.ui.View()
            view.add_item(skipbtn)
            view.add_item(keepbtn)
        
            msg = await ctx.send(embed=embed, view = view)
