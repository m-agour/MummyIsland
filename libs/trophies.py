from libs.ObjLoader import *
from libs.vector import Vec3
from OpenGL.GLUT import *
import pygame


class Trophy:
    def __init__(self, path, pos):
        self.pos = Vec3(*pos)
        self.posTuple = self.pos.tuple()
        self.taken = False


class Ammo(Trophy):
    obj = OBJ("assets/obj/Trophies/ammo/AMMO.obj")

    def __init__(self, path, pos):
        Trophy.__init__(self, path, pos)
        self.sound = pygame.mixer.Sound("assets/sounds/player/max-ammo.ogg")


    def checkIfReward(self, player):
        if player.getLegPos().distance(self.pos) < 3:
            player.gun.ammo = player.gun.maxAmmo
            player.gun.loadedBullets = 6
            self.taken = True
            self.sound.play()

    def draw(self):
        glPushMatrix()
        glTranslate(*self.posTuple)
        glRotate(0.05*glutGet(GLUT_ELAPSED_TIME), 0, 1, 0)
        glScale(5, 5, 5)
        glEnable(GL_TEXTURE_2D)
        glCallList(self.obj.gl_list)
        glPopMatrix()

    def loop(self, player):
        if not self.taken:
            self.checkIfReward(player)
            self.draw()
