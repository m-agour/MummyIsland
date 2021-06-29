# from OpenGL.GLU import *
# from OpenGL.GL import *
# from OpenGL.GLUT import *
from libs.settings import *
import pygame


class Sound:
    def __init__(self, path, volume=1):
        self.sound = pygame.mixer.Sound(path)
        self.volume = volume
        self.sound.set_volume(volume)
        self.length = self.sound.get_length()
        self.playing = False
        self.startPayingTime = 0

    def play(self, volume=None, overlap=False):
        if not self.isPlaying() or overlap:
            if volume:
                self.sound.set_volume(volume)
            self.sound.play()
            self.startPayingTime = glutGet(GLUT_ELAPSED_TIME)

    def stop(self):
        self.sound.stop()
        self.startPayingTime = 0

    def isPlaying(self):
        return glutGet(GLUT_ELAPSED_TIME) - self.startPayingTime <= self.length * 1000


class SoundSeries:
    def __init__(self, path, number,  volume=1, overlap=False):
        self.sounds = []
        self.num = number
        self.overlap = overlap
        self.volume = volume
        self.loadSounds(path)
        self.setVol(volume)

    def loadSounds(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.ogg') or file.endswith('.wav')]

        for i in files:
            self.sounds.append(Sound(i))

    def play(self, volume=None):
        if not self.sounds[0].isPlaying() or self.overlap:
            self.sounds.insert(0, self.sounds.pop())
            self.sounds[0].play(volume)

    def stop(self):
        self.sounds[0].stop()
        self.sounds.insert(0, self.sounds.pop())

    def setVol(self, num):
        for i in self.sounds:
            i.sound.set_volume(num)
