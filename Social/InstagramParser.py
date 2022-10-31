import os
import re
import uuid
import json
from Social.Stories import download_stories
from aiogram import types
from instaloader import *

ID = str(uuid.uuid4())


async def download_instagram(url):
    '''
    set proxy:
    https://github.com/instaloader/instaloader/issues/459
    # '''

    # url = url.replace('?hl=ru', '').replace('?utm_source=ig_web_copy_link', '') \
    #     .replace('?utm_source=ig_web_button_share_sheet', '')
    # url = re.sub('[?]igshid.*', '', url)
    # url = re.sub('[?]utm_source.*', '', url)
    # slash_count = len(url.split('/'))
    # if not url.endswith('/'):
    #     url = url + '/'
    # highlights = re.fullmatch(r'^(https:)[/][/]([^/]+[.])([r][u]|[c][o][m])[/]stories[/]highlights/.*', url)
    # if highlights:
    #     return 'highlights'
    # if slash_count == 5:
    #     return 'profile_guide'
    # # profile = re.fullmatch(r'^https://www.instagram.com/[^0-9]\w+/$', url)
    # # if profile:
    # #     return 'profile_guide'
    #
    # story = re.fullmatch(r'^(https:)[/][/]([^/]+[.])([r][u]|[c][o][m])[/]stories[/].*', url)
    #
    # if story:
    #     try:
    #         file = download_stories(url)
    #         return file
    #     except Exception as e:
    #         # print(e)
    #         return e
    #         # return 'privat_account'
    # # try:
    # shortcode = url.split('/')[-1]
    # if shortcode == '':
    #     shortcode = url.split('/')[-2]
    # content_directory = '/var/www/savebot/content/'
    # USER = 'faken.ews228'
    # PASSWORD = 'xjby0m0s228'
    #
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 ' \
    #              '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    # instance = instaloader.Instaloader(dirname_pattern=content_directory, download_pictures=False,
    #                                    download_videos=False,
    #                                    download_video_thumbnails=False, compress_json=False,
    #                                    filename_pattern=shortcode, download_comments=False, user_agent=user_agent)
    # # instance.test_login()
    #
    # try:
    #     instance.load_session_from_file('forbot_tg', '/var/www/savebot/content/stories/' + 'forbot_tg')
    #     try:
    #         os.chmod('forbot_tg', mode=0o777)
    #     except:
    #         print('exist')
    # except Exception as e:
    #     instance.login(user=USER, passwd=PASSWORD)
    #     print(e)
    #
    # # instance.login(user=USER, passwd=PASSWORD)
    # # instance.save_session_to_file('/var/www/savebot/content/stories/' + 'forbot_tg')
    #
    # # instance.save_session_to_file(content_directory + 'stories/' + 'forbot_tg')
    # # profile = Profile.from_username(instance.context, username=victim_username)
    # post = Post.from_shortcode(instance.context, shortcode)
    # instance.download_post(post, target=content_directory)
    #
    # pathInfoFile = open(content_directory + '/' + shortcode + '.json', 'rb')
    #
    # try:
    #     os.remove(content_directory + '/' + shortcode + '.txt')
    # except Exception as e:
    #     print(e)
    # jsonInfo = json.loads(pathInfoFile.read())
    # fileFormat = jsonInfo['node']['__typename']
    # if fileFormat == 'GraphVideo':
    #     fileUrl = jsonInfo['node']['video_url']
    #     return fileUrl  # , shortcode
    #
    # elif fileFormat == 'GraphImage':
    #     fileUrl = jsonInfo['node']['display_resources'][-1]['src']
    #     return fileUrl  # , shortcode
    #
    # elif fileFormat == 'GraphSidecar':
    #     countContentCarousel = len(jsonInfo['node']['edge_sidecar_to_children']['edges'])
    #     total_page = jsonInfo['node']['edge_sidecar_to_children']['edges']
    #     media = types.MediaGroup()
    #
    #     for i in range(0, int(countContentCarousel)):
    #         regex = total_page[i]['node']['is_video']
    #         if regex is True:
    #             # This_video = \
    #             # jsonInfo['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children'][
    #             # 'edges'][i]['node']['video_url']
    #             This_video = jsonInfo['node']['edge_sidecar_to_children']['edges'][i]['node']['video_url']
    #             media.attach_video(This_video)
    #
    #
    #         else:
    #             Not_video = \
    #                 jsonInfo['node']['edge_sidecar_to_children'][
    #                     'edges'][i]['node']['display_resources'][-1]['src']
    #             media.attach_photo(Not_video)
    #     return media  # , shortcode
    # # except Exception as e:
    # #     return 'no_service'

    return 'rework_service'


def sizes_instagram(url):
    return 1700000
