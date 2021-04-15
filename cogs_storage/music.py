from asyncio.windows_events import NULL
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import asyncio

import options.format_options as format_options
from main import botsays

# help='Play audio in a voice channel'
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue_list = []
        # the discord method .is_playing(), which returns a 
        # boolean value that signifies if any sound is playing 
        # in the voice channel the bot is in, doesn't 
        # always work: I added this manual boolean to recreat the 
        # functionality in a reliable way
        self.playing = False  

    # functions
    async def voice(self, ctx):
        return get(self.bot.voice_clients, guild=ctx.guild)
    
    # searches inputted songs 
    def add_to_queue(self, song_input, queue_placement: int = None):
        with youtube_dl.YoutubeDL(format_options.ytdl_format_options) as ydl:
            url_info = ydl.extract_info(song_input, download=False)

        if 'entries' in url_info: 
            # if 'entries' are found from the info, a playlist was inputted, 
            # loop through all the songs all the songs in the playlist and add to the queue list
            playlist_info = url_info['entries']

            for i, item in enumerate(playlist_info):
                if queue_placement == None:
                    self.queue_list.append((playlist_info[i]["formats"][0]["url"], playlist_info[i]['title']))
                else:
                    self.queue_list.insert(queue_placement,(playlist_info[i]["formats"][0]["url"], playlist_info[i]['title']))
        else: # a url for a single song inputted
            if queue_placement == None:
                self.queue_list.append((url_info["formats"][0]["url"], url_info['title']))
            else:
                self.queue_list.insert(queue_placement,(url_info["formats"][0]["url"], url_info['title']))

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
        voice = await self.voice(ctx)
        
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
        voice = await self.voice(ctx)

        if voice != None:
            await voice.disconnect()
            await botsays(ctx,f"I've left \"{voice.channel}\": keep the party up while I'm gone!")
        else:
            await botsays(ctx,"I don't think I'm currently connected to a voice channel. Use !join to invite me to your party.")

    @commands.command(name='play',pass_context=True, aliases=['p'], help='Adds the given song(s) to queue and starts playing it if no music was previously playing.')
    async def play(self, ctx, *, song_input: str = ''):
        voice = await self.voice(ctx)
        # adding input(s) to queue
        if song_input != '':
            self.add_to_queue(song_input)
        else:
            if self.queue_list != [] and self.playing == False:
                self.resume(ctx)
                return

        if self.queue_list == []:
            await botsays(ctx, 'No songs are queued. After the !play command, paste a url of a song or playlist - or keywords to search from YouTube with - to add the song(s) to queue and start playing!')
            return
        
        
        # is called after a song finishes playing
        def after_song(error):
            if error != None: # error has ocurred with the playing of the song
                print(f'Error while playing song: {error}')

            asyncio.run_coroutine_threadsafe(next_song(), self.bot.loop).result()

        # if there are more songs in queue, call play_song() again
        # if not, call queue() to get the message for an empty queue
        async def next_song():
            discord.FFmpegPCMAudio.cleanup
            voice.cleanup()
            if len(self.queue_list) > 1:
                del self.queue_list[0]
                self.playing = True
                await play_song()
            else:
                if len(self.queue_list)==1:
                    del self.queue_list[0]
                self.playing = False
                await self.queue(ctx)
                
        # plays the first song of the queue, after song finished calls after_song() and passes the error as an argument
        async def play_song():
            voice.play(discord.FFmpegPCMAudio(self.queue_list[0][0], **format_options.ffmpeg_options), after=after_song)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1
            await botsays(ctx, f'**Now playing:** {self.queue_list[0][1]}')
        
        # if bot isn't in a voice channel, join the vc the user is in
        if voice == None:
            if not ctx.message.author.voice:
                await botsays(ctx, "You're not connected to a voice channel. Connect to a channel and try the !play command again!")
                return
            else:
                await self.join(ctx)
                voice = await self.voice(ctx)
        
        # if bot isn't playing music when !play is called, play the first song from the queue
        # if bot is playing music, tell the user the songs they inputted were added to the queue
        if not self.playing:
            self.playing = True
            await play_song()
        else: # if playing music
            await botsays(ctx, 'Song(s) added to queue!')

    @commands.command(name='playtop',pass_context=True, aliases=['pt', 'ptop'], help='Adds the given song **to the top** of the queue.')
    async def playtop(self, ctx, input_url: str):
        if self.queue_list == []:
            await botsays(ctx, 'The queue was empty. I added inputted song(s) to queue and started playing!')
            self.play(input_url)
        else:
            self.add_to_queue(input_url, queue_placement=0)

    # X
    @commands.command(name='playskip',pass_context=True, aliases=['ps', 'pskip', 'playnow', 'pn'], help='Adds the given song **to the top** of the queue and skips the one currently playing.')
    async def playskip(self, ctx, input_url: str):
        pass

    @commands.command(name='pause',pass_context=True, aliases=['pa', 'pau'], help='Pauses the currently playing track.')
    async def pause(self, ctx):
        voice = await self.voice(ctx)

        if self.playing:
            # print('Music paused')
            self.playing = False
            voice.pause()
            await botsays(ctx,'Music paused!')
        else:
            # print('Music not playing, failed to pause')
            await botsays(ctx,'Music is already paused!')

    @commands.command(name='resume',pass_context=True, aliases=['re', 'res', 'continue'], help='Resumes paused music.')
    async def resume(self, ctx):
        voice = await self.voice(ctx)

        if self.queue_list==[]:
            await botsays(ctx,'No music is queued. Try queuing some with the !play command!')
        elif not self.playing:
            # print('Music resumed')
            self.playing = True
            voice.resume()
            await botsays(ctx,'Music resumed!')
        else:
            # print('Music already playing, failed to resume')
            await botsays(ctx,'Music is already playing!')

    @commands.command(name='stop',pass_context=True, aliases=['st', 'sto'], help='Stops playing music and deletes the queue.')
    async def stop(self, ctx):
        voice = await self.voice(ctx)

        if (voice and self.playing) or len(self.queue_list)!=0:
            # print('Music stoppped')
            self.queue_list = []
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
        voice = await self.voice(ctx)

        if len(self.queue_list)==1: # only one song left in queue, the one we're currently playing
            await botsays(ctx, f'**Skipped:** {self.queue_list[0][1]}\n{self.queue()}')
            self.playing = False
            voice.pause()
            voice.stop()
        elif self.playing and len(self.queue_list)>1: # queue has more than the song we're playing in it
            await botsays(ctx, f'**Skipped** {self.queue_list[0][1]}')
            voice.pause()
            voice.stop()
        else:
            await botsays(ctx, 'Cant skip while no songs are playing, add some with the !play command.')

    @commands.command(name='queue',pass_context=True, aliases=['q'], help='Shows the current queue and the currently playing song.')
    async def queue(self, ctx):
        if len(self.queue_list)==0: 
            current_queue = 'There are currently **no songs in queue**, add some with the !play command!'
        else:
            current_queue = f'**Currently playing:** {self.queue_list[0][1]}'
            if len(self.queue_list) == 1:
                current_queue += '\n**No songs waiting in queue!**\nAdd some with the !play command.'
            else:
                current_queue += '\n**Current queue:**'
                for i in range(len(self.queue_list)-1):
                    current_queue += f'\n{i+1}. {self.queue_list[i+1][1]}'
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