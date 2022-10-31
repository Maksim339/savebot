import requests
from bs4 import BeautifulSoup
import uuid

ID = str(uuid.uuid4())
path = "/var/www/savebot/content/"


def download_xvideos(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.findAll('script')[6]
    soup_string = str(scripts)
    raw_data = soup_string.split("html5player.setVideoUrlHigh('")[-1].split("');")[0]
    content_size = requests.get(raw_data, stream=True)
    filename = ID
    with open('/var/www/savebot/content/' + filename + '.mp4', 'wb') as f:
        for data in content_size.iter_content(1024000):
            f.write(data)
    file = open('/var/www/savebot/content/' + filename + ".mp4", "rb")
    return file


def sizes_xvideos(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.findAll('script')[6]
    soup_string = str(scripts)
    raw_data = soup_string.split("html5player.setVideoUrlHigh('")[-1].split("');")[0]
    content_size = requests.get(raw_data, stream=True)
    file_size = int(content_size.headers['Content-Length'])
    return file_size
