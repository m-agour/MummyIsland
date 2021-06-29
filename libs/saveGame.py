# try:
#     import ujson as json
# except:
#     import json
import gzip
import json
from libs.vector import Vec3
import os
import time
from OpenGL.GLUT import *
from tkinter import *
import tkinter.messagebox as box


def saveAll(game):
    w = _savePlayer(game.player)
    x = _saveCam(game.player.camera)
    y = _saveGun(game.player.gun)
    z = _saveEnemies(game.enemies)
    return [w, x, y, z]


# dat = json.load(open("./save/savecam.json"))


def loadAll(game, data):
    _loadPlayer(game.player, data[0])
    _loadCam(game.player.camera, data[1])
    _loadGun(game.player.gun, data[2])
    _loadEnemies(game.enemies, data[3])


def _savePlayer(player):
    dic = dict(player.__dict__)
    for i in ["sounds", "camera", "terrain", "gun", "motionTimer"]:
        del dic[i]
    return dic


def _loadPlayer(player, data):
    for i in data.keys():
        player.__dict__[i] = data[i]


def _saveCam(camera):
    dic = dict(camera.__dict__)
    for i in ["cam_pos", "cam_fr", "cam_up", "cam_ri"]:
        dic[i] = dic[i].tuple()
    return dic


def _loadCam(camera, data):
    camera.__dict__ = dict(data)
    for i in ["cam_pos", "cam_fr", "cam_up", "cam_ri"]:
        camera.__dict__[i] = Vec3(*data[i])


def _saveGun(gun):
    dic = dict(gun.__dict__)
    for i in ["animation", "sounds", "muzzle"]:
        del dic[i]
    if dic["shootingDir"]:
        dic["shootingDir"] = dic["shootingDir"].tuple()
    return dic


def _loadGun(gun, data):
    for i in data.keys():
        gun.__dict__[i] = data[i]
    if data["shootingDir"]:
        gun.shootingDir = Vec3(*data["shootingDir"])


def _saveEnemies(lstOfEnemies):
    outDicLst = []
    for i in lstOfEnemies:
        tmp = dict(i.__dict__)
        for j in tmp.keys():
            if j in ["initialPos", "prevPos", "pos", "front", "forces"]:
                tmp[j] = tmp[j].tuple()
        for j in ["player", "texture", "dyingSounds", "animation"]:
            del (tmp[j])
        outDicLst.append(tmp)
    return outDicLst


def _loadEnemies(lstOfEnemies, data):
    for i in range(len(lstOfEnemies)):
        for j in data[i].keys():
            lstOfEnemies[i].__dict__[j] = data[i][j]
            if j in ["initialPos", "prevPos", "pos", "front", "forces"]:
                lstOfEnemies[i].__dict__[j] = Vec3(*data[i][j])


