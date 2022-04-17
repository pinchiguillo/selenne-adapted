#Selenne Stable Version
#By DCS Network

from cog.addons import music_upd
import discord
from discord.ext import commands
import json
import asyncio

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
        self.pid = await self.fetch_user(000000000000000000)
        m = await self.pid.send('Ya vuelvo a estar conectada')
        await asyncio.sleep(5)
        await m.delete()

bot = Selenne()
bot.remove_command('help')

#Universal Vars
bot.owner = config.owner

#SetUp
@bot.event
async def setup_hook():
    import cog.dcs
    await bot.add_cog(cog.dcs.esssentials(bot))

    import cog.addons
    await bot.add_cog(cog.addons.games(bot))
    await bot.add_cog(cog.addons.music_upd(bot))
    import cog.Zuteki
    #await bot.add_cog(cog.Zuteki.message(bot))
    import cog.ZenkuBlocks
    await bot.add_cog(cog.ZenkuBlocks.all(bot))

    import cog.devroom
    await bot.add_cog(cog.devroom.testers(bot))

    import cog.Selenne
    #await bot.add_cog(cog.Selenne.core(bot))


    #NEW GEN
    await bot.load_extension('extension.manager')
    
    await bot.load_extension('extension.Selenne')
    await bot.load_extension('extension.server.zuteki')


    #Reload Buttons
    pass

#Run
bot.run(config.TOCKEN)
