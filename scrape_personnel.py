import json
import hashlib
import logging
import os
import re
import shutil
from bs4 import BeautifulSoup
import requests

import cache
logger = logging.getLogger('scraper')
logging.basicConfig(level='DEBUG')


@cache.page
def get(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content


@cache.binary
def get_binary(url):#, artist, album, size):
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    resp.raw.decode_content = True
    return resp.raw.read()


def parse_album_div(div):
    artist_name = (div
            .find('span', class_='by-artist')
            .text
            .lstrip('by '))
    album_link = div.find('a', class_='album-title')
    page_url = album_link['href']
    album_name = album_link.text.strip()
    thumbnail_url = div.find('img')['src']
    return {'artist': artist_name,
            'url': page_url,
            'name': album_name,
            'thumbnail_url': thumbnail_url}

def get_personnel_soup(soup):
    return soup.find('ul', class_='personnel')

def parse_personnel_soup(soup):
    persons = []
    items = soup.find_all('li')
    
    for item in items:
        name = item.find('span', class_='name').text
        instrument = item.find('span', class_='instrument').text
        persons.append((name, instrument))
    return persons

def clean_name(name):
    name = name.replace(os.sep, ' ')
    name = name.strip()
    name = re.sub('[^a-zA-Z0-9]', '_', name)
    return name
    
def download_album_image(url, artist, album, size):
    image_type = url.split('.')[-1]
    directory = os.path.join('img', 'albums')
    album=clean_name(album)
    artist=clean_name(artist)
    filename = '{}_{}_{}.{}'.format(artist, album, size, image_type) 
    filepath = os.path.join(directory, filename)
    
    content = get_binary(url)

    with open(filepath, 'wb') as fh:
        fh.write(content)

START_URL = 'http://www.portofrancorecords.com/albums-and-store/'
resp = get(START_URL)
soup = BeautifulSoup(resp)
album_divs = soup.find_all('div', class_='album')
albums = [parse_album_div(div) for div in divs]
for album in albums:
    download_album_image(album['thumbnail_url'], album['artist'], album['name'], 'thumbnail')
album_pages = [get(album['url']) for album in albums]
album_soups = [BeautifulSoup(page) for page in album_pages]
personnel_lists = [get_personnel_soup(page) for page in album_soups]
personnels = [parse_personnel_soup(s) for s in personnel_lists]
for album, personnel in zip(albums, personnels):
    album['personnel'] = personnel

with open('albums.json', 'w') as fh:
    json.dump(albums, fh, indent=2)
