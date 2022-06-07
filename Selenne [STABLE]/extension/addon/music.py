import discord
from discord.ext import commands

import asyncio
from youtube_dl import YoutubeDL

async def setup(bot):
    
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')
    bot.add_cog(music_upd(bot))

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')

bot_version = 'Selenne 4.8.5'
version = 'Music: 2.7'
ename = 'Music'

class music_upd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            await asyncio.sleep(15)
            await self.vc.disconnect()
    
    async def check_leave(self):
        while self.is_playing:
            await asyncio.sleep(10)
            if self.is_playing == False:
                await self.vc.disconnect()

    #NEW CMD
    @commands.command()
    async def m(self, ctx, mode = None, *args):
        if mode == 'p':
            query = " ".join(args)
            
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                #you need to be connected so that the bot knows where to go
                await ctx.send("Selenne se ha conectado al canal de voz")
            else:
                song = self.search_yt(query)
                if type(song) == type(True):
                    await ctx.send("No se pudo descargar la canción. Formato incorrecto pruebe con otra palabra clave. Esto podría deberse a una lista de reproducción o un formato de transmisión en vivo.")
                else:
                    await ctx.send("Canción añadida a la cola")
                    self.music_queue.append([song, voice_channel])
                    
                    if self.is_playing == False:
                        await self.play_music()
                        await self.check_leave()
        elif mode == 'q':
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += self.music_queue[i][0]['title'] + "\n"

            print(retval)
            if retval != "":
                await ctx.send(f'```{retval}```')
            else:
                await ctx.send("No hay canciones en cola")
        elif mode == 's':
            if self.vc != "" and self.vc:
                self.vc.stop()
                #try to play next in the queue if it exists
                await self.play_music()
        elif mode == 'l':
            if self.is_playing == False:
                await self.vc.disconnect()
        else:
            h = '''```s.m p [youtube link]``` Pone musica desde youtube, tambien pueden ser playlists publicas\n```s.m q```Muestra la cola de canciones\n```s.m s```Salta la cancion que esta sonando\n```s.m l```Selenne abandona el canal de voz de manera forzada'''
            embed = discord.Embed(title = "Selenne Music Help", description = h, color = 0xfe2a9b)
            await ctx.send(embed = embed)
