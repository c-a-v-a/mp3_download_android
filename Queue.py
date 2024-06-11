from os import listdir
import yt_dlp

from MusicItems import OfflineItem, OnlineItem

class OfflineQueue:
    def __init__(self, item: OfflineItem):
        self.songs = []
        self.position = -1

        if item.is_album:
            items = listdir(f'{item.location}{item.name}')
            items.sort()

            for i in items:
                self.songs.append(f'{item.location}{item.name}/{i}')
        else:
            self.songs.append(f'{item.location}{item.name}')

    def get_next(self):
        self.position += 1

        if self.position > self.songs.length:
            self.position = 0

        return self.songs[self.position]

class OnlineQueue:
    def __init__(self, item: OnlineItem):
        self.songs = []
        self.position = -1

        if item.is_album:
            # can be album only for youtube item
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'quiet': True
            }
            items = [];
            info = yt_dlp.YoutubeDL(options).extract_info(url=item.url, download=False)

            for x in info['entries']:
                self.songs.append({'title': x['title'], 'url': x['webpage_url']})
        else:
            self.songs.append({'title': item.title, 'url': item.url})

    def get_next(self):
        self.position += 1

        if self.position > self.songs.length:
            self.position = 0

        return self.songs[self.position]
