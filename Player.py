import pygame
import requests
from io import BytesIO


class Player:
    """Class representing a music player. Should be used as a singleton,
        since there is only one pygame.mixer object.
    """
    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()
        self.paused = False
        self.loaded = False

    def load_online(self, url: str):
        """Loads online song into music player. Music is loaded from
            url via the requests or yt_dlp library, depending if url
            is a youtube url or not.
        """
        if 'youtube.com' in url or 'youtu.be' in url:
            raise Exception('Error. Youtube playback unsupported.')

        try:
            if self.loaded:
                if not self.paused:
                    self.mixer.music.pause()
                    self.paused = True

                self.loaded = False
                self.paused = False
                self.mixer.music.unload()

            response = requests.get(url)
            file = BytesIO(response.content)
            self.mixer.music.load(file)
            self.loaded = True
        except:
            self.loaded = False
            raise Exception('Error. Could not play this music.')

    def load_offline(self, path: str):
        """Loads online song into music player. The music is loaded by path
            to a downloaded file.
        """
        try:
            if self.loaded:
                if not self.paused:
                    self.mixer.music.pause()
                    self.paused = True

                self.loaded = False
                self.paused = False
                self.mixer.music.unload()

            self.mixer.music.load(path)
            self.loaded = True
        except:
            self.loaded = False
            raise Exception('Error. Could not play this music.')

    def stop(self):
        """Stops the music playback."""
        self.mixer.music.pause();
        self.paused = True

    def start(self):
        """Depending on the Player state either unpauses the Player, or starts
            playing song from the beggining.
        """
        if self.paused:
            self.mixer.music.unpause()
        else:
            self.mixer.music.play()
