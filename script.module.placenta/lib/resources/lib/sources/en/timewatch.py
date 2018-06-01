# -*- coding: utf-8 -*-
''' 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

	Scraper for Placenta: plugin.video.placenta
	Author: K1ept0
'''
import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.timetowatch.video']
        self.base_link = 'https://www.timetowatch.video'
        self.search_link = '%s/wp-json/wp/v2/posts?search=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = title.lower()
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(':', '%3A').replace(',', '%2C').replace('&', '%26').replace("'", '%27').replace(' ', '+').replace('...', ' '))
            search_results = client.request(url)
            match = re.compile('<div data-movie-id=.+?href="(.+?)".+?oldtitle="(.+?)"',re.DOTALL).findall(search_results)
            for movie_url, movie_title in match:
                clean_title = cleantitle.get(title)
                movie_title = movie_title.replace('&#8230', ' ').replace('&#038', ' ').replace('&#8217', ' ').replace('...', ' ')
                clean_movie_title = cleantitle.get(movie_title)
                if clean_movie_title in clean_title:
                    return movie_url
            return
        except:
            failure = traceback.format_exc()
            log_utils.log('K1ept0 - Movie - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            html = client.request(url)
            links = re.compile('<form id="linkplayer.+?href="(.+?)"',re.DOTALL).findall(html)
            for link in links:
                quality,info = source_utils.get_release_quality(link, url)
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('K1ept0 - Sources - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url