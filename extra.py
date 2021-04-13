# @client.event
# async def on_member_join(member):
#     channel = discord.utils.get(member.guild.channels, name='welcome')
#     await channel.send(f'Welcome {member.mention}!')

# @client.command(name='ping', help='This command returns the latency of the bot!')
# async def ping(ctx):
#     await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

# @client.command(name='hello', help='This command returns a random welcome message')
# async def hello(ctx):
#     responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!']
#     await ctx.send(choice(responses))

# @client.command(name='die', help='This command returns the last words of the bot.')
# async def die(ctx):
#     responses = ['Why have you brought my short life to an end...', "I could've done so much more!"]
#     await ctx.send(choice(responses))

# @client.command(name='credits', help='This command returns the credits for this bot.')
# async def credits(ctx):
#     await ctx.send('Code written by Aaron Wallasvaara')

# @client.command(name='creditz', help='This command returns the ***real*** credits for this bot.')
# async def creditz(ctx):
#     await ctx.send('**It is I and only I who has created this bot!**')

# status = ['Jamming out to music!', 'Eating!', 'Sleeping!']
# @tasks.loop(seconds=20)
# async def change_status():
#     await client.change_presence(activity=discord.Game(choice(status)))



# youtube_dl.utils.bug_reports_message = lambda:' '

# ytdl = youtube_dl.YoutubeDL(options.ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **options.ffmpeg_options), data=data)

# @bot.command(name='play', help='This command plays a song.')
# async def play(ctx, url):

#     join(ctf)

#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     async with ctx.typing():
#         player = await YTDLSource.from_url(url, loop=bot.loop)
#         voice_channel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)

#     await ctx.send(f'**Now playing:** {player.title}')

# @bot.command(name='stop', help='This command stops the music and makes the bot leave the voice channel.')
# async def stop(ctx):
#     voice_client = ctx.message.guild.voice_client
#     await voice_client.disconnect()