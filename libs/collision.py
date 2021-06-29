# from math import sqrt
# class collision:
#
#     def intersectRaySegmentSphere(o, d, so, radius2, ip):
#         # we pass in d non-normalized to keep it's length
#         # then we use that length later to compare the intersection point to make sure
#         # we're within the actual ray segment
#         l = d.length()
#         d /= l
#
#         m = o - so # vec3
#         b = m.dot(d)
#         c = m.dot(m) - radius2
#
#         # Exit if r’s origin outside s (c > 0) and r pointing away from s (b > 0)
#         if c > 0.0 and b > 0.0:
#             return False
#
#         discr = b * b - c
#
#         # A negative discriminant corresponds to ray missing sphere
#         if discr < 0.0:
#             return False
#
#         # Ray now found to intersect sphere, compute smallest t value of intersection
#         t = -b - sqrt(discr)
#
#         # If t is negative, ray started inside sphere so clamp t to zero
#         if t < 0.0:
#             t = 0.0
#         ip = o + (d * t)
#
#         # here's that last segment check I was talking about
#         if (t > l):
#             return False
#
#         return True


class Rect:

    def __init__(self, player, x=0, y=0, w=1, h=1):
        self.center = [x, y]
        self.width = w
        self.height = h
        self.player = player

    def checkCollWithPlayer(self, playerPos, playerWidth):
        return self.center[0] + 1.5 + playerWidth > playerPos.x > self.center[0] - 1.5 - playerWidth and \
                self.center[2] + 1.5 + playerWidth > playerPos.z > self.center[2] - 1.5 - playerWidth

    def handleCollisionWithPlayer(self, player):
        norm = self.player.camera.cam_pos - Vec3(temp[0], 0, temp[1])
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
            if center[0] + 1.5 + r > player.x > center[0] - 1.5 - r and center[2] + 1.5 + r > player.z > center[
                2] - 1.5 - r:
                self.player.camera.cam_pos += (norm + ((temp ** norm) - dir)).normalize() * self.player.currentSpeed

        elif not self.player.left and self.player.right:
            if center[0] + 1.5 + r > player.x > center[0] - 1.5 - r and center[2] + 1.5 + r > player.z > center[
                2] - 1.5 - r:
                self.player.camera.cam_pos += (norm + ((temp ** norm) - dir)).normalize() * self.player.currentSpeed
