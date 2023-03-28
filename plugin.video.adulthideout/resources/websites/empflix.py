import re
import xbmc
from ..functions import add_dir, add_link, make_request, fanart, logos
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib.parse as urllib_parse


def process_empflix_content(url, mode=None):
    # changing the base-URl to base-URL + /new/1/
    url = url + "/new/1/"
    
    content = make_request(url)
    add_dir('[COLOR blue]Search[/COLOR]', 'empflix', 5, logos + 'empflix.png', fanart)
    match = re.compile('<img src=".+?" data-src="([^"]*)"(.+?)<p class="title"><a href="([^"]*)" title="([^"]*)".+?<span class="duration">([^"]*)</span>', re.DOTALL).findall(content)
    
    # Get the base URL part from the input URL
    base_url = url.rsplit("/", 3)[0]
    
    for thumb, dummy, url, name, duration in match:
        name = name.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', '`')
        url = url.replace('THUMBNUM/', '')
        add_link(name + ' [COLOR lime]('+ duration + ')[/COLOR]', base_url + url, 4, thumb, fanart)
    
    try:
        match = re.compile('<a href="([^"]+)" class="no-page next-page">Next</a>').findall(content)
        match = [item.replace('&amp;', '&') for item in match]
        add_dir('[COLOR blue]Next  Page  >>>>[/COLOR]', base_url + match[0], 2, logos + 'empflix.png', fanart)
    except:
        pass

def play_empflix_video(url):
    content = make_request(url)
    media_url = re.compile(r"html5player\.setVideoUrlHigh\('(.+?)'\);").findall(content)[0]
    return media_url