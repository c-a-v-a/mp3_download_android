import pygame
import requests
from io import BytesIO


class Player:
    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()
        self.paused = False
        self.loaded = False

    def load_online(self, url: str):
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
        self.mixer.music.pause();
        self.paused = True

    def start(self):
        if self.paused:
            self.mixer.music.unpause()
        else:
            self.mixer.music.play()
