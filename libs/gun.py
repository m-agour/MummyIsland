# from OpenGL.GLUT import *
# from OpenGL.GL import *
import pygame
# from time import time
from math import inf
from libs.misc import *
from libs.animated import *
from libs.sound import *
from libs.Texture import *

class Gun:
    def __init__(self, damage):
        self.damage = damage
        self.ammo = 12
        self.maxAmmo = 12
        self.loadedBullets = 6
        self.ouOfAmmo = False
        self.shootingDir = None
        self.prevShotTime = 0
        self.restTime = 0.2
        self.shooting = False
        self.shootingSoundTime = 0.5
        self.reloading = False
        self.forceReload = False
        self.reloadingTime = 1.8
        self.reloadingStartTime = 0
        self.recoilStrength = 2
        self.recoiling = False
        self.recoilStartTime = 0
        self.sounds = {}
        self.animation = getGunAnimations()
        self.muzzle = TexSeries("assets/obj/player/weapon/muzzle/", alpha=True, speed=2.5)
        self.loadSounds()

    def loadSounds(self):
        self.sounds["shot"] = Sound("assets/sounds/gun/shot.ogg", 0.3)
        self.sounds["reload"] = Sound("assets/sounds/gun/reload.ogg", 0.3)
        self.sounds["empty"] = Sound("assets/sounds/gun/empty.ogg", 0.3)


    def canShoot(self):
        if self.loadedBullets != 0:
            return True
        else:
            return False

    def shoot(self, direction):
        if not self.reloading:
            currTime = glutGet(GLUT_ELAPSED_TIME)
            timeBetweenShots = currTime - self.prevShotTime
            # print(timeBetweenShots / 1000, currTime, self.prevShotTime)
            if timeBetweenShots / 1000 >= self.restTime:
                if self.canShoot():
                    self.shooting = True
                    self.prevShotTime = glutGet(GLUT_ELAPSED_TIME)
                    self.shootingDir = direction
                    self.loadedBullets -= 1
                    self.sounds["shot"].play(overlap=True)
                    # muzzle
                    self.muzzle.start()
                    self.animation["shoot"].animate()
                    # shoot.start()

                    return True
                else:
                    self.sounds["empty"].play()
                    return False

    def reload(self):
        if not self.reloading and (self.loadedBullets == 0 or self.forceReload) and self.ammo != 0 and not self.animation["shoot"].isPlaying():
            self.sounds["reload"].play()
            self.reloading = True
            self.animation["reload"].animate()
            self.reloadingStartTime = glutGet(GLUT_ELAPSED_TIME)

        if self.reloading:
            elapsedTime = (glutGet(GLUT_ELAPSED_TIME) - self.reloadingStartTime) / 1000
            if elapsedTime > self.reloadingTime * 0.9:
                self.ammo += self.loadedBullets
                if self.ammo >= 6:
                    self.loadedBullets = 6
                    self.ammo -= 6
                elif self.ammo == inf:
                    self.loadedBullets = 6
                else:
                    self.loadedBullets = self.ammo
                    self.ammo = 0

            if elapsedTime > self.reloadingTime:
                self.reloading = False
