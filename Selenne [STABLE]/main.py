#Selenne Stable Version
#By DCS Network

import discord
from discord.ext import commands
import json

#Internal
import dcs.bot
import config

class Selenne(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX), #https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.when_mentioned_or
            description = config.version,
            activity = discord.Game(name = config.activity),
            status = config.status,
            intents=intents
            )

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = Selenne()
bot.remove_command('help')

#Cogs
@bot.event
async def setup_hook():
    import cog.dcs
    await bot.add_cog(cog.dcs.esssentials(bot))

    import cog.addons
    await bot.add_cog(cog.addons.games(bot))
    #await bot.add_cog(cog.addons.music(bot)) #OUTDATED
    import cog.Zuteki
    await bot.add_cog(cog.Zuteki.message(bot))
    import cog.ZenkuBlocks
    await bot.add_cog(cog.ZenkuBlocks.all(bot))

    #import cog.Selenne
    #await bot.add_cog(cog.Selenne.core(bot))    #Unable to Load

    #Reload Buttons
    pass

#Run
bot.run(config.TOCKEN)
