import re
import xbmc
from ..functions import add_dir, add_link, make_request, fanart, logos
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib.parse as urllib_parse
import urllib.request

def process_youjizz_content(url, mode=None):
    if "search" not in url:
        url = 'https://www.youjizz.com' + "/newest-clips/1.html"

    add_dir(f'Search YouJizz', 'youjizz', 5, logos + 'youjizz.png', fanart)
    content = make_request(url)
    match = re.compile('data-original="([^"]*)".+?<a href=\'(.+?)\' class="">(.+?)</a>', re.DOTALL).findall(content)
    base_url = url.rsplit("/", 3)[0]
    for thumb, url, name in match:
        add_link(name, 'https://www.youjizz.com' + url, 4, 'https:' + thumb, fanart)

def play_youjizz_video(url):
    content = make_request(url)
    data = re.compile('"filename":"([^"]+.mp4[^"]*)",').findall(content)

    preferred_order = ["1080", "720"]

    for quality in preferred_order:
        for media_url in data:
            if quality in media_url:
                media_url = 'https:' + media_url.replace('/', '')
                return media_url

    # If 1080 and 720 are not found, return the first available media_url
    media_url = 'https:' + data[0].replace('/', '')
    return media_url