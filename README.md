
# MummyIsland  
  
MummyIsland is a 3D game, Written in Python using Pyopengl and Pygame.  
  
![image](https://user-images.githubusercontent.com/63170874/123775636-d5fe2f80-d8ce-11eb-9510-ecac702169fa.png)



## How to run
 1. Install python 3  
 2. install Pyopengl and Pygame  
 3. open cmd
 4. `cd <main-directory>  `
 5. `python game.py `
 
## How to play
 -  WASD-controls
 - space for jumping
 - shift for running
 - f1 to start/stop recording
 - f2 to replay a record
 - esc to exit game

## Cheat Codes

 - To use cheat codes just type the code while playing


| code | what it does |
|--|--|
| massacre | kill all the mummies |
| hackmag | infinity number of bullets loaded into mag |
| maxa | infinity reloads |
| rocket | no gravity |
| flash | speed boost |
| neverdie | infinity health |
| slamdunk | high jump |
| reset | removes all applied cheats |

## Gameplay
latest version
https://youtu.be/myg0ISQryD8
previous version
https://youtu.be/TgGBlhRgckA

## For Devs
To add animations to the game follow these steps

 1. Export the animation as obj sequence format (I used [Obj Sequence Export](http://www.scriptspot.com/3ds-max/scripts/obj-sequence-export) for 3DS Max)
 2. Use obj.py to convert from obj sequence to single animation json file by changing 'path' string variable to the animation's folder.
 note: all obj/mtl files will be deleted and two files will be created instead.
 3. Compress the resulting "Animation" file to a "ZIP" format, and rename the compressed file to "something.pak".
 4. Now you should have 3 files: "something.pak", "texture.tan" and the texture image (if exists).


 - why not just use th obj sequence animation directly?
Because they will consume a lot of space, slower to load and the same texture will be loaded into memory multiple of times. 

 - why not use the collada format (.DAE)?
	Since the game is made using an old version of OpenGL (glBegin/glEnd), the default vertex shader cannot be modified to calculate the animation using transformation matrix of each vertex, and hence the best option is to precalculate thousands of sequential matrix multiplications by the CPU for each frame and store them in memory which will result in the same memory usage as the obj sequence.
