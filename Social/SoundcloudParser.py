import os
import uuid
import youtube_dl
import requests

ID = str(uuid.uuid4())
path = os.getcwd()


def download_soundcloud(url):
    pass


def audio_soundcloud(url):
    # response = requests.head(url)
    # if '404' in str(response):
    #     print('Закрытый профиль!')
    #     return
    # outtmpl = '/Users/artem/Desktop/bot/MacOs_Downloader-master/%(title)s.%(ext)s'
    # outtmpl = path + '/content' + '/soundcloud/' + '%(title)s.%(ext)s'
    outtmpl = '/var/www/savebot/content/' + '%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': outtmpl
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url)
        title = meta['title']
        file = open('/var/www/savebot/content/' + title + '.mp3', 'rb')
        return file


def thumbnail_soundcloud(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        thumbnail = meta['thumbnail']
        print(thumbnail)
        return thumbnail


def sizes_soundcloud(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            url, download=False)
        link = meta['url']
        content_size = requests.get(link, stream=True)
        file_size = int(content_size.headers['Content-Length'])
        print(file_size)
        return file_size
