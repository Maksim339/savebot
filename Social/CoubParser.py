import requests
from bs4 import BeautifulSoup
import json
import uuid
import youtube_dl
import requests
import os

ID = str(uuid.uuid4())
path = os.getcwd()


def download_coub(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.find_all('script', {'type': 'text/json'})
    soup_string = str(scripts)
    raw_data = soup_string.replace('[<script id="coubPageCoubJson" type="text/json">', '').replace('</script>]', '')
    jsondata = json.loads(raw_data)
    result = jsondata['file_versions']['share']['default']
    return result


def sizes_coub(url):
    file = download_coub(url)
    content_size = requests.get(file)
    sizes = int(content_size.headers['content-length'])
    print(sizes)
    return sizes


def thumbnail_coub(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        thumbnail = meta['thumbnail']
        print(thumbnail)
        return thumbnail


def audio_coub(url):
    filename = ID
    #outtmpl = '/var/www/savebot/content/{}.%(ext)s'.format(filename)
    outtmpl = '/var/www/savebot/content/{}.%(ext)s'.format(filename)
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': outtmpl
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url)
        file = open('/var/www/savebot/content/' + filename + '.mp3', 'rb')
        return file
