import threading
from libs.Texture import *
import json
from time import time
# import numpy as np


class OBJ:
    generate_on_init = True


    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue

            values = line.split()

            if not values:
                continue

            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}

            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")

            if values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = loadTexture(imagefile)

            else:
                mtl[values[0]] = map(float, values[1:])
        return contents

    def __init__(self, filename, Json=False, Zip=False, mtl=None, swapyz=False, pos=(0, 0, 0)):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        self.pos = pos
        self.matFiles = []


        if Json:
            self.loadJson(filename, mtl)
        elif Zip:
            self.loadZip(filename, mtl)
        else:
            self.load(filename, swapyz)
            self.saveJson(filename)

        if self.generate_on_init:
            self.generate()

    def saveJson(self, filename):
        file = self.__dict__.copy()
        del(file["gl_list"])
        mtlTmp = {}
        for i in file["mtl"].keys():
            mtlTmp[i] = {}
            mtlTmp[i]["texture_Kd"] = file["mtl"][i]["map_Kd"]
        file["mtl"] = mtlTmp
        json.dump(file, open(filename.replace(".obj", ".json"), 'w'))

    def loadJson(self, filename, mtl):
        self.__dict__ = json.load(filename)
        self.mtl = mtl


    def loadZip(self, filename, mtl):
        self.__dict__ = json.load(filename)
        self.mtl = mtl

    def load(self, filename, swapyz):
        dirname = os.path.dirname(filename)
        material = None

        objFile = open(filename, "r")

        for line in objFile:
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
                # print(material)
            elif values[0] == 'mtllib':
                self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))



    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glPushMatrix()

        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]

            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                n = list(mtl['Kd'])
                try:
                    glColor(n[0], n[1], n[2])
                except:
                    ...
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3f(*self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2f(*self.texcoords[texture_coords[i] - 1])
                glVertex3f(*self.vertices[vertices[i] - 1])
            glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()
        glEndList()

    def render(self):
        glCallList(self.gl_list)

    def free(self):
        glDeleteLists([self.gl_list])




    # delete useless vars
    # del self.vertices
    # del self.normals
    # del self.texCoords
    # del self.faces

