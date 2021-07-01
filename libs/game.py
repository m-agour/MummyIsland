from libs.Texture import loadTexture
from libs.terrain import Terrain
from libs.player import Player
from libs.skybox import Skybox
from libs.enemy import Enemy
from libs.vector import *
from libs.animated import *
from libs.saveGame import *
from libs.sound import *
# from libs.shader import *
from libs.trophies import Ammo
from math import inf
from random import randrange as rg
from math import sin
import pygame
# from PIL import Image

class Game:

    terrain = Terrain("assets/textures/heightmap/alien256.png", "assets/textures/ground/sand.jpg")
    shotTraces = []
    firstFrame = True
    initSave = []
    player = Player(terrain)
    sky = Skybox(player.camera, "assets/textures/skybox/skybox1day/")
    
    x, y, z, p, d = 0, 0, 0, 0, 0
    Enemy.health = 120
    enemies = []
    trophies = []
    crows = []
    lastEightChars = ["a" for i in range(8)]
    message = {"start": -100, "message": ""}
    modifiers = {"CTRL": False, "SHIFT": False, "ALT": False, 'L': False, 'F1': False, 'F2': False}

    # Enemy
    enemyTexture = loadTexture("assets/textures/other/metal.jpg")
    enemyDyingSound = SoundSeries("assets/sounds/enemy", 17, 0.6, True)
    cheatSound = Sound("assets/sounds/player/allhail.ogg")



    # background sounds
    horror = pygame.mixer.Sound("assets/sounds/horror.ogg")
    horror.set_volume(0.3)
    horror.play(-1)




    playerRect = pygame.Rect(0, 0, 0, 0)
    
    for i in range(10):
        enemies.append(Enemy(player, enemyTexture, enemyDyingSound, terrain.getRandomPlace()))
    for i in range(10):
        trophies.append(Ammo("assets/AMMO.obj", terrain.getRandomPlace(0.05)))

    for i in range(200):
        center = rg(0, terrain.height), rg(0, terrain.width)
        r = rg(100, 200)/10
        speed = rg(1, 4)/10
        height = terrain.getHeight(*center) + rg(60, 150)/10
        crows.append(Crow(center, r, height, speed))


    def saveGame(self):
        self.initSave = saveAll(self)

    def loadGame(self):
        loadAll(self, self.initSave)

    def cheatCodes(self):
        lastEightChars = "".join(self.lastEightChars)
        # print(lastEightKeys)
        if lastEightChars[8 - 7:] == "hackmag":
            self.player.gun.loadedBullets = inf
            self.cheatSound.play()
            self._afterCheat("No Reload Cheat Activated")

        if lastEightChars[8 - 4:] == "maxa":
            self.player.gun.ammo = inf
            self.cheatSound.play()
            self._afterCheat("Infinity Ammo Cheat Activated")

        if lastEightChars[8 - 5:] == "flash":
            self.player.walkSpeed *= 3
            self.player.runSpeed *= 3
            self.cheatSound.play()
            self._afterCheat("Speed Cheat Activated")

        if lastEightChars[8 - 6:] == "rocket":
            self.player.gravity = 0
            self.cheatSound.play()
            self._afterCheat("Zero Gravity Cheat Activated")

        if lastEightChars == "slamdunk":
            self.cheatSound.play()
            self.player.jumpPower *= 5
            self._afterCheat("High Jump Cheat Activated")

        if lastEightChars == "neverdie":
            self.cheatSound.play()
            self.player.health = inf
            self._afterCheat("Infinity Health Activated")

        if lastEightChars[:] == "massacre":
            for i in self.enemies:
                self.enemyDyingSound.play()
                i.dead = True
                i.player.kills += 1
                i.dyingSounds.play(1 / 6)
                i.currentAnimation = "death"
                i.animation["death"].animate()
            self._afterCheat("All Enemies are killed")





        if lastEightChars[8 - 5:] == "reset":
            self.player.jumpPower = 2.7 * self.player.sScale / self.player.tScale
            self.player.gravity = 9.8 * self.player.sScale / self.player.tScale ** 2
            self.player.gun.loadedBullets = 6
            self.player.gun.ammo = 12
            self.player.walkSpeed = 3 * self.player.sScale / self.player.tScale
            self.player.runSpeed = 7 * self.player.sScale / self.player.tScale
            self._afterCheat("Defaults Restored")

    def _afterCheat(self, message):
        # miss up stack
        self.lastEightChars.append("/")
        self.lastEightChars.pop(0)
        # cheat time
        self.message["start"] = glutGet(GLUT_ELAPSED_TIME)
        self.message["message"] = message

    def addTrophy(self, pos):
        self.trophies.append(Ammo("assets/AMMO.obj", pos))

    def loop(self):

        self.playerRect.center = self.player.camera.cam_pos.x, self.player.camera.cam_pos.z
        # print(self.p, self.x, self.y, self.z, self.d)
        player = self.player.camera.cam_pos
        center = (21, 0, 21)
        w = 5.367
        h = 6.8307
        width = w * (h-player.y + 1.5 + self.player.height)/h
        dir = self.player.camera.cam_fr
        r = 0.15
        if center[0] + width + r > player.x > center[0] - width - r and center[2] + width + r > player.z > center[2] - width - r:

            norm = self.player.camera.cam_pos - Vec3(center[0], 0, center[2])
            if abs(norm.x) > abs(norm.z):
                if norm.x > 0:
                    norm = Vec3(1, 0, 0)
                else:
                    norm = Vec3(-1, 0, 0)
            else:
                if norm.z > 0:
                    norm = Vec3(0, 0, 1)
                else:
                    norm = Vec3(0, 0, -1)

            temp = norm ** dir
            self.player.camera.cam_pos -= dir * self.player.currentSpeed
            self.player.camera.cam_pos += (temp ** norm).normalize() * self.player.currentSpeed

            if self.player.left and not self.player.right:
                if center[0] + width + r > player.x > center[0] - width - r and center[2] + width + r > player.z > center[2] - width - r:
                    self.player.camera.cam_pos += (norm + ((temp ** norm) - dir)).normalize() * self.player.currentSpeed

            elif not self.player.left and self.player.right:
                if center[0] + width + r > player.x > center[0] - width - r and center[2] + width + r > player.z > center[2] - width - r:
                    self.player.camera.cam_pos += (norm + ((temp ** norm) - dir)).normalize() * self.player.currentSpeed
  

        # f1 to save
        if self.modifiers['F1']:
            self.saveGame()
            self.firstFrame = False
        # ctrl+l to load
        if not self.player.alive or self.modifiers['F2']:
            self._afterCheat("You Died!")
            self.loadGame()
            self.player.lives -= 1
            self.saveGame()


        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(0, self.terrain.getSeaLevel(), 0)
        glEnable(GL_TEXTURE_2D)

        self.sky.water()

        t = glutGet(GLUT_ELAPSED_TIME)
        glPopMatrix()

        # crows loop
        for i in self.crows:
            i.render()


        # we sort according to distance from player so that the closest enemy gets the shot
        self.enemies.sort(key=lambda i: i.distanceToPlayer())

        enemyLen = len(self.enemies)

        for i in range(enemyLen - 1):
            for j in range(i + 1, enemyLen):
                # collision here affects both enemies
                self.enemies[i].collisionWithOtherEnemy(self.enemies[j])
        for i in self.enemies:
            i.Draw()





        glPushMatrix()
        glTranslate(0, 0, 0)
        for trophy in self.trophies:
            trophy.loop(self.player)
        glPopMatrix()

        # terrain.Draw()
        glPushMatrix()
        glEnable(GL_COLOR_MATERIAL)
        glCallList(self.terrain.gl_list)
        glEnable(GL_TEXTURE_2D)
        glTranslate(32.0, self.player.terrain.interpolateHeight(32, 32), 32.0)
        glPopMatrix()
        
        glPushMatrix()
        self.player.loop()
        self.cheatCodes()
        glPopMatrix()
        
        for i in self.enemies:
            i.loop(self)


        # reset player shooting
        rd = self.player.gun.shootingDir
        rp = self.player.camera.cam_pos
        if self.player.gun.shooting:
            done = False
            for i in range(int(rp.x)-6, int(rp.x)+6):
                for j in range(int(rp.z)-6, int(rp.z)+6):
                    if 0 > i > self.terrain.width - 2 or 0 > j > self.terrain.height - 2:
                        continue
                    pp = Vec3(i, self.terrain.heights[i][j], j)
                    pn = self.terrain.planeNormals[i][j]
                    inP = checkLinePlaneCollision(pn[0], pp, rd, rp)
                    if inP:
                        if firstTri(inP.x, inP.z, pp.x, pp.z):
                            pn = pn[0]
                        else:
                            inP.y = self.terrain.getRightPos(inP.x, inP.z)
                            inP = LinePlaneCollision(pn[1], inP, rd, rp)
                            pn = pn[1]


                        inP.y = self.terrain.getRightPos(inP.x, inP.z)
                        self.shotTraces.insert(0, ShotTrace(pn, inP))
                        if len(self.shotTraces) > 500:
                            self.shotTraces.pop()
                        self.player.gun.shooting = False
                        done = True
                        break
                if done:
                    break
        self.player.gun.shooting = False

    def waterFog(self):

        if self.player.camera.cam_pos.y > 0.3:
            glFogf(GL_FOG_DENSITY, 0.03)
            fogColour = [0.5, 0.5, 0.5, 0.2]
            glFogfv(GL_FOG_COLOR, fogColour)
        else:
            glFogf(GL_FOG_DENSITY, 100)
            fogColour = [0.0, 0.4, 0.9, 0.2]
            glFogfv(GL_FOG_COLOR, fogColour)

