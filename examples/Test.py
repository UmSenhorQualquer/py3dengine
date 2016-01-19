import sys,cv2, numpy as np, os, sys, itertools
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3DEngine.scenes.Scene import Scene
from py3DEngine.bin.RunScene import RunScene

SCENE = 'DolphinScene.obj'

scene = Scene()

w = WavefrontOBJReader(SCENE)
scene.objects = w.objects
scene.cameras = w.cameras

ellipse = scene.getObject('Test')

print ellipse.pointIn( (0,0,0.1) )


run = RunScene(SCENE)
run.startScene()
