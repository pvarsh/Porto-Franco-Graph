import string
import pdb
import hashlib
import os
import functools

import requests
from bs4 import BeautifulSoup

CATALOG_URL = "http://www.portofrancorecords.com/albums-and-store/"
CACHE_PATH = "cache"

class Album(object):

    def __init__(self, title, artist, url=None):
        self._title = title
        self._artist = artist
        self._url = url
        self._personnel = [] 

    def describe(self):
        print("'{title}' by {artist}\n"
              "Personnel: "
              .format(title=self.title, artist=self.artist))
        for musician in self.personnel:
            print musician

    @property
    def instruments(self):
        instruments = set()
        for musician in self.personnel:
            instruments.update(musician.instruments)
        return instruments

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def personnel(self):
        return self._personnel

    @property
    def artist(self):
        return self._artist

    def personnel_from_page(self):
        soup = make_soup(self.url)
        ul = soup.find("ul", class_="personnel")
        list_items = ul.find_all("li")
        for li in list_items:
            musician = Musician.from_pfr_list_item(li)
            self._personnel.append(musician)

class Musician(object):

    def __init__(self, name, instruments):
        self._name = name
        self._instruments = instruments

    def __str__(self):
        return "Name: {}, instruments: {}".format(self.name, self.instruments)

    @property
    def instruments(self):
        return self._instruments

    @property
    def name(self):
        return self._name

    @classmethod
    def from_pfr_list_item(cls, li):
        name = li.find("span", class_="name").text
        instruments = li.find("span", class_="instrument").text
        instruments = [
            instrument.strip(string.digits + string.punctuation + ' ')
            for instrument in instruments.split(',')
            ]
        instruments = [instrument for instrument in instruments if instrument]
        return cls(name, instruments)

def cache_filename(url):
    return hashlib.md5(url).hexdigest()

def fetch_page(url):
    cache_filepath = os.path.join(CACHE_PATH, cache_filename(url))
    if not os.path.isfile(cache_filepath):
        resp = requests.get(url)
        resp.raise_for_status()
        with open(cache_filepath, 'wb') as fh:
            fh.write(resp.content)
    return cache_filepath

def make_soup(url):
    filepath = fetch_page(url)
    with open(filepath, 'rb') as fh:
        soup = BeautifulSoup(fh)
    return soup

def scrape_album_div(div):
    title = div.find("a", class_="album-title")
    name = title.text.strip()
    url = title.get('href')
    artist = div.find("span", class_="by-artist").text.strip()
    artist = artist[3:] if artist[:3] == "by " else artist
    return (name, artist, url)

def get_albums(url):
    soup = make_soup(url)
    album_divs = soup.find_all("div", class_="album")
    albums = []
    for div in album_divs:
        title, artist, url = scrape_album_div(div)
        album = Album(title, artist, url)
        albums.append(album)
    return albums

def scrape_album(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content)
    return soup.find("h1", class_="entry-title")

if __name__ == "__main__":
    albums = get_albums(CATALOG_URL)
    for album in albums:
        album.personnel_from_page()
