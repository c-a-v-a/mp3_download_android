import json
import requests
import yt_dlp
import os
from typing import List, Dict

from Item import Item

class Database:
    """
    A class that represents a music database.

    Attributes
    ----------
    items : List[Item]
        a list of all music items (songs or albums) that are currently saved in
        the database
    location : str
        a location where database items are stored, passed as a argument to 
        constructor (default 'music/')

    Methods
    -------
    add(url, path='', name='')
        Downloads music file (or files when working with youtube playlists)
        from url, saves it in database location, and appends it to `items`.
    """
    def __init__(self, location: str = 'music/'):
        """
        Constructs a database on given location.

        Parameters
        ----------
        location : str
            location of the database (by extension, a location where
            downloaded files are going to be saved by default
        """
        self.items: List[Item] = []
        self.location = location

        if not os.path.isdir(self.location):
            os.mkdir(location)

        self._load_music()

    def add(self, url: str, path: str = '', name: str = ''):
        """
        Downloads song from given url, and saves it to the database.

        Parameters
        ----------
        url : str
            url of the song that needs to be downloaded
        path : str
            path to the directory in which song should be saved, when it's
            not an empty string, it overrides default database location
        name : str
            custom name for downloaded song, a song will be saved under
            that name

        Raises
        ------
        A custom exception that is used in the main program as an error message
        and prevents the whole program from crashing.
        """
        try:
            if 'youtube.com' in url or 'youtu.be' in url:
                self._add_music_yt(url, path, name)
            else:
                self._add_music(url, path, name)
        except:
            raise Exception(f'Error. Could not download a file.')

    def _load_music(self):
        """
        Loads music from the database `location` into database `items` attribute.

        Raises
        ------
        A custom exception that is used in the main program as an error message
        and prevents the whole program from crashing.
        """
        try:
            self.items = []
            content = os.listdir(self.location)

            for x in content:
                self.items.append(Item(self.location, x, os.path.isdir(f'{self.location}{x}')))
        except:
            raise Exception(f'Error. Could not load music data.')

    def _add_music(self, url: str, path: str = '', name: str = ''):
        """
        Adds music from the non youtube url to the database.

        Parameters
        ----------
        url : str
            url of the song that needs to be downloaded
        path : str
            path to the directory in which song should be saved, when it's
            not an empty string, it overrides default database location
        name : str
            custom name for downloaded song, a song will be saved under
            that name

        Raises
        ------
        A custom exception that is used in the main program as an error message
        and prevents the whole program from crashing.
        """
        try:
            p = path if path != '' else self.location
            item = None

            if p[-1] != '/':
                p += '/'

            res = requests.get(url)

            if res.status_code != 200 or 'audio' not in res.headers['Content-Type']:
                raise Exception(f'Error. Could not download a file.')

            if name == '':
                item = Item(p, self._get_name(res.headers), False)
            else:
                item = Item(p, f'{name}.mp3', False)

            with open(f'{p}{item.name}', 'wb') as f:
                f.write(res.content)
                f.close()

            self._load_music()
        except:
            raise Exception(f'Error. Could not download a file.')

    def _add_music_yt(self, url: str, path: str = '', name: str = ''):
        """
        Adds music from the youtube url to the database.

        Parameters
        ----------
        url : str
            url of the song that needs to be downloaded
        path : str
            path to the directory in which song should be saved, when it's
            not an empty string, it overrides default database location
        name : str
            custom name for downloaded song, a song will be saved under
            that name

        Raises
        ------
        A custom exception that is used in the main program as an error message
        and prevents the whole program from crashing.
        """
        try:
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'quiet': True
            }
            video_info = yt_dlp.YoutubeDL(options).extract_info(url=url, download=False)
            p = path if path != '' else self.location

            if 'entries' in video_info:
                directory = name if name != '' else video_info['title']
                count = 1

                if directory[-1] != '/':
                    directory += '/'

                for e in video_info['entries']:
                    options['outtmpl'] = f'{p}{directory}{count}. {e["title"]}'
                    yt_dlp.YoutubeDL(options).download([video_info['webpage_url']])
                    count += 1
            else:
                n = name if name != '' else video_info['title']

                if '.mp3' not in n:
                    n += '.mp3'

                options['outtmpl'] =  f'{p}{n}'
                yt_dlp.YoutubeDL(options).download([video_info['webpage_url']])

            self._load_music()
        except:
            raise Exception(f'Error. Could not download file.')

    def _get_name(self, headers: Dict[str, str]) -> str:
        """
        Gets music file name from the requests headers.

        Parameters
        ----------
        headers : Dict[str, str]
            a dictionary of http headers

        Returns
        -------
        A name of the song. 
        """
        try:
            return headers['Content-Disposition'].split('filename=')[1].replace('"', '')
        except:
            return f''
