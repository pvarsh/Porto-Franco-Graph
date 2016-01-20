import string
import pdb
import hashlib
import os
import functools

from collections import defaultdict

import requests
from bs4 import BeautifulSoup

CACHE_PATH = "cache"

class Catalog(object):

    def add_pfr(self):
        scraper = PortoFrancoScraper()
        self._albums = scraper.get_albums()

    @property
    def albums(self):
        return self._albums

    def delete_albums_by_artist(self, artist):
        self._albums = [album for album in self._albums if album.artist != artist]

    @property
    def musician_names(self):
        musicians = set()
        for album in self.albums:
            for musician in album.personnel:
                print musician.name
                musicians.add(musician.name)

        return musicians

    @property
    def musician_credits(self):
        musicians = defaultdict(list)
        for album in self.albums:
            for musician in album.personnel:
                musicians[musician.name].append(album.title)
        return musicians

class Scraper(object):

    def cache_filename(self, url):
        return hashlib.md5(url).hexdigest()

    def fetch_page(self, url):
        cache_filepath = os.path.join(CACHE_PATH, self.cache_filename(url))
        if not os.path.isfile(cache_filepath):
            resp = requests.get(url)
            resp.raise_for_status()
            with open(cache_filepath, 'wb') as fh:
                fh.write(resp.content)
        return cache_filepath

    def make_soup(self, url):
        filepath = self.fetch_page(url)
        with open(filepath, 'rb') as fh:
            soup = BeautifulSoup(fh)
        return soup

class PortoFrancoScraper(Scraper):

    CATALOG_URL = "http://www.portofrancorecords.com/albums-and-store/"

    def scrape_album_div(self, div):
        title = div.find("a", class_="album-title")
        name = title.text.strip()
        url = title.get('href')
        artist = div.find("span", class_="by-artist").text.strip()
        artist = artist[3:] if artist[:3] == "by " else artist
        return (name, artist, url)

    def get_albums(self):
        soup = self.make_soup(self.CATALOG_URL)
        album_divs = soup.find_all("div", class_="album")
        albums = []
        for div in album_divs:
            title, artist, url = self.scrape_album_div(div)
            album = Album(title, artist, url)
            albums.append(album)
        return albums


class Album(object):

    def __init__(self, title, artist, url=None):
        self._title = title
        self._artist = artist
        self._url = url
        self._personnel = []

    def describe(self):
        print(u"'{title}' by {artist}\n"
              u"Personnel: "
              .format(title=self.title, artist=self.artist))
        for musician in self.personnel:
            print(musician)
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
        soup = self.make_soup(self.url)
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
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Name: {}, instruments: {}".format(self.name, self.instruments)

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


if __name__ == "__main__":
    catalog = Catalog()
    catalog.add_pfr()
#     albums = get_albums(CATALOG_URL)
#     for album in albums:
#         album.personnel_from_page()
