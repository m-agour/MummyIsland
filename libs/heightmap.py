from PIL import Image
from OpenGL.GL import *
import numpy as np
from libs.Texture import loadTexture


class Heightmap:
    def __init__(self, heightmap, normal, diffuse):
        self.image = Image.open(heightmap).convert('L')
        self.normImg = Image.open(normal)

        self.width, self.height = self.image.size
        self.VAO = glGenVertexArrays(1)
        self.IBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        self.vertices = []
        self.indices = []
        self.texCoords = []
        self.normals = []
        self.tangents = []
        self.bitangents = []

        self.maxHeight = 10
        self.getVertices()
        self.calcIndices()
        self.TEXBuffer = glGenTextures(3)
        self.diff = loadTexture(diffuse, self.TEXBuffer[0])
        self.lightDir = (0.2, -1.0, 0.3)

        self.buffer()

    def getHeight(self, xx, zz):
        return self.image.getpixel((xx, zz)) / 256 * self.maxHeight

    def getVertices(self):
        for x in range(self.height):
            for y in range(self.width):
                self.vertices.append(x)
                self.vertices.append(self.image.getpixel((x, y)) / 256 * self.maxHeight)
                self.vertices.append(y)
                temp_x = x / ((self.height - 1) / 250)
                temp_y = y / ((self.width - 1) / 250)
                self.vertices.append(round(temp_x, 2))
                self.vertices.append(round(temp_y, 2))
                xx, yy, zz = self.normImg.getpixel((x, y))
                self.vertices.append(self.normImg.getpixel((x, y))[0] / 256)
                self.vertices.append(self.normImg.getpixel((x, y))[1] / 256)
                self.vertices.append(self.normImg.getpixel((x, y))[2] / 256)

    def calcIndices(self):
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                start = y * self.width + x
                self.indices.append(start)
                self.indices.append(start + 1)
                self.indices.append(start + self.width)
                self.indices.append(start + 1)
                self.indices.append(start + 1 + self.width)
                self.indices.append(start + self.width)

    def calcTexCoords(self):
        for y in range(self.height):
            for x in range(self.width):
                temp_x = x / ((self.height - 1) / 150)
                temp_y = y / ((self.width - 1) / 150)
                self.texCoords.append(temp_x)
                self.texCoords.append(temp_y)

    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.diff)

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)

    def buffer(self):
        vertices = np.array(self.vertices, dtype=np.float32).flatten()
        faces = np.array(self.indices, dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(0))

        # texture position
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(12))

        # normal position
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(20))

    def collision(self, camera):

        x = camera.camera_pos[0]
        z = camera.camera_pos[1]
        y = camera.camera_pos[2]

        camera.camera_pos[1] = self.interpolate_current_heigh(x, y)

    def interpolate_current_heigh(self, x, y):
        return bilinear_interpolation(x, y,
                                      [(int(x), int(y), self.getHeight(int(x), int(y))),
                                       (int(x) + 1, int(y), self.getHeight(int(x) + 1, int(y))),
                                       (int(x), int(y) + 1, self.getHeight(int(x), int(y) + 1)),
                                       (int(x) + 1, int(y) + 1, self.getHeight(int(x) + 1, int(y) + 1))])

    def playerHeight(self, player):
        return self.interpolate_current_heigh(player.getPos()[0], player.getPos()[2]) + player.playerHeight

    def anyHeight(self, pos, height):
        return self.interpolate_current_heigh(pos[0], pos[2]) + height

    def checkIfInRange(self, cam_pos):
        if 0 < cam_pos[0] < self.width - 1 and 0 < cam_pos[2] < self.height - 1:
            return True
        else:
            return False


def bilinear_interpolation(x, y, points):
    points = sorted(points)  # order points by x, then by y
    (x1, y1, q11), (xn1, y2, q12), (x2, yn1, q21), (xn2, yn2, q22) = points

    if x1 != xn1 or x2 != xn2 or y1 != yn1 or y2 != yn2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
            ) / ((x2 - x1) * (y2 - y1) + 0.0)
