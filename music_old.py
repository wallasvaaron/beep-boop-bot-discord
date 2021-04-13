import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import asyncio

import options.format_options as format_options
from cogs.talking import botsays

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = queue = []
        self.playing = playing = False
    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music: ready')

    # commands
    @commands.command(name='join',pass_context=True, aliases=['summon'], help='Summons the bot to the voice channel you\'re in.')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await botsays(ctx, "You're not connected to a voice channel. Connect, and then try the !join command again!")
            return

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        

        # if the user and the bot  both connected to a channel,
        # bot will move to the user's channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
            await botsays(ctx,f"I've joined \"{channel}\": let's party!")
        else:
            # if bot isn't in a voice channel already,
            # it will connect to the user's channel
            voice = await channel.connect()
            await botsays(ctx,f"I've joined \"{channel}\": let's party!")

    @commands.command(name='leave',pass_context=True, aliases=['dc', 'disconnect', 'dis'], help='Disconnects the bot from the voice channel it is in.')
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice != None:
            await voice.disconnect()
            await botsays(ctx,f"I've left \"{voice.channel}\": keep the party up while I'm gone!")
        else:
            await botsays(ctx,"I don't think I'm currently connected to a voice channel. Use !join to invite me to your party.")

    @commands.command(name='play',pass_context=True, aliases=['p'], help='Adds the given song to queue and resumes music if none was playing.')
    async def play(self, ctx, *, input_url: str):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and not voice.is_playing() and len(self.queue)!= 0:
            voice.resume()
        
        if voice == None:
            if not ctx.message.author.voice:
                await ctx.send("You're not connected to a voice channel. Connect to a channel and try the !play command again!")
                return
            else:
                await self.join(ctx)
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                    
        def add_to_queue(url):
            with youtube_dl.YoutubeDL(format_options.ytdl_format_options) as ydl:
                url_info = ydl.extract_info(url, download=False)

            if 'entries' in url_info:
                playlist_info = url_info['entries']

                for i, item in enumerate(playlist_info):
                    self.queue.append((playlist_info[i]["formats"][0]["url"], playlist_info[i]['title']))
            else:
                self.queue.append((url_info["formats"][0]["url"], url_info['title']))

        def next_song(error):
            discord.FFmpegPCMAudio.cleanup
            if len(self.queue) > 1:
                del self.queue[0]
                fut = asyncio.run_coroutine_threadsafe(play_song(), self.bot.loop)
                fut.result()
            else:
                if len(self.queue)==1:
                    del self.queue[0]
                    fut = asyncio.run_coroutine_threadsafe(self.currentqueue(ctx), self.bot.loop)
                    fut.result()
                self.playing = False
                return

        async def play_song():
            
            voice.play(discord.FFmpegPCMAudio(self.queue[0][0], **format_options.ffmpeg_options), after=next_song)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = .15
            await botsays(ctx,f'**Now playing:** {self.queue[0][1]}')

        if not self.playing:
            add_to_queue(input_url)
            discord.FFmpegPCMAudio.cleanup

            self.playing = True
            await play_song()
        else: # if playing music
            add_to_queue(input_url)
            await botsays(ctx, 'Song(s) added to queue!')

    # X
    @commands.command(name='playtop',pass_context=True, aliases=['pt', 'ptop'], help='Adds the given song **to the top** of the queue.')
    async def playtop(self, ctx, input_url: str):
        pass

    # X
    @commands.command(name='playskip',pass_context=True, aliases=['ps', 'pskip', 'playnow', 'pn'], help='Adds the given song **to the top** of the queue and skips the one currently playing.')
    async def playskip(self, ctx, input_url: str):
        pass

    @commands.command(name='pause',pass_context=True, aliases=['pa', 'pau'], help='Pauses the currently playing track.')
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            # print('Music paused')
            voice.pause()
            await botsays(ctx,'Music paused!')
            return
        else:
            # print('Music not playing, failed to pause')
            await botsays(ctx,'I can\'t pause if music isn\'t playing!')
            return

    @commands.command(name='resume',pass_context=True, aliases=['re', 'res', 'continue'], help='Resumes paused music.')
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if self.queue==[]:
            await botsays(ctx,'No music is queued. Try queuing some with the !play command!')
            return
        elif voice and not voice.is_playing():
            # print('Music resumed')
            voice.resume()
            await botsays(ctx,'Music resumed!')
            return
        else:
            # print('Music already playing, failed to resume')
            await botsays(ctx,'Music already playing!')
            return

    @commands.command(name='stop',pass_context=True, aliases=['st', 'sto'], help='Stops playing music and deletes the queue.')
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if (voice and voice.is_playing()) or len(self.queue)!=0:
            # print('Music stoppped')
            self.queue = []
            self.playing = False
            # print(f'Queue after stop: {len(queue)}')
            voice.pause()
            voice.stop()
            await botsays(ctx,'Music stopped!')
            return
        else:
            # print('Music not playing, failed to stop')
            await botsays(ctx,'I can\'t stop the music if none is playing!')
            return

    @commands.command(name='skip',pass_context=True, aliases=['next', 's', 'forceskip','fskip', 'fs'], help='Skips the currently playing song.')
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if len(self.queue)==1: # only one song left in queue, the one we're currently playing
            # print("Song skipped, no more songs in queue")
            await botsays(ctx, f'**Skipped:** {self.queue[0][1]}\nThere are currently **no songs in queue**, add some with the !play command!')
            self.queue = []
            self.playing = False
            voice.pause()
            voice.stop()
            
        elif voice and voice.is_playing() and len(self.queue)>1: # if
            # print("Song skipped")
            await botsays(ctx, f'**Skipped** {self.queue[0][1]}')
            voice.stop()
        else:
            # print('No music playing, failed to skip')
            await botsays(ctx, 'Cant skip while no songs are playing, add some with the !play command.')

    @commands.command(name='queue',pass_context=True, aliases=['q'], help='Shows the current queue and the currently playing song.')
    async def currentqueue(self, ctx):
        if len(self.queue)==0:
            current_queue = 'There are currently **no songs in queue**, add some with the !play command!'
        else:
            current_queue = f'**Currently playing:** {self.queue[0][1]}'
            if len(self.queue) == 1:
                current_queue += '\n**No songs waiting in queue!**\nAdd some with the !play command.'
            else:
                current_queue += '\n**Current queue:**'
                for i in range(len(self.queue)-1):
                    current_queue += f'\n{i+1}. {self.queue[i+1][1]}'
        await botsays(ctx, current_queue)

    # X
    @commands.command(name='nowplaying',pass_context=True, aliases=['np'], help='Shows what is currently playing.')
    async def nowplaying(self, ctx):
        pass

    # X
    @commands.command(name='move',pass_context=True, aliases=['m', 'mv'], help='Moves the song to a chosen position in queue: if not specified, it\'s moved to the top of the queue.')
    async def move(self, ctx):
        pass

    # X
    @commands.command(name='shuffle',pass_context=True, aliases=['random'], help='Shuffles the entire queue.')
    async def shuffle(self, ctx):
        pass

    # X
    @commands.command(name='clear',pass_context=True, aliases=['cl'], help='Clears the queue. If !clear <user>, clears only the songs added by that user.')
    async def clear(self, ctx):
        pass

    # X
    @commands.command(name='removedupes',pass_context=True, aliases=['rmd', 'rd', 'drm'], help='Removes duplicates from the queue.')
    async def removedupes(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Music(bot))