import youtube_dl
import os
import uuid
import requests

ID = str(uuid.uuid4())
# url = 'https://rt.pornhub.com/view_video.php?viewkey=ph5ea960ab48e2e'
path = os.getcwd()


def download_pornhub(url):
    filename = ID
    path = '/var/www/savebot/content/'
    outtmpl = '/var/www/savebot/content/{}.%(ext)s'.format(filename)
    ydl_opts = {
        'format': 'best',
        'outtmpl': outtmpl
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        file = open('/var/www/savebot/content/' + filename + '.mp4', 'rb')
        print(file)
        return file


def sizes_pornhub(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            url, download=False)
        link = meta['url']
        content_size = requests.get(link, stream=True)
        file_size = int(content_size.headers['Content-Length'])
        print(file_size)
        return file_size
