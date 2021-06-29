from libs.Texture import *
import json
import re


class OBJ:
    generate_on_init = True

    def loadMaterial(self, filename):
        current = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue

            values = line.split()

            if not values:
                continue

            if values[0] == 'newmtl':
                current = values[1]

            elif current is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")

            if values[0] == 'map_Kd':
                imageFile = os.path.join(dirname, values[1])
                self.mtl[current] = imageFile
                print(self.mtl)



    def __init__(self, filename, first=False, swapyz=False, pos=(0, 0, 0)):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texCoords = []
        self.faces = []
        self.pos = pos
        self.mtl = {}
        self.firstFrame = first
        self.load(filename, swapyz)
        self.saveTex(filename)

        del(self.__dict__["pos"])
        del(self.__dict__["mtl"])



    def saveTex(self, filename):
        # make json files and one tan file
        dirname = os.path.dirname(filename)
        json.dump(self.__dict__["mtl"], open(os.path.join(dirname, "textures.tan"), 'w'))



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
                self.texCoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
                # print(material)
            elif values[0] == 'mtllib':
                if self.firstFrame:
                    self.loadMaterial(os.path.join(dirname, values[1]))
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
                self.faces.append((face, norms, texcoords))



# path = "assets/obj/enemy/mummy"
path = "assets/obj/player/weapon"
# path = "assets/obj/crow"


tex = os.path.join(path, "textures.tan")


files =[os.path.join(path, file) for file in os.listdir(path) if file.endswith('.obj')]

files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

# pack json files
frames = []

fileName = os.path.basename(path)

for i in range(len(files)):
    print(files[i])
    f = True if i == 0 else False
    frames.append(OBJ(files[i], first=f).__dict__)

json.dump(frames, open(os.path.join(path, "animation"), 'w'), separators=(',', ':'))
[os.remove(i) for i in files]
[os.remove(i.replace(".obj", ".mtl")) for i in files]