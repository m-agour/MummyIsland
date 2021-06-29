from math import *
from time import time

from OpenGL.GL import *
# from OpenGL.GLU import *
from OpenGL.GLUT import *
from libs.font import *
from libs.vector import *
from libs.settings import *

class ShotTrace:
    tex = loadTexture("assets/textures/ground/gnd.png", alpha=True)

    def __init__(self, normal, pos):

        # self.pos = pos + normal/1000
        self.pos = pos
        self.pos.y += 0.001
        self.opacity = 1
        self.gl_List = glGenLists(1)
        self.normal = normal
        w = 0.09

        glNewList(self.gl_List, GL_COMPILE)
        glEnable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1)
        glVertex3f(w, 0, w)
        glTexCoord2f(0, 1)
        glVertex3f(-w, 0, w)
        glTexCoord2f(0, 0)
        glVertex3f(-w, 0, -w)
        glTexCoord2f(1, 0)
        glVertex3f(w, 0, -w)
        glEnd()
        glEndList()
        glDisable(GL_BLEND)

    def draw(self):

        glPushMatrix()
        glTranslate(*self.pos.tuple())
        glRotatef(*rotationMatrix(self.normal))
        glColor4f(1, 1, 1, self.opacity)
        glCallList(self.gl_List)
        glPopMatrix()
        glColor4f(1, 1, 1, 1)