class Record:
    def __init__(self, game):
        self.frames = []
        self.firstFrame = None
        self.recording = False
        self.path = "save"
        self.name = ""
        self.game = game
        self.playing = False
        self.playingIndex = 0
        self.length = 0

    def startRec(self):
        self.frames = []
        self.recording = True
        self.name = time.strftime("%Y%m%d-%H%M%S.rec")
        self.firstFrame = saveAll(self.game)

    def stopRec(self):
        print("stopped recording")
        self.recording = False
        self.length = len(self.frames)
        data = bytes(json.dumps([self.firstFrame, self.frames]), 'utf-8')
        s_out = gzip.compress(data)
        with open(os.path.join(self.path, self.name), 'wb') as out:
            out.write(s_out)

        # json.dump([self.firstFrame, self.frames], open(os.path.join(self.path, self.name), 'w'), separators=(',',':'))

    def playRec(self, file):
        self.recording = False
        self.playing = True
        with open(file, "rb") as saveFile:
            self.firstFrame, self.frames = json.loads(gzip.decompress(saveFile.read()).decode('utf-8'))
        loadAll(self.game, self.firstFrame)

    def playLastRec(self):
        files = [os.path.join(self.path, x) for x in os.listdir(self.path) if x.endswith(".rec")]
        latest = max(files, key=os.path.getctime)
        print(latest)
        self.playRec(latest)


    def playFromList(self):
        print(glutGetWindow())
        files = [x for x in os.listdir(self.path) if x.endswith(".rec")]

        window = Tk()
        window.title("records")

        frame = Frame(window)
        listbox = Listbox(frame)

        for i in range(len(files)):
            listbox.insert(i, files[i])

        def action():
            self.playRec(os.path.join(self.path, listbox.get(ACTIVE)))
            window.destroy()

        btn = Button(frame, text='load', command=action)
        btn.pack(side=RIGHT, padx=5)
        listbox.pack(side=LEFT)
        frame.pack(padx=30, pady=60)
        window.mainloop()

    def isPlaying(self):
        return self.playing

    def isRecording(self):
        return self.recording

    def loop(self):
        if self.recording:
            player = []
            for i in ["forward", "backward", "left", "right", "jump", "running", "triggering"]:
                player.append(self.game.player.__dict__[i])

            enemies = []
            for i in self.game.enemies:
                enemyPos = i.pos.tuple()
                enemies.append(tuple((round(j, 4) for j in enemyPos)))

            camera = []
            # for i in ["jaw", "pitch"]:
            #     # camera.append(round(self.game.player.camera.__dict__[i], 6))
            #     camera.append(self.game.player.camera.__dict__[i])
            #     print(self.game.player.camera.__dict__[i])
            for i in ["cam_pos", "cam_fr"]:
                tup = self.game.player.camera.__dict__[i].tuple()
                camera.append(tuple((round(j, 4) for j in tup)))

            self.frames.append([player, self.game.player.gun.reloading, camera, enemies])

        elif self.playing:
            frame = self.frames[self.playingIndex]
            playerData = ["forward", "backward", "left", "right", "jump", "running", "triggering"]
            cameraData = ["jaw", "pitch"]

            for i in range(len(playerData)):
                self.game.player.__dict__[playerData[i]] = frame[0][i]

            self.game.player.gun.forceReload = frame[1]

            # for i in range(len(cameraData)):
            #     self.game.player.camera.__dict__[playerData[i]] = frame[2][i]
            #     print(frame[2][i])
            camera = self.game.player.camera
            camera.cam_pos = Vec3(*frame[2][0])
            camera.cam_fr = Vec3(*frame[2][1])
            camera.cam_ri = (camera.cam_fr ** Vec3(0.0, 1.0, 0.0)).normalize()
            camera.cam_up = (camera.cam_ri ** camera.cam_fr).normalize()

            for i in range(len(self.game.enemies)):
                self.game.enemies[i].pos = Vec3(*frame[3][i])

            self.playingIndex += 1
            if self.playingIndex == len(self.frames):
                self.playingIndex = 0
                self.playing = False
                self.game.player.camera.firstMovement = True
# class Record:
#     def __init__(self, game):
#         self.frames = []
#         self.firstFrame = []
#         self.recording = False
#         self.path = "save"
#         self.name = ""
#         self.game = game
#         self.playing = False
#         self.playingIndex = 0
#         self.length = 0
#
#     def startRec(self):
#         self.frames = []
#         self.recording = True
#         self.name = time.strftime("%Y%m%d-%H%M%S")
#
#     def stopRec(self):
#         print("stopped recording")
#         self.recording = False
#         self.length = len(self.frames)
#         json.dump(self.frames, open(os.path.join(self.path, self.name), 'w'))
#
#     def play(self):
#         print("playing started")
#         self.recording = False
#         self.playing = True
#
#     def isPlaying(self):
#         return self.playing
#
#     def isRecording(self):
#         return self.recording
#
#     def loop(self):
#         if self.recording:
#             w = _savePlayer(self.game.player)
#             x = _saveCam(self.game.player.camera)
#             y = _saveGun(self.game.player.gun)
#             z = _saveEnemies(self.game.enemies)
#             self.frames.append([w, x, y, z])
#
#         elif self.playing:
#             _loadPlayer(self.game.player, self.frames[self.playingIndex][0])
#             _loadCam(self.game.player.camera, self.frames[self.playingIndex][1])
#             _loadGun(self.game.player.gun, self.frames[self.playingIndex][2])
#             _loadEnemies(self.game.enemies, self.frames[self.playingIndex][3])
#             self.playingIndex += 1
#             if self.playingIndex == self.length:
#                 self.playingIndex = 0
#                 self.playing = False
