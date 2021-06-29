from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.error import GLError
import glm
import glfw
from ctypes import *


class Shader:
    def __init__(self, vs, fs):
        with open(vs) as vertexSourceFile:
            vertexSource = vertexSourceFile.read()
        with open(fs) as fragmentSourceFile:
            fragmentSource = fragmentSourceFile.read()

        self.program = glCreateProgram()

        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(vertex, vertexSource)
        glShaderSource(fragment, fragmentSource)

        glCompileShader(vertex)
        glCompileShader(fragment)

        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            print("failed to compile vertex shader:", glGetShaderInfoLog(vertex))
            return
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            print("failed to compile fragment shader", glGetShaderInfoLog(fragment).decode())
            return

        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)

        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print("failed to link individual shaders into shader program", glGetProgramInfoLog(self.program))
            return

    def setFloat(self, Name, value):
        glUniform1f(glGetUniformLocation(self.program, Name), value)

    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def setBool(self, Name, value):
        glUniform1i(glGetUniformLocation(self.program, Name), value)

    def setVec2(self, Name, value):
        glUniform2f(glGetUniformLocation(self.program, Name), *value)

    def setVec3(self, Name, value):
        glUniform3f(glGetUniformLocation(self.program, Name), *value)

    def setVec4(self, Name, value):
        glUniform4f(glGetUniformLocation(self.program, Name), *value)

    def setMat4(self, Name, value):
        glUniformMatrix4fv(glGetUniformLocation(self.program, Name), 1, GL_FALSE, glm.value_ptr(value))

    def use(self):
        glUseProgram(self.program)

    def unuse(self):
        glUseProgram(0)


def getOpenGlErrorIfExist():
    GL_Error = glGetError()
    if GL_Error != GL_NO_ERROR:
        print('OpenGL Error: ', gluErrorString(GL_Error))



