import glob
from libs.ObjLoader import *
from zipfile import *
from time import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from random import randrange as rg
from libs.vector import Vec3, Vec2
from libs.Texture import *
from libs.sound import *
from libs.misc import *
import lzma
import threading

try:
    import ujson as json
except:
    import json

# loading = TexSeries("assets\\textures\\loading", 0.007)


class Animation:
    def __init__(self, frames, step=1, speed=1.0, reverse=False, loop=False, randomIndex=False, defaultFrame=0):
        self.frames = frames
        if reverse:
            self.reverseAnimation()
        self.length = len(self.frames)
        if randomIndex:
            self.index = rg(0, self.length)
        else:
            self.index = 0
        self.is_detected = False
        self.playing = False
        self.speed = speed / step
        self.step = step
        self.loop = loop

    def reverseAnimation(self):
        self.frames.reverse()

    def getCurrentFrame(self):
        return self.frames[int(self.index)]

    def getNextFrame(self):
        # get next frame
        if self.playing or self.loop:
            self.index += self.speed
            if self.index >= self.length:
                self.index = 0
                if not self.loop:
                    self.playing = False
                    return self.frames[-1]
            return self.frames[int(self.index)]
        else:
            # self.index = 0
            return self.frames[-1]


    def getFirstFrame(self):
        return self.frames[0]

    def animate(self):
        self.playing = True

    def isPlaying(self):
        return self.playing

    def isLastFrame(self):
        return self.index + self.speed >= len(self.frames)

    def isFirstFrame(self):
        return self.index == 0

    def reset(self):
        self.index = 0
        self.playing = False


def loadPak(pakFile, step=1):
    frames = []
    # load frames from directory
    # load first material
    texFile = os.path.join(os.path.dirname(pakFile), "textures.tan")
    mtl = {}

    with open(texFile) as file:
        tex = json.loads(file.read())
        for i in tex.keys():
            mtl[i] = loadTexture(tex[i], alpha=True)

    with ZipFile(pakFile, "r") as z:
        with z.open("animation") as file:
            Dict = json.load(file)
            for frame in range(0, len(Dict), step):
                frames.append(_loadFrame(Dict[frame], mtl))

    print("Pak animation file loaded!")
    return frames


def _loadFrame(Dict, mtl):
    # Dict contains vertices, normals, texCoords, and faces

    # prepare gl_list
    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glPushMatrix()
    t = time()
    glBindTexture(GL_TEXTURE_2D, list(mtl.values())[0])
    glBegin(GL_TRIANGLES)
    for face in Dict["faces"]:
        for i in range(len(face[0])):
            glNormal3f(*Dict["normals"][face[1][i] - 1])
            glTexCoord2f(*Dict["texCoords"][face[2][i] - 1])
            glVertex3f(*Dict["vertices"][face[0][i] - 1])
    glEnd()
    # print(time() - t)
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopMatrix()
    glEndList()
    return gl_list


def loadPackOfPak(path, step=1):
    clips = {}
    pakFiles = [file for file in os.listdir(path) if file.endswith('.pak')]
    for i in pakFiles:
        t = time()
        clips[i.replace(".pak", "")] = loadPak(os.path.join(path, i), step=step)
        print(time() - t)
    return clips


def loadingRect():
    glBindTexture(GL_TEXTURE_2D, loading.getNextFrame())
    drawRect(1, 1)


# mummy and gun animation global variables
mummyAnimations = loadPackOfPak("assets/obj/enemy/mummy/lowpoly/", step=1)
gunAnimations = loadPackOfPak("assets/obj/player/weapon/", step=1)

# def loadGameAnimations():
#     global mummyAnimations, gunAnimations
#     mummyAnimations =
#     gunAnimations = loadPackOfPak("assets/obj/player/weapon/", step=1)


def getMummyAnimations():
    temp = {}
    for i in mummyAnimations.keys():
        if i in ["walk", "attack", "walkAttack"]:
            tmp = True
        else:
            tmp = False
        temp[i] = Animation(mummyAnimations[i], step=1, speed=0.5, loop=tmp, randomIndex=tmp)
    return temp


def getGunAnimations():
    temp = {}
    for i in gunAnimations.keys():
        s = 1

        temp[i] = Animation(gunAnimations[i], step=1, speed=s)

    temp["hide"] = Animation(gunAnimations["show"][9:0:-1], step=1, speed=1/2)
    return temp


class Crow:
    fly = loadPak("assets/obj/crow/fly3.pak")
    sound = Sound("assets/sounds/crow/CROW.WAV")

    def __init__(self, center, radius, height, speed):
        self.center = center
        self.height = height
        self.radius = radius
        self.speed = speed
        self.clip = Animation(self.fly, speed=0.5, loop=True, randomIndex=True)

    def render(self):
        t = time() * self.speed
        glPushMatrix()
        if self.clip.isFirstFrame() and rg(0, 25) == 2:
            self.sound.play(volume=rg(10, 100) / 1000)
        # t = glutGet(GLUT_ELAPSED_TIME) * self.speed
        x, y = self.radius * sin(t), self.radius * cos(t)
        glTranslate(self.center[0] + x, self.height, self.center[1] + y)
        glScale(0.04, 0.04, 0.04)
        glRotate(180 - degrees(atan2(y, x)), 0, 1, 0)
        # print(time()-t)
        glCallList(self.clip.getNextFrame())
        glPopMatrix()
