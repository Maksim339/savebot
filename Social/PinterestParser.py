import requests
from bs4 import BeautifulSoup
import json
import uuid
import os

path = os.getcwd()
ID = str(uuid.uuid4())


async def download_pinterest(url):
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.findAll('script', {'id': 'initial-state'})
    soup_string = str(scripts)
    raw_data = soup_string.replace('[<script id="initial-state" type="application/json">', '').replace('</script>]',
                                                                                                       '')
    jsondata = json.loads(raw_data)
    regex = jsondata['resourceResponses'][0]['response']['data']

    try:
        content = regex['videos']['video_list']['V_720P'].get('url')
        req_file_size = requests.get(content, stream=True)
        filename = ID
        with open('/var/www/savebot/content/' + filename + '.mp4', 'wb') as f:
            for data in req_file_size.iter_content(1024000):
                f.write(data)
        pinterest_file = open('/var/www/savebot/content/' + filename + '.mp4', 'rb')
        print(pinterest_file)
        return pinterest_file

    except TypeError:
        content = regex['images']['orig'].get('url')
        return content


def sizes_pinterest(url):
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.findAll('script', {'id': 'initial-state'})
    soup_string = str(scripts)
    raw_data = soup_string.replace('[<script id="initial-state" type="application/json">', '').replace('</script>]', '')
    jsondata = json.loads(raw_data)
    regex = jsondata['resourceResponses'][0]['response']['data']

    try:
        content = regex['videos']['video_list']['V_720P'].get('url')
        content_size = requests.get(content)
        sizes = content_size.headers['content-length']
        return sizes

    except TypeError:
        content = regex['images']['orig'].get('url')
        content_size = requests.get(content)
        sizes = content_size.headers['content-length']
        return sizes
