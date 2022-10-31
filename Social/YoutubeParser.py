from __future__ import unicode_literals
import os
import uuid
from typing import Dict
import aiofiles
import youtube_dl
import requests
import re
import asyncio
import asyncio.subprocess
import sys
import pafy
import random

ID = str(uuid.uuid4())
path = os.getcwd()

"""
ОШИБКА: "ERROR: iGnk3eqiuuU: YouTube said: Unable to extract video data" из-за yt-dl версии может возникать
         На данный момент - youtube-dl==2021.1.24.1 , если меняешь на youtube-dl==2021.4.1 - отрабатывает!?
"""


def get_proxy():
    proxy = ['91.246.195.183:6952',
             '193.23.253.222:7794',
             '193.23.253.106:7678']
    random_proxy = random.choice(proxy)
    return random_proxy


async def download_youtube(video_url):
    if 'channel' in video_url:
        return 'no_service'
    if video_url.startswith('https://youtu.be/'):
        fname = video_url.replace('https://youtu.be/', '')
    if video_url.startswith('https://www.youtube.com/'):
        fname = video_url.split('watch?')[-1]
    fname = fname.replace('v=', '')

    # Синхронное скачаивание видео
    # outtmpl = '/var/www/savebot/content/' + fname + '.mp4'
    # ydl_opts = {
    #     'format': 'best',
    #     'outtmpl': outtmpl,
    #     'nocheckcertificate:': True,
    #     'proxy': 'irkvpn:GioGio79@168.80.42.120:50139',
    #
    # }
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.extract_info(video_url)
    #     file = open(outtmpl, 'rb')
    #     os.chmod(outtmpl, 0o777)
    # print(file)
    # return file

    # Асинхронное скачивание
    proxy = get_proxy()
    print(proxy)
    outtmpl = '/var/www/savebot/content/' + fname
    args = ['youtube-dl', '-f', 'best', '--proxy', proxy,
            '-o', '/var/www/savebot/content/%(id)s.%(ext)s', video_url]
    create = asyncio.create_subprocess_exec(*args,
                                            stdout=asyncio.subprocess.PIPE,
                                            stderr=asyncio.subprocess.PIPE)
    proc = await create
    code = await proc.wait()
    if code != 0:
        print("Command '{}' failed.".format(' '.join(args)), file=sys.stderr)
        logs = await proc.stderr.read()
        raise OSError(logs)
    # return await proc.stdout.read()
    file = open(outtmpl + '.mp4', 'rb')
    print('file', file)
    os.chmod(outtmpl + '.mp4', 0o777)
    return file


# return 'rework_service'


def title(url):
    response = requests.get(url, stream=True)
    titleSearch = re.search(r'<title>.*', response.text).group()
    title = titleSearch.replace('<title>', '').replace('</title>', '').replace('&quot;', '').replace('&#39;', '')
    title = title.split('<meta')[0]
    return title


def sizes_youtube(url):
    proxy = get_proxy()
    try:

        video = pafy.new(url)
        streams = video.getbest()
        value = streams.get_filesize()
        return value

    except:
        ydl_opts = {
            'ignoreerrors': True,
            'format': 'best',
            'proxy': proxy,

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            formats = len(meta['formats'])
            print('formats : ' + str(formats))
            for i in range(formats):
                bestFormat = meta['formats'][i]['format_note']
                # print(bestFormat['formats'][1]['format_note'])
                if bestFormat == '720p' and meta['formats'][i]['filesize'] is not None:
                    sizes = meta['formats'][i]['filesize']
                    # print(meta['formats'][0])
                    # print(sizes)
                # print(bestFormat, meta['formats'][i]['filesize'])
        return sizes

    # except:
    # try:
    # print(proxy)
    # ydl_opts = {
    #     'format': 'best',
    #     'proxy': proxy,
    # }
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     meta = ydl.extract_info(url, download=False)
    #     formats = meta['formats'][-1]['url']
    #     proxies: Dict[str, str] = {
    #         'http': 'http://' + proxy, #сюда прокси
    #         'https': 'https://' + proxy #сюда прокси
    #     }
    #     content_size = requests.request('GET', formats, proxies=proxies)
    #     # content_size = requests.get(formats, stream=True)
    #     sizes = int(content_size.headers['content-length'])
    #     print(sizes)
    #     return sizes
    # except:
    # return 70000000


def thumbnail_youtube(url):
    if url.startswith('https://youtu.be/'):
        shortcode = url.split('youtu.be/')[-1]
    else:
        shortcode = url.split("=", 1)[1]
    thumbnail = 'https://img.youtube.com/vi/' + shortcode + '/maxresdefault.jpg'
    return thumbnail


def audio_youtube(url):
    proxy = get_proxy()
    filename = ID
    outtmpl = '/var/www/savebot/content/' + filename + '.mp3'
    ydl_opts = {
        'format': 'best',
        'outtmpl': outtmpl,
        'nocheckcertificate:': True,
        'proxy': proxy,

    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url)
        formats = meta['formats']
        num = len(meta['formats'])
        for i in range(0, num):
            if formats[i]['ext'] == "m4a":
                audio = formats[i]['url']
                content_size = requests.get(audio, stream=True)
                filename = ID
                with open('/var/www/savebot/content/' + filename + '.mp3', 'wb') as f:
                    for data in content_size.iter_content(1024000):
                        f.write(data)
                file = open('/var/www/savebot/content/' + filename + '.mp3', "rb")
        return file


async def main(video_url):
    # video_url = 'video_url'
    await download_youtube(video_url)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
