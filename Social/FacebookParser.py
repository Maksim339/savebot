import requests
import re
import uuid
import youtube_dl
import os


ID = str(uuid.uuid4())
path = os.getcwd()


def download_facebook(url):
    request = requests.get(url)
    utf = request.content.decode('utf-8')
    type_selection = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', utf)
    ts_group = type_selection.group()
    total = re.sub('<meta name="medium" content="', '', ts_group)
    extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', utf)
    video_link = extract_video_link.group()
    total = re.sub('meta property="og:video" content="', '', video_link)
    total = re.sub('amp;', '', total)
    req_file_size = requests.get(total, stream=True)
    value_size = 1024000
    filename = ID
    with open('/var/www/savebot/content/' + filename + '.mp4', 'wb') as f:
        for data in req_file_size.iter_content(value_size):
            f.write(data)
    facebook_file = open('/var/www/savebot/content/' + filename + ".mp4", "rb")
    return facebook_file

def sizes_facebook(url):
    request = requests.get(url)
    utf = request.content.decode('utf-8')
    type_selection = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', utf)
    ts_group = type_selection.group()
    total = re.sub('<meta name="medium" content="', '', ts_group)

    extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', utf)
    video_link = extract_video_link.group()
    total = re.sub('meta property="og:video" content="', '', video_link)
    total = re.sub('amp;', '', total)
    req_file_size = requests.get(total, stream=True)
    value_file = int(req_file_size.headers['Content-Length'])
    return value_file


def thumbnail_facebook(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        thumbnail = meta['thumbnail']
        print(thumbnail)
        return thumbnail

