import os
import requests
import uuid
import youtube_dl

ID = str(uuid.uuid4())
path = os.getcwd()


def download_twitter(url):
    try:
        outtmpl = '/var/www/savebot/content/' + '%(id)s.%(ext)s'
        ydl_opts = {
            'format': 'best',
            'outtmpl': outtmpl,
            # 'nooverwrites': True,

        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            meta = ydl.extract_info(url, download=False)
            id = meta['id']
            file = open('/var/www/savebot/content/' + id + '.mp4', 'rb')
            return file
    except:
        return 'confusing_error'


def thumbnail_twitter(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        thumbnail = meta['thumbnail']
        print(thumbnail)
        return thumbnail


def sizes_twitter(url):
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                url, download=False)
            link = meta['url']
            req_file_size = requests.get(link, stream=True)
            file_size = int(req_file_size.headers['Content-Length'])
            return file_size
    except:
        return 'confusing_error'
