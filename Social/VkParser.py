from Social import YoutubeParser
import requests
import uuid
import os
import youtube_dl
from bs4 import BeautifulSoup

path = os.getcwd()
ID = str(uuid.uuid4())


def download_vk(url):
    try:
        url.replace('%2Fpl_cat_trends', '')
        filename = ID
        outtmpl = '/var/www/savebot/content/' + filename + '.mp4'
        ydl_opts = {
            'format': 'best',
            'outtmpl': outtmpl
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            file = open('/var/www/savebot/content/' + filename + '.mp4', 'rb')
            print(file)
            return file
    except:
        return 'invalid_url'
        # verison = 5.52
        # id_videos = url.split('%')[0].split('=video')[-1]
        # token = '3ed6d77ac6df0aa9c373b8cf5282ef851aa9582c880a2fdb2a4c9c0bcc273b037cf6706e13e6da0fbf57f'
        # response = requests.get('https://api.vk.com/method/video.get',
        #                         params={'v': verison, 'videos': id_videos, 'access_token': token})
        # link_youtube = 'https://www.youtube.com/'
        # soup = BeautifulSoup(response.text, 'lxml')
        # json_data = response.json()
        # total = json_data['response']['items'][-1]['player']
        #
        # if link_youtube in total:
        #     rename = total.replace('embed', 'watch')
        #     url = rename.split('?')[0]
        #     send_youtube = YoutubeParser.download_youtube(url)
        #     return send_youtube
        # else:
        #     response = requests.get(total)
        #     soup = BeautifulSoup(response.text, 'lxml')
        #     scripts = soup.findAll('source')[1].get('src')
        #     print(scripts)
        #     if '=UNKNOWN' in scripts:
        #         return 'privat_account'
        #     scripts = scripts.split('?')[0]
        #     req_file_size = requests.get(scripts, stream=True)
        #     filename = ID
        #     with open('/var/www/savebot/content/' + filename + '.mp4', 'wb') as f:
        #         for data in req_file_size.iter_content(1024000):
        #             f.write(data)
        #     vk_file = open('/var/www/savebot/content/' + filename + '.mp4', 'rb')
        #     return vk_file


def sizes_vk(url):
    try:
        ydl_opts = {
            'format': 'best',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            formats = meta['formats'][-1]['url']
            content_size = requests.head(formats, stream=True)
            sizes = int(content_size.headers['content-length'])
            print(sizes)
        return sizes
    except:
        return 'invalid_url'
    # try:
    # verison = 5.52
    # id_videos = url.split('%')[0].split('=video')[-1]
    # token = '3ed6d77ac6df0aa9c373b8cf5282ef851aa9582c880a2fdb2a4c9c0bcc273b037cf6706e13e6da0fbf57f'
    # response = requests.get('https://api.vk.com/method/video.get',
    #                         params={'v': verison, 'videos': id_videos, 'access_token': token})
    # link_youtube = 'https://www.youtube.com/'
    # soup = BeautifulSoup(response.text, 'lxml')
    # json_data = response.json()
    # total = json_data['response']['items'][-1]['player']
    # print(total)
    #
    # if link_youtube in total:
    #     rename = total.replace('embed', 'watch')
    #     url = rename.split('?')[0]
    #     file_size = YoutubeParser.sizes_youtube(url)
    #     return file_size
    #
    # else:
    #     response = requests.get(total)
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     scripts = soup.findAll('source')[1].get('src')
    #     scripts = scripts.split('?')[0]
    #     content_size = requests.get(scripts)
    #     sizes = content_size.headers['content-length']
    #     print(sizes)
    #     return int(sizes)
    # except:
    #     return 'invalid_url'


def thumbnail_vk(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        thumbnail = meta['thumbnail']
        print(thumbnail)
        return thumbnail


def audio_vk(url):
    return 'confusing_error'
