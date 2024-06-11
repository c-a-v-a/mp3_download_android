import json
import requests
import yt_dlp
from os import listdir, path
from typing import List, Dict

from MusicItems import OnlineItem, OfflineItem
from Preflight import DATABASE_PATH, MUSIC_LOCATIONS

class Database:
    """Class representing a container for all saved pieces of music.

    Properties:
    online_items -- music that is not saved locally on the device; only its 
    title and url is saved in database file.
    offline_items -- music that is saved locally on the device
    """
    def __init__(self, online_location: str, offline_locations: List[str]):
        self.online_items: List[OnlineItem] = []
        self.offline_items: List[OfflineItem] = []
        self.online_location: str = online_location
        self.offline_locations: List[str] = offline_locations

        self._load_online()
        self._load_offline()

    def save_online(self):
        """Save online_items array into json file on given location"""
        try:
            dicts = list(map(lambda x: x.__dict__, self.online_items))
            file = open(self.online_location, 'w')
            json.dump(dicts, file, indent=4)
            file.close()
        except:
            raise Exception(f'Error. Could not save data.')

    def _load_online(self):
        """Loads saved online music items from specified json file"""
        try:
            file = open(self.online_location, 'r')
            dicts = json.load(file)
            self.online_items = list(map(lambda x: OnlineItem(x), dicts))
            file.close()
        except:
            raise Exception(f'Error. Could not load online music data.')

    def _load_offline(self):
        """Loads saved offline music items from specified locations"""
        try:
            contents = list(map(lambda x: listdir(x), self.offline_locations))
            with_prefix = list(zip(self.offline_locations, contents))

            self.offline_items = []
            
            for x in with_prefix:
                location = x[0]
                names = x[1]

                for name in names:
                    self.offline_items.append(OfflineItem(location, name, path.isdir(f'{location}{name}')))
        except:
            raise Exception(f'Error. Could not load offline music data.')

    def add_offline(self, url: str, path: str = '', name: str = ''):
        """Adds item to offline list. That means that mp3 files are downloaded
        from url and then saved on hard drive in the MUSIC_LOCATIONS[0].
        """
        try:
            p = path
            res = requests.get(url)
            item = None 

            if p == '':
                p = self.offline_locations[0]

            filename = p

            if res.status_code != 200 or 'audio' not in res.headers['Content-Type']:
                raise Exception(f'Error. Could not download file.')
            
            if name == '':
                n = self._get_name(res.headers)
                filename += n
                item = OfflineItem(p, n, False)
            else:
                filename += f'{name}.mp3'
                item = OfflineItem(p, f'{name}.mp3', False)

            with open(filename, 'wb') as f:
                f.write(res.content)
                f.close()

            self.offline_items.append(item)
        except:
            raise Exception(f'Error. Could not download file.')

    def add_online(self, url: str, name: str = ''):
        """Adds items to online list. That means that title is taken from the 
        request metadata (or function parameters), and with the file url, they
        are stored in the database json file.
        """
        try:
            res = requests.get(url)
            item = None 

            if res.status_code != 200 or 'audio' not in res.headers['Content-Type']:
                raise Exception(f'Error. Could not download file.')
            
            if name == '':
                n = self._get_name(res.headers)
                item = OnlineItem({'title': n, 'url': url, 'is_album': 'False'})
            else:
                item = OnlineItem({'title': name, 'url': url, 'is_album': 'False'})

            self.online_items.append(item)
            self.save_online()
        except:
            raise Exception(f'Error. Could not save to database.')

    def add_offline_yt(self, url: str):
        """Function similar to `add_offline`, but it handles only youtube urls"""
        try:
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'quiet': True
            }
            video_info = yt_dlp.YoutubeDL(options).extract_info(url=url, download=False)

            if 'entries' in video_info:
                directory = video_info['title']
                count = 1

                for video in video_info['entries']:
                    title =  f'{self.offline_locations[0]}{directory}/{count}. {video["title"]}'
                    options['outtmpl'] = title + '.mp3'
                    yt_dlp.YoutubeDL(options).download([video_info['webpage_url']])
                    count += 1
            else:
                title = f'{self.offline_locations[0]}{video_info["title"]}'
                options['outtmpl'] = title + '.mp3'
                yt_dlp.YoutubeDL(options).download([video_info['webpage_url']])

            self._load_offline()
        except:
            raise Exception(f'Error. Could not download file.')

    def add_online_yt(self, url: str):
        """Function similar to `add_online`, but it handles only youtube urls"""
        try:
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'quiet': True
            }
            video_info = yt_dlp.YoutubeDL(options).extract_info(url=url, download=False)
            title = video_info['title']
            is_album = 'entries' in video_info

            item = OnlineItem({'title': title, 'url': url, 'is_album': str(is_album)})
            
            self.online_items.append(item)
            self.save_online()
        except:
            raise Exception(f'Error. Could not save to database.')

    def _get_name(self, headers: Dict[str, str]) -> str:
        """Gets song title from request metadata"""
        try:
            return headers['Content-Disposition'].split('filename=')[1].replace('"', '')
        except:
            return f''
