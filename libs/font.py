from libs.Texture import *
from OpenGL.GLUT import *


class Font:
    def __init__(self, png, fnt):
        self.letters = {}
        self.tex = loadTexture(png, alpha=True)
        self.width, self.height = pygame.image.load(png).get_rect().size
        self.data = self._readFile(open(fnt, "r").readlines())

    def _readFile(self, fontFile):
        data = fontFile
        tmp = {}
        for i in data:
            if i[:5] != "char ":
                continue
            tmp2 = {}
            for i in i.split(" "):
                if i not in ['', "\n"] and "=" in i:
                    tmp3 = i.split("=")
                    tmp2[tmp3[0]] = int(tmp3[1])

            tmp2["x"] /= self.width
            tmp2["y"] = 1 - tmp2["y"] / self.height
            tmp2["width"] /= self.width
            tmp2["height"] /= self.height

            tmp[chr(tmp2["id"])] = tmp2
            # print(chr(tmp2["id"]))
        return tmp

    def draw(self, string):
        off = 0
        glEnable(GL_BLEND)
        glDepthFunc(GL_ALWAYS)
        for i in string:

            glTranslate(off, 0, 0)
            glBindTexture(GL_TEXTURE_2D, self.tex)
            glBegin(GL_QUADS)
            x = self.data[i]['x']
            y = self.data[i]['y']
            width = self.data[i]['width']
            height = self.data[i]['height']
            glTexCoord2f(x, y)
            glVertex3f(0, height, 0)

            glTexCoord2f(x + width, y)
            glVertex3f(width, height, 0)

            glTexCoord2f(x + width, y - height)
            glVertex3f(width, 0, 0)

            glTexCoord2f(x, y - height)
            glVertex3f(0, 0, 0)

            glEnd()

            off = self.data[i]['xadvance']/self.width
        glDisable(GL_BLEND)
        glDepthFunc(GL_LESS)





