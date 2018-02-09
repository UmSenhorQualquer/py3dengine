

import sys,cv2, numpy as np, os, sys, csv

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.SceneClient import SceneClient


#PARAMETERS
SCENE_FILE 			= '/media/ricardo/Elements/DOLPHINS/13_02_2015/scene.obj'
SCENE_FILE 			= '../../Dolphin/DOLPHINS/13_02_2015/sceneWithPool.obj'
SERVER_HOST 		= 'localhost', 8000

w = WavefrontOBJReader(SCENE_FILE)
scene = SceneClient(SERVER_HOST)
scene.objects = w.objects
scene.cameras = w.cameras
for camera in scene.cameras: camera.cleanRays()




p0 = (600,200)
p2 = (700,300)
p1 = (p2[0],p0[1])
p3 = (p0[0],p2[1])

objects = scene.objects
camera0 = scene.cameras[0]
camera1 = scene.cameras[1]

ray0 = camera0.addRay( *p0 ); ray0.collide(objects)
ray1 = camera0.addRay( *p1 ); ray1.collide(objects)
ray2 = camera0.addRay( *p2 ); ray2.collide(objects)
ray3 = camera0.addRay( *p3 ); ray3.collide(objects)

pp0 = ray0.points[1]
pp1 = ray1.points[1]
pp2 = ray2.points[1]
pp3 = ray3.points[1]

for camera in scene.cameras[1:]:

	ppp0 = camera.calcPixel(*pp0)
	ppp1 = camera.calcPixel(*pp1)
	ppp2 = camera.calcPixel(*pp2)
	ppp3 = camera.calcPixel(*pp3)

	camera.addRay(*ppp0)
	camera.addRay(*ppp1)
	camera.addRay(*ppp2)
	camera.addRay(*ppp3)

