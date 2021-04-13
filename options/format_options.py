
# youtube-dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors':[{
        'key':'FFmpegExtractAudio',
        'preferredcodec': 'mp3'
    }],
    'preferredquality': '192',
    'quiet': True,
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': False,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

# ffmpeg
ffmpeg_options = {
    'before_options': "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn'
}

    # -stream_type a -i nullsrc -analyzeduration 0.01 -probesize 0.01 -nocache 1 -c:v libx264
    # FFMPEG executable sometimes gets corrupt packets from the webhost, which causes it to terminate: 
    # the next line continues the song if this happens
    