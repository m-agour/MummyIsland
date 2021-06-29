from OpenGL.GL import *
import pygame
import os
from random import shuffle

def loadTexture(path , skybox = False, alpha = False):
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    imgF = ('RGB', GL_RGB) if not alpha else ('RGBA', GL_RGBA)
    if skybox:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    else:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, 4.0)
    image = pygame.image.load(path)
    image = pygame.transform.flip(image, False, True)
    image_width, image_height = image.get_rect().size
    img_data = pygame.image.tostring(image, imgF[0])
    glTexImage2D(GL_TEXTURE_2D, 0, imgF[1], image_width, image_height, 0, imgF[1], GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return tex


class TexSeries:
    def __init__(self, path, speed=1, alpha=False):
        self.frames = []
        self.speed = speed
        self.currentFrame = 0
        self.playing = False
        self._loadFrames(path, alpha)

    def _loadFrames(self, path, alpha):
        x = [os.path.abspath(os.path.join(path, p)) for p in os.listdir(path)]
        for i in x:
            self.frames.append(loadTexture(i, alpha=alpha))

    def start(self, shuffled=False):
        if shuffled:
            shuffle(self.frames)
        self.playing = True

    def getNextFrame(self, loop=False):
        if self.playing or loop:
            tmp = self.frames[int(self.currentFrame)]
            self.currentFrame += self.speed
            if self.currentFrame >= len(self.frames):
                self.currentFrame = 0
                if not loop:
                    self.playing = False

            return tmp
        else:
            return self.frames[0]


