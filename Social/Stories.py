from instaloader import *
import json
import os


def download_stories(url):
    # Get instance
    mediaId = url.split('/')[-1]
    if mediaId == '':
        mediaId = url.split('/')[-2]
    if '?hl=ru' in url:
        url = url.replace('?hl=ru', '')
    victim_username = url.split('stories/')[-1].split('/')[0]
    USER = 'faken.ews228'
    PASSWORD = 'xjby0m0s228'
    content_directory = '/var/www/savebot/content/stories/'
    instance = instaloader.Instaloader(dirname_pattern=content_directory, download_pictures=False,
                                       download_videos=False,
                                       download_video_thumbnails=False, compress_json=False,
                                       filename_pattern="{mediaid}")

    # Авторизация. Использование сессии - иногда слетает не выдавая ошибок
    try:
        instance.load_session_from_file('forbot_tg', content_directory + 'forbot_tg')
        try:
            os.chmod('forbot_tg', mode=0o777)
        except:
            print('exist')
    except Exception as e:
        instance.login(user=USER, passwd=PASSWORD)
        print(e)

    # instance.login(user=USER, passwd=PASSWORD)
    # instance.save_session_to_file(content_directory + 'forbot_tg')
    profile = Profile.from_username(instance.context, username=victim_username)

    instance.download_stories(userids=[profile.userid], filename_target='content/stories'.format(profile.username))
    pathInfoFile = open(content_directory + mediaId + '.json', 'r')
    jsonInfo = json.loads(pathInfoFile.read())
    fileFormat = jsonInfo['node']['__typename']
    if fileFormat == 'GraphStoryVideo':
        fileUrl = jsonInfo['node']['video_resources'][-1]['src']
        print(fileUrl)
        return fileUrl
    elif fileFormat == 'GraphStoryImage':
        fileUrl = jsonInfo['node']['display_resources'][-1]['src']
        print(fileUrl)
        return fileUrl
