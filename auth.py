import Social.YoutubeParser
import Social.InstagramParser
import Social.CoubParser
import Social.VkParser
import Social.PinterestParser
import Social.FacebookParser
import Social.TiktokParser
import Social.TwitterParser
import Social.PhParser
import Social.XvideosParser
import Social.SoundcloudParser
import Social.TiktokParser
import os
import re
import requests
import json
from bs4 import BeautifulSoup
import psycopg2
import mysql.connector

# mydb = psycopg2.connect(
#     host="localhost",
#     user="savebot",
#     password="898989qW!",
#     database="mediabot",
# )

# Для локального теста
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database="",
)
print('connected')

services = 'instagram.com', 'vk.com', 'youtube.com', 'tiktok.com', 'pinterest.com', \
           'facebook.com', 'pornhub.com', 'twitter.com', 'xvideos.com', 'soundcloud.com', \
           'youtu.be', 'm.youtube.com', 'vm.tiktok.com'

size_data = {
    'sizes_coub': Social.CoubParser.sizes_coub,
    'sizes_tiktok': Social.TiktokParser.sizes_tiktok,
    'sizes_youtube': Social.YoutubeParser.sizes_youtube,
    'sizes_instagram': Social.InstagramParser.sizes_instagram,
    'sizes_vk': Social.VkParser.sizes_vk,
    'sizes_pinterest': Social.PinterestParser.sizes_pinterest,
    'sizes_facebook': Social.FacebookParser.sizes_facebook,
    'sizes_pornhub': Social.PhParser.sizes_pornhub,
    'sizes_twitter': Social.TwitterParser.sizes_twitter,
    'sizes_xvideos': Social.XvideosParser.sizes_xvideos,
    'sizes_soundcloud': Social.SoundcloudParser.sizes_soundcloud
}

download_data = {
    'download_coub': Social.CoubParser.download_coub,
    'download_tiktok': Social.TiktokParser.download_tiktok,
    'download_youtube': Social.YoutubeParser.download_youtube,
    'download_instagram': Social.InstagramParser.download_instagram,
    'download_vk': Social.VkParser.download_vk,
    'download_pinterest': Social.PinterestParser.download_pinterest,
    'download_facebook': Social.FacebookParser.download_facebook,
    'download_pornhub': Social.PhParser.download_pornhub,
    'download_twitter': Social.TwitterParser.download_twitter,
    'download_xvideos': Social.XvideosParser.download_xvideos,
    'download_soundcloud': Social.SoundcloudParser.download_soundcloud
}

thumbnail_data = {
    'thumbnail_coub': Social.CoubParser.thumbnail_coub,
    'thumbnail_tiktok': Social.TiktokParser.thumbnail_tiktok,
    'thumbnail_youtube': Social.YoutubeParser.thumbnail_youtube,
    'thumbnail_vk': Social.VkParser.thumbnail_vk,
    'thumbnail_facebook': Social.FacebookParser.thumbnail_facebook,
    'thumbnail_pornhub': Social.PhParser.sizes_pornhub,
    'thumbnail_twitter': Social.TwitterParser.thumbnail_twitter,
    'thumbnail_soundcloud': Social.SoundcloudParser.thumbnail_soundcloud
}

audio_data = {
    'audio_coub': Social.CoubParser.audio_coub,
    'audio_tiktok': Social.TiktokParser.audio_tiktok,
    'audio_youtube': Social.YoutubeParser.audio_youtube,
    'audio_soundcloud': Social.SoundcloudParser.audio_soundcloud,
    'audio_vk': Social.VkParser.audio_vk
}


