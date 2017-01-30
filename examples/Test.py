import sys,cv2, numpy as np, os, sys, itertools
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3DEngine.scenes.Scene import Scene
from py3DEngine.bin.RunScene import RunScene

SCENE = '..\\..\\py3DSceneEditor\\py3DSceneEditor\\scene.obj'

scene = Scene()

w = WavefrontOBJReader(SCENE)
scene.objects = w.objects
scene.cameras = w.cameras

#ellipse = scene.getObject('Test')

#print ellipse.pointIn( (0,0,0.1) )

camera = scene.getCamera('Camera1')
img = camera.rayCastingImage(5, scene.objects, box=(300,300,400,400))

cv2.imshow('image', img)
cv2.waitKey(0)
#run = RunScene(scene)
#run.startScene()
