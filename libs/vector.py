# made by mohamed nagy 2nd comp
from math import sqrt, acos, tan, degrees, atan2, sin, cos, pi
import sys


class Vec3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __pow__(self, Vec):
        return Vec3(self.y * Vec.z - self.z * Vec.y,
                    self.z * Vec.x - self.x * Vec.z,
                    self.x * Vec.y - self.y * Vec.x)

    def __add__(self, operand):
        return Vec3(self.x + operand.x, self.y + operand.y, self.z + operand.z)

    def __iadd__(self, operand):
        return Vec3(self.x + operand.x, self.y + operand.y, self.z + operand.z)

    def __sub__(self, operand):
        return Vec3(self.x - operand.x, self.y - operand.y, self.z - operand.z)

    def __isub__(self, operand):
        return Vec3(self.x - operand.x, self.y - operand.y, self.z - operand.z)

    def __mul__(self, num):
        return Vec3(self.x * num, self.y * num, self.z * num)

    def __truediv__(self, num):
        return Vec3(self.x / num, self.y / num, self.z / num)

    def abs(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return str(self.tuple())

    def normalize(self):
        length = self.abs()
        return Vec3(self.x / length,
                    self.y / length,
                    self.z / length)

    def tuple(self):
        return self.x, self.y, self.z

    def shortestDist(self, point):
        mult = self.x * point.x + self.y * point.y + self.z * point.z
        return tan(acos(mult / (self.abs() * point.abs()))) * self.distance(point)

    def dot(self, vec2):
        return self.x * vec2.x + self.y * vec2.y + self.z * vec2.z

    def distance(self, vec2):
        return (vec2 - self).abs()

    # angle = aCos ( (V1.V2) / (|V1|.|V2|)  )
    # def angle(self):
    #     return atan(z/x)

    def angleWith(self, vec):
        return acos(self.dot(vec) / (self.abs() * vec.abs()))

    def angleWithX(self):
        vec = Vec3(1, 0, 0)
        return self.angleWith(vec)

    def angleWithY(self):
        vec = Vec3(0, 1, 0)
        return self.angleWith(vec)

    def angleWithZ(self):
        vec = Vec3(0, 0, 1)
        return self.angleWith(vec)

    def angleWithXZ(self):
        return pi / 2 - self.angleWithY()

    def angleWithPlane(self, normalVec):
        return pi / 2 - self.angleWith(normalVec)

    def reset(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def rotate(self, theta):
        cs = cos(theta)
        sn = sin(theta)
        px = self.x * cs - self.z * sn
        pz = self.x * sn + self.z * cs
        self.x = px
        self.z = pz

    def xy(self):
        return self.x, self.y

    def yz(self):
        return self.y, self.z

    def xz(self):
        return self.x, self.z

    def vec2xy(self):
        return Vec2(self.x, self.y)

    def vec2yz(self):
        return Vec2(self.y, self.z)

    def vec2xz(self):
        return Vec2(self.x, self.z)

    def copy(self):
        return Vec3(self.x, self.y, self.z)


class Vec2:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __pow__(self, operand):
        return self.x * operand.y - self.y * operand.x

    def __add__(self, operand):
        return Vec2(self.x + operand.x, self.y + operand.y)

    def __sub__(self, operand):
        return Vec2(self.x - operand.x, self.y - operand.y)

    def __mul__(self, num):
        return Vec2(self.x * num, self.y * num)

    def abs(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return str(self.tuple())

    def normalize(self):
        length = self.abs()
        return Vec2(self.x / length,
                    self.y / length)

    def tuple(self):
        return self.x, self.y

    def degree(self, vec2):
        mult = self.x * vec2.x + self.y * vec2.y
        return tan(acos(mult / (self.abs() * vec2.abs()))) * self.distance(vec2)

    def dot(self, vec2):
        return self.x * vec2.x + self.y * vec2.y

    def distance(self, vec2):
        return (vec2 - self).abs()


def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=sys.float_info.epsilon):
    ndotu = planeNormal.dot(rayDirection)
    if abs(ndotu) < epsilon:
        return Vec3(0, 0, 0)

    w = rayPoint - planePoint
    si = -planeNormal.dot(w) / ndotu
    Psi = w + rayDirection * si + planePoint
    return Psi


def firstTri(px, py, tx, ty):
    if px + py <= tx + ty + 1:
        return True
    else:
        return False



def checkLinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=sys.float_info.epsilon):
    intPoint = LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon)
    if int(planePoint.x) <= intPoint.x <= int(planePoint.x)+1 and int(planePoint.z) <= intPoint.z <= int(planePoint.z)+1:
        return intPoint
    else:
        return None



def meanVec(listOfVecs):
    t = listOfVecs[0]
    length = len(listOfVecs)
    for i in range(1, length):
        t += listOfVecs[i]
    return t


def getNormalVector(p1, p2, p3):
    Dir = (p2 - p1) ** (p3 - p1)
    return Dir.normalize()


def rotationMatrix(FR, UP=Vec3(0, 1, 0)):
    A = UP ** FR
    omega = degrees(acos(UP.dot(FR)))
    return omega, *A.tuple()


def pointYOnPlane(x, z, normal, point):
    r, s, t = normal.tuple()
    a, b, c = point.tuple()
    y = (r*a + s*b + t*c - r*x - t*z) / s
    return y

# print(LinePlaneCollision(Vec3(0, 1, 0), Vec3(0, 0, 0), Vec3(0,  -1, 0), Vec3(1, 1, 1)))
