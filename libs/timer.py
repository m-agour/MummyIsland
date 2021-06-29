from OpenGL.GLUT import *


class Timer:
    def __init__(self):
        self.startTime = glutGet(GLUT_ELAPSED_TIME)
        self.tag = ""


    def startFromNow(self):
        self.startTime = glutGet(GLUT_ELAPSED_TIME)


    def getTime(self, tag):
        if tag != self.tag:
            self.tag = tag
            self.startTime = glutGet(GLUT_ELAPSED_TIME)
            return 0
        return glutGet(GLUT_ELAPSED_TIME) - self.startTime


    def setTag(self, tag):
        self.tag = tag


    def getTag(self):
        return self.tag
