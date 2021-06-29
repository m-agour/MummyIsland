import sys

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ('''
ERROR: PyOpenGL not installed properly.  
        ''')

def init():
   glClearColor (0.0, 0.0, 0.0, 0.0)
   glShadeModel (GL_FLAT)

def display():
   glClear (GL_COLOR_BUFFER_BIT)
   glColor3f (1.0, 1.0, 1.0)
   glLoadIdentity ()             # clear the matrix

   gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
   glScalef (1.0, 2.0, 1.0)      # modeling transformation
   glutWireCube (1.0)
   glFlush ()

def reshape (w, h):
   glViewport (0, 0, w, h)
   glMatrixMode (GL_PROJECTION)
   glLoadIdentity ()
   glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
   glMatrixMode (GL_MODELVIEW)

def keyboard(key, x, y):
   if key == chr(27):
      import sys
      sys.exit(0)

glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (500, 500)
glutInitWindowPosition (100, 100)
glutCreateWindow ('cube')
init ()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()