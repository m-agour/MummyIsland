# from OpenGL.GLUT import *
from OpenGL.GLU import *
# from OpenGL.GL import *
# from time import time
from math import sin, cos, radians
from libs.vector import Vec3
from libs.misc import *


class Camera:
    def __init__(self):
        self.jaw = -90
        self.pitch = 0
        self.cam_pos = Vec3(32.0, 0, 32.0)
        self.cam_fr = Vec3(0.0, 0.0, -1.0)
        self.cam_up = Vec3(0.0, 1.0, 0.0)
        self.cam_ri = Vec3(1.0, 0.0, 0.0)
        self.mouse_sensitivity = 0.09
        self.firstMovement = True
        self.left, self.forward, self.right, self.backward = False, False, False, False
        self.lastX, lastY = 500 / 2, 500 / 2
        self.xOffset, self.yOffset = 0, 0
        self.lastX, self.lastY = 500 / 2, 500 / 2



    def callPerspective(self):
        glLoadIdentity()
        gluLookAt(*self.cam_pos.tuple(), *(self.cam_pos + self.cam_fr/1000).tuple(), *self.cam_up.tuple())


    def updateCameraV(self):
        front = Vec3(0, 0, 0)

        # xzLen = cos(radians(self.pitch))
        # front.x = xzLen * cos(radians(self.jaw))
        # front.y = sin(radians(self.pitch))
        # front.z = xzLen * sin(radians(-self.jaw))

        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.cam_fr = front.normalize()
        self.cam_ri = (self.cam_fr ** Vec3(0.0, 1.0, 0.0)).normalize()
        self.cam_up = (self.cam_ri ** self.cam_fr).normalize()



    def processMouseMotion(self, c_p=True):

        self.xOffset *= self.mouse_sensitivity
        self.yOffset *= self.mouse_sensitivity
        self.jaw += self.xOffset
        self.pitch += self.yOffset

        if c_p:
            if self.pitch > 90:
                self.pitch = 90
            if self.pitch < -90:
                self.pitch = -90
        self.updateCameraV()

