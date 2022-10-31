import youtube_dl
import uuid

ID = str(uuid.uuid4())
path = "/var/www/savebot/content/"


async def download_tiktok(url):
    # try:
    #     fname = ID
    #     outtmpl = '/var/www/savebot/content/' + fname + '.mp4'
    #     ydl_opts = {
    #         'format': 'best',
    #         'outtmpl': outtmpl,
    #     }
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         ydl.extract_info(url)
    #         file = open(outtmpl, 'rb')
    #     return file
    # except Exception as e:
    #     return 'confusing_error'
    # filename = ID
    # path = '/var/www/savebot/content/'
    # outtmpl = '/var/www/savebot/content/{}.%(ext)s'.format(filename)
    # ydl_opts = {
    #     'format': 'best',
    #     'outtmpl': outtmpl
    # }
    #
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([url])
    #     file = open('/var/www/savebot/content/' + filename + '.mp4', 'rb')
    #     print(file)
    #     return file
    return 'tt_video'


def sizes_tiktok(url):
    return 15000


def thumbnail_tiktok(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        thumbnail = meta['thumbnail']
        print(thumbnail)
        return thumbnail


def audio_tiktok(url):
    return 'confusing_error'