class Misc:

    def __init__(self):
        self.gl_list = glGenLists(1)
        self.Prepare()
        self.width = glutGet(GLUT_SCREEN_HEIGHT)
        self.width = glutGet(GLUT_SCREEN_WIDTH)

    def drawCursoe(self):
        glColor3d(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        glVertex3d(0, 0, -.1)
        glEnd()

    def drawSkyBox(self):
        glColor3d(1.0, 1.0, 1.0)
        glutSolidSphere(50, 100, 100)

    def Prepare(self):
        glNewList(self.gl_list, GL_COMPILE)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glPushAttrib(GL_CURRENT_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        self.drawSkyBox()

        glPopAttrib()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glPushAttrib(GL_CURRENT_BIT)
        glLoadIdentity()

        self.drawCursoe()

        glPopAttrib()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEndList()


fnt = Font("assets/font/MUMMY.png", "assets/font/MUMMY.fnt")
point = loadTexture("assets/textures/onscreen/crosshair_default.png", alpha=True)
scoreBoard = loadTexture("assets/textures/onscreen/ammo_bg.png", alpha=True)
heart = loadTexture("assets/textures/onscreen/heart.png", alpha=True)
bloodBar = loadTexture("assets/textures/onscreen/bloodBar.jpg", alpha=True)
shoot = TexSeries("assets/textures/gun", alpha=True)


def drawRect(w=ratio, h=1.0):
    glBegin(GL_QUADS)
    glTexCoord2f(1, 1)
    glVertex2d( w / ratio,  h)
    glTexCoord2f(0, 1)
    glVertex2d(-w / ratio,  h)
    glTexCoord2f(0, 0)
    glVertex2d(-w / ratio, -h)
    glTexCoord2f(1, 0)
    glVertex2d( w / ratio, -h)
    glEnd()

def draw_health_bar(health):
    # health bar
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor(1, 1, 1)

    glBindTexture(GL_TEXTURE_2D, bloodBar)
    drawRectBounded(-0.5, -0.5 + health, 0.03, health)
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor4f(1, 1, 1, 0.3)
    drawRect(0.5, 0.0307)
    glDisable(GL_BLEND)
def drawHorizontalRect(w=ratio, h=1.0):
    glBegin(GL_QUADS)
    glTexCoord2f(1, 1)
    glVertex3f( w / ratio, 0,  h)
    glTexCoord2f(0, 1)
    glVertex3f(-w / ratio, 0,  h)
    glTexCoord2f(0, 0)
    glVertex3f(-w / ratio, 0, -h)
    glTexCoord2f(1, 0)
    glVertex3f( w / ratio, 0, -h)
    glEnd()

def drawRectBounded(x1, x2, h, texX2):
    glBegin(GL_QUADS)
    glTexCoord2f(texX2, 1)
    glVertex2d(x2 / ratio,  h)
    glTexCoord2f(0, 1)
    glVertex2d(x1 / ratio,  h)
    glTexCoord2f(0, 0)
    glVertex2d(x1 / ratio, -h)
    glTexCoord2f(texX2, 0)
    glVertex2d(x2 / ratio, -h)
    glEnd()

def drawOnScreen(game, x, y, z):
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    for i in game.shotTraces:
        # i.opacity -= 0.001
        # i.opacity -= 0.001 / i.opacity ** 2
        if i.opacity <= 0:
            game.shotTraces.remove(i)
            continue
        i.draw()
    glPushMatrix()
    glLoadIdentity()
    # point
    if not game.player.inWater():
        # get color to revert it
        # color = glReadPixels(0, 0, 1, 1, GL_RGB, GL_FLOAT)[0][0]
        # brightness = (299 * R + 587 * G + 114 * B) / 1000
        # c = 1 - sum(color)/3
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_BLEND)
        # c = 0.7, 0.0, 0.0
        c = 1, 1, 1
        glColor(*c, 1)
        glBindTexture(GL_TEXTURE_2D, point)
        glScale(0.27, 0.27, 0.27)
        drawRect(0.1, 0.1)
        glDisable(GL_BLEND)

        glLoadIdentity()
        health = game.player.health
        glTranslate(0, 0.91, 0)
        draw_health_bar(health/100)

        glLoadIdentity()
        glColor(0.8, 0.8, 0.8, 1)
        glTranslate(-0.9, 0.9, 0)
        for i in range(game.player.lives):
            # print(game.player.lives)
            glEnable(GL_BLEND)
            glBindTexture(GL_TEXTURE_2D, heart)
            drawRect(0.05, 0.05)
            glDisable(GL_BLEND)
            glTranslate(0.06, 0, 0)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        if game.player.gun.muzzle.playing:
            glEnable(GL_BLEND)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glColor(1, 1, 1)
            glBindTexture(GL_TEXTURE_2D, game.player.gun.muzzle.getNextFrame())
            # glScale(game.p + 1.72, game.p + 1.72, game.p + 1.72)
            # glTranslate(game.x + 0.24, game.y-0.14, game.z)
            glScale(1.30999 + game.p, 1.30999 + game.p, 1.30999 + game.p)
            glTranslate(0.28 -0.035, -0.14 -0.016, 0.07999  -0.014)
            # print(0.28 + game.x, -0.14 + game.y, 0.07999 + game.z, 1.30999 + game.p)
            drawRect(0.2, 0.2)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glDisable(GL_BLEND)

    # score
    ammo = game.player.gun.ammo # if game.player.gun.ammo != inf else chr(8734)

    color = (1, 0.1, 0.1, 0.8) if ammo == 0 else (1, 1, 1, 0.8)
    drawText("{}".format(game.player.gun.loadedBullets).upper(), 0.875, -0.9, ratio, color, 2.5)
    drawText("{}".format(ammo).upper(), 0.93, -0.865, ratio, color, 1.5)

    # lives
    glLoadIdentity()
    glTranslate(0, 0, 0)
    drawText("{}".format(int(game.player.kills)).upper(), 0.83, 0.86, ratio, (0.8, 0, 0, 1), 1.7)

    if glutGet(GLUT_ELAPSED_TIME) - game.message["start"] < 3000:
        text = game.message["message"]
        drawText(text, 0-len(text)/90, -0.95, ratio, (1, 0.2, 0.2, 1), 2, projection=True)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()



def moveWithPlayer():
    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glPushAttrib(GL_CURRENT_BIT)
    glLoadIdentity()
    glutSolidSphere(50, 10, 10)
    glPopAttrib()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEndList()
    return gl_list


def drawText(text, x, y, wh, color=(0, 0, 0, 1), scale=1.0, projection=True):

    if projection:
        default_scale = .2 * scale
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glTranslate(x, y, 0)
        glScalef(default_scale, default_scale * wh, 1.0)

    else:
        default_scale = 0.0002 * scale
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glScalef(default_scale, default_scale * wh, 1.0)
        glTranslate(x, y, 0)

    # glLineWidth(line)
    glColor4f(*color)
    fnt.draw(text)
    # glutStrokeString(GLUT_STROKE_MONO_ROMAN, bytes(text, 'utf-8'))
    # glColor4f(1.0, 1.0, 1.0, 1.0)
    glPopMatrix()
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
