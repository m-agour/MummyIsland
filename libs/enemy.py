import random

from libs.vector import *
from math import atan2, degrees, pi, cos
# from OpenGL.GLU import *
# from OpenGL.GL import *
# from OpenGL.GLUT import *
from libs.settings import *
from libs.ObjLoader import *
from libs.animated import *
import pygame

class Enemy:
    # damage map
    _damageMap = pygame.image.load("assets/textures/damage.jpg")
    damageMapDims = _damageMap.get_size()
    damageArray = []
    for x in range(damageMapDims[1]-1, -1, -1):
        tmp = []
        for y in range(damageMapDims[0]):
            tmp.append(_damageMap.get_at((y, x))[0] / 255)
        damageArray.append(tmp)


    def __init__(self, player, tex, dyingSounds, pos=(0, 0, 0)):
        self.currentAnimation = "walk"
        self.sScale = 1/player.terrain.scale  # space scale
        self.tScale = GAME_FPS  # time scale
        self.overallScale = self.sScale * 3
        self.health = 100
        self.speed = 3 * self.sScale / self.tScale
        self.smellDist = 400 * self.sScale
        self.attackStrength = 20 * 60 / GAME_FPS
        self.sphereR = (0.5 + 0.2)
        self.dead = False
        self.attacking = False
        # self.health = 100
        self.followDir = False
        self.move = False
        self.initialPos = Vec3(*pos)
        self.player = player
        self.pos = (Vec3(*pos), Vec3(*self.player.terrain.getRandomPlace()))[pos == (0, 0, 0)]
        self.front = Vec3(1, 0, 0)
        self.prevPos = self.initialPos
        self.prevAng = 0
        self.impactStart = -1000
        self.dyingSounds = dyingSounds
        self.texture = tex
        self.animation = getMummyAnimations()
        self.headHeight = 2.4 * self.sScale
        self.width = 2.4 * self.sScale / 7


    def angleWithX(self):
        return atan2(self.front.z, self.front.x)

    def dirToPointAngleWithX(self):
        direction = self.vectorToPlayer()
        return atan2(direction.z, direction.x)

    def angleWithPlayer(self):
        dx = self.player.camera.cam_pos.x - self.pos.x
        dy = self.player.camera.cam_pos.z - self.pos.z
        self.front.rotate(-(self.angleWithX() - atan2(dy, dx)))
        return self.angleWithX() - atan2(dy, dx)

    def lookAt(self):
        if self.angleWithX() - self.dirToPointAngleWithX() < -0.1:
            self.front.rotate((self.angleWithX() - self.dirToPointAngleWithX())/50)
        if self.angleWithX() - self.dirToPointAngleWithX() > 0.1:
            self.front.rotate(-(self.angleWithX() - self.dirToPointAngleWithX())/50)


    def attack(self):
        vecToPlayer = self.vectorToPlayer()
        distanceToPlayer = self.distanceToPlayer()
        if distanceToPlayer < self.smellDist:
            # move toward player
            self.front = vecToPlayer
            self.pos += vecToPlayer.normalize() * self.speed
            # start freaking out the player

            if distanceToPlayer < (self.sphereR + self.player.sphereR) * 1.5:
                # check if another animation is playing
                if self.currentAnimation != "attack" and (self.animation[self.currentAnimation].isLastFrame()):
                    self.animation[self.currentAnimation].reset()
                    self.currentAnimation = "attack"

            elif distanceToPlayer <  (self.sphereR + self.player.sphereR)*3:
                if self.currentAnimation != "walkAttack" and (self.animation[self.currentAnimation].isLastFrame()):
                    self.animation[self.currentAnimation].reset()
                    self.currentAnimation = "walkAttack"

            # stop freaking out the player ;(
            else:
                if self.currentAnimation != "walk" and self.animation[self.currentAnimation].isLastFrame():
                    self.animation[self.currentAnimation].reset()
                    self.currentAnimation = "walk"


            # don't attack
            if distanceToPlayer > (self.sphereR + self.player.sphereR)*1.2:
                self.attacking = False

            # attack for real don't just move your hands
            else:
                self.attacking = True
                self.impactStart = time()
                self.player.health -= self.attackStrength / GAME_FPS
                self.player.sounds["damage"].play()

    def _enemyPlayerVec(self):
        playerPos = self.player.getPos().tuple()
        playerLegPos = Vec3(playerPos[0], playerPos[1] - self.headHeight, playerPos[2])
        return playerLegPos - self.pos


    def vectorToPlayer(self):
        return self._enemyPlayerVec().normalize()

    def distanceToPlayer(self):
        return self._enemyPlayerVec().abs()


    def loop(self, game):
        # print(self.pos.tuple())
        # print(sys.getsizeof(self.animation["walk"].frames[0].gl_list))


        if self.dead:
            if not self.animation["death"].isPlaying():
                # gift ammo prop
                if random.randrange(0, 6) == 0:
                    game.addTrophy(self.pos.tuple())
                self.resurrect()
        else:
            self.collisionWithPlayer()
            self.walkOnTerr()
            self.beingShot()
            self.attack()


    def getHeadPos(self):
        return Vec3(self.pos.x, self.pos.y + self.headHeight, self.pos.z)


    def Draw(self):
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.01, 0.01, 0.01))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 0.0, 0.0))
        glPushMatrix()

        glTranslate(self.pos.tuple()[0], self.pos.tuple()[1], self.pos.tuple()[2])
        glScale(self.overallScale, self.overallScale, self.overallScale)


        upV = ((self.front ** Vec3(0, 1, 0)) ** self.front).normalize()
        fr = self.front
        # glRotate(*rotationMatrix(upV, fr))
        # glRotate(degrees(upV.angleWithXZ()), 0, 1, 0)


        glRotate(90-degrees(self.angleWithX()), 0, 1, 0)
        glScale(0.016, 0.016, 0.016)
        # glutSolidTeapot(self.sphereR )

        glCallList(self.animation[self.currentAnimation].getNextFrame())


        vert = [[-0.5, 1.0, -0.5, 0.0, 1.0],
         [0.5, 1.0, -0.5, 1.0, 1.0],
         [0.5, 0, -0.5, 1.0, 0.0],
         [-0.5, 0, -0.5, 0.0, 0.0]]
        # glDisable(GL_BLEND)
        # glEnable(GL_ALPHA_TEST)

        # glBegin(GL_QUADS)
        # t = glutGet(GLUT_ELAPSED_TIME) / 5000
        # for i in vert:
        #     glTexCoord2f(i[3:][0], i[3:][1])
        #     x, y, z = i[:3]
        #     glVertex3f(x , y, z )
        # glEnd()
        # glDisable(GL_ALPHA_TEST)
        # glCallList(self.model.gl_list)
        # glutSolidCube(0.5)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

        glPushMatrix()

        # glTranslate(0, 0, 0)
        # f = self.front.normalize()
        # p = Vec3(self.pos.x, self.pos.y + 0.3, self.pos.z)
        # glBegin(GL_LINES)
        # glColor(1, 0, 0)
        # glVertex3f(*p.tuple())
        # glColor(0, 0, 1)
        # glVertex3f(*(f+p).tuple())
        # glEnd()

        # glTranslate(0, 0, 0)
        # pf = self.player.camera.cam_fr * 5
        # pp = self.player.camera.cam_pos
        # glBegin(GL_LINES)
        # glColor(1, 0, 0)
        # glVertex3f(*pp.tuple())
        # glColor(0, 0, 1)
        # glVertex3f(*(pp ).tuple())
        # glEnd()
        glPopMatrix()

        glColor(1, 1, 1)
        light_position = (1922, 2354, 3391)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.2, 0.2, 0.2))

    def walkOnTerr(self):
        if self.player.terrain.checkIfInRange(self.pos.tuple()):
            self.pos.y = self.player.terrain.heightPlus(self.pos.tuple())

    def beingShot(self):
        if self.player.gun.shooting and not self.dead:
            pv = self.player.camera.cam_pos
            pp = self.pos
            vv = self.player.camera.cam_fr.normalize()
            vp = self.front.normalize()

            # p = pv + vv * ((pp - pv).dot(vp)/(vv.dot(vp)))
            # glPushMatrix()
            # glPointSize(5)
            # glBegin(GL_POINTS)
            # glColor3f(1, 0.5, 0.5)
            # glVertex3f(*p.tuple())
            # glEnd()
            # glPopMatrix()
            #
            # position = self.pos.tuple()
            # front = (self.front.normalize() / 4).tuple()
            # vecToHead = self.player.camera.cam_pos - Vec3(position[0] + front[0], position[1] + self.headHeight, position[2] + front[2])
            # vecToBelly = self.player.camera.cam_pos - Vec3(position[0] + front[0], position[1] + self.headHeight/2, position[2] + front[2])
            #
            # damageHeight = tan(self.player.camera.cam_fr.angleWithXZ() - self.front.angleWithXZ()) * self.distanceToPlayer()
            # print(damageHeight)
            #
            # distFromHeart = abs(self.player.gun.shootingDir.shortestDist(vecToHead))
            # distFromBelly = abs(self.player.gun.shootingDir.shortestDist(vecToBelly))
            # damageY = tan(
            #     self.player.camera.cam_fr.angleWithXZ() + self.front.angleWithXZ()) * self.distanceToPlayer()
            # playerEnemyPlane = self.vectorToPlayer() ** Vec3(0, 1, 0)
            # damageX = abs(tan(self.player.camera.cam_fr.angleWithPlane(playerEnemyPlane)) * self.distanceToPlayer())
            FR = Vec3(self.front.x, 0, self.front.z).normalize()
            shotPos = LinePlaneCollision(FR, self.pos, self.player.camera.cam_fr, self.player.camera.cam_pos)

            relativeInt = shotPos - self.pos
            shotHeight = relativeInt.y
            shotWidth = relativeInt.vec2xz().abs()
            # print(shotWidth, shotHeight)

            # return

            if shotWidth <= 0.15 * self.overallScale and 0 <= shotHeight <= 1.25* self.overallScale:

                damage = self.damageArray[int(shotHeight * (len(self.damageArray)-1)/(1.25* self.overallScale))][int(shotWidth * (len(self.damageArray[0])-1)/(0.15* self.overallScale))]
                # print(damage)
                if damage == 0:
                    return

                self.health -= self.player.gun.damage * damage
                self.player.gun.shooting = False

                if self.health <= 0:
                    self.dead = True
                    self.player.kills += 1
                    self.dyingSounds.play(1 / abs(self.distanceToPlayer()))
                    self.currentAnimation = "death"
                    self.animation["death"].animate()

                else:
                    self.currentAnimation = "hit"
                    self.pos -= self.front/7
                    self.animation["hit"].animate()



            # print(self.player.shootingDir.degree(self.pos - self.player.camera.cam_pos))
            # dirVec = self.vectorToPlayer().normalize()
            # self.player.shootingDir = None


    def collisionWithOtherEnemy(self, enemy):
        vec2enemy = (self.pos - enemy.pos)
        if vec2enemy.abs() < 2 * self.sphereR:
            tmp = vec2enemy.normalize() * self.speed/2
            self.pos += tmp# * cos(enemy.front.angleWith(tmp))
            enemy.pos += tmp# * cos(self.front.angleWith(tmp))
        if vec2enemy.abs() < 2 * self.sphereR:
            tmp = vec2enemy.normalize() * self.speed
            self.pos += tmp# * cos(enemy.front.angleWith(tmp))
            enemy.pos -= tmp# * cos(self.front.angleWith(tmp))

    def collisionWithPlayer(self):
        vec2player = self._enemyPlayerVec()
        if vec2player.abs() < self.sphereR + self.player.sphereR - 0.01:
            tmp = vec2player.normalize()
            if self.player.currentSpeed == 0:
                self.pos -= tmp * self.speed
            else:
                self.pos -= tmp * self.player.currentSpeed
                self.player.camera.cam_pos += tmp * self.speed


    def resurrect(self):
        self.health = 100
        self.dead = False
        self.pos = Vec3(*self.player.terrain.getRandomPlace())
        self.currentAnimation = "walk"