# ИЗМЕНЯЕТ ДОМЕН ДО ФОРМАТА: youtube.com
class Control:

    def __init__(self):
        self.url = url

    # ДОМЕН ФОРМАТА youtube.com
    def domain_formater(url):
        if url.startswith('https://youtu.be/'):
            part = 'watch?v='
            url1 = url.replace('.', '')
            domain = url1.split('//')[-1].split('/')[0] + '.com'
            id_video = url1.split('youtube/')[-1]
            url = 'https://' + domain + '/' + part + id_video

        if url.startswith('https://m.youtube.com/'):
            url = url.replace('m.', '')

        if url.startswith('https://vm.tiktok.com'):
            url = url.replace('vm.', '')

        if url.startswith('https://pin.it'):
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/83.0.4103.97 Safari/537.36"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            scripts = soup.findAll('script', {'id': 'initial-state'})
            soup_string = str(scripts)
            raw_data = soup_string.replace('[<script id="initial-state" type="application/json">', '').replace(
                '</script>]',
                '')
            jsondata = json.loads(raw_data)
            getShortcode = jsondata['location']['history'][0]['pathname']
            shortcode = '/pin/' + getShortcode.split('/')[2]
            url = 'https://www.pinterest.com' + shortcode

        clean = url.replace('www.', '').replace('.ru', '.com').replace('ru.', '')
        ru_com = re.sub(r'[.]([r][u]|[c][o][m])', '.com', clean)
        domain = ru_com.split('https://')[-1].split('.com')[0] + '.com'
        domain = domain.replace('rt.', '')
        # print('domain >>> ' + str(domain))
        return domain

    # ОТДАЕТ КЛЮЧ СЛОВА "accept" / "no_service", продолжать проваливаться в скрипт /
    # / сообщить пользователю, что нет сервиса в списке.
    def domain_validation(url):
        if url.startswith('https://youtu.be/'):
            part = 'watch?v='
            url1 = url.replace('.', '')
            domain = url1.split('//')[-1].split('/')[0] + '.com'
            id_video = url1.split('youtube/')[-1]
            url = 'https://' + domain + '/' + part + id_video
        domain = Control.domain_formater(url)
        clean = url.replace('www.', '').replace('.ru', '.com')
        if domain in services:
            domain = domain.replace('.com', '').replace('rt.', '')
            regex = re.fullmatch(r'^(https:)[/][/]([^/]+[.])([r][u]|[c][o][m]).*', clean)
            # print('regex >>> ' + str(regex))
            return 'accept'
        else:
            return 'no_service'

    # ОТДАЕТ РАЗМЕР ФАЙЛА
    def file_size(url):
        domain = Control.domain_formater(url)
        domain = domain.replace('rt.', '')
        domain = domain.split('.')[0]
        funcname = 'sizes_{}'.format(domain)
        sizes = size_data[funcname](url)
        check_file = round(int(sizes) / 1000000, 1)
        # print('Размер файла ' + str(check_file) + ' MB')
        return check_file

    # НАПРАВЛЯЕТ В ЗАВИСИМОСТИ ОТ РАЗМЕРА ФАЙЛА
    async def media_reference(url):
        check_file = Control.file_size(url)
        domain = Control.domain_formater(url)
        if check_file <= 47:
            domain = domain.replace('.com', '')
            funcname = 'download_{}'.format(domain)
            # if funcname == 'download_youtube':
            readyfile = await download_data[funcname](url)
            # else:
            #     readyfile = download_data[funcname](url)
            return readyfile

        elif 47 <= check_file <= 1500:
            domain = domain.replace('.com', '')
            funcname = 'download_{}'.format(domain)
            readyfile = await download_data[funcname](url)
            return 'sizer', readyfile
            # return 'sizer' + readyfile

        else:
            return 'large_data'

    def preview(url):
        domain = Control.domain_formater(url).replace('.com', '')
        funcname = 'thumbnail_{}'.format(domain)
        thumbnail = thumbnail_data[funcname](url)
        return thumbnail

    def audio(url):
        domain = Control.domain_formater(url).replace('.com', '')
        funcname = 'audio_{}'.format(domain)
        audio = audio_data[funcname](url)
        # print('audio >>> ' + str(audio))
        return audio


def client_api():
    api_id =
    api_hash = ''
    return api_id, api_hash


def delete_file(file):
    file = str(file)
    path = file.replace("<_io.BufferedReader name='", '').replace("'>", '')
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


def delete_json_file(shortcode):
    path = '/var/www/savebot/content/'
    json_file = path + shortcode + '.json'
    # print(json_file)
    if os.path.exists(json_file):
        os.remove(json_file)
    else:
        print("The file does not exist")


def check_url_database(url):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT file_id FROM bot_url_history WHERE url = '" + url + "'")
    myresult = mycursor.fetchone()
    # print(myresult)
    try:
        return myresult[0]
    except:
        return myresult


def insert_file_database(url, file_id):
    mycursor = mydb.cursor()

    sql = "INSERT INTO bot_url_history (url, file_id) VALUES (%s, %s)"
    val = (url, file_id)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


def insert_statistics(user_id, date_add, button_id, reaction_time, url):
    mycursor = mydb.cursor()

    sql = "INSERT INTO statistics (user_id, date_add, button_id, reaction_time, url) VALUES (%s, %s, %s, %s, %s)"
    val = (user_id, date_add, button_id, reaction_time, url)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


def check_base(url, user_id, date_add):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM statistics WHERE url = %s AND user_id = %s AND date_add = %s"
    adr = (url, user_id, date_add)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    return myresult


def update_records(button_id, url, user_id, date_add):
    mycursor = mydb.cursor()
    sql = "UPDATE statistics SET button_id = %s WHERE url = %s AND user_id = %s AND date_add = %s"
    adr = (button_id, url, user_id, date_add)
    mycursor.execute(sql, adr)
    mydb.commit()
