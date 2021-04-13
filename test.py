import youtube_dl

with youtube_dl.YoutubeDL() as ydl:
    url_info = ydl.extract_info('https://youtu.be/YQHsXMglC9A')

print(url_info)