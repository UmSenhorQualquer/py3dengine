#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script loads a scene and calculate the closest point between 2 rays traced from 2 different cameras.
"""

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.Scene import Scene
from py3dengine.cameras.Ray import Ray

# Load the scene from a file
w = WavefrontOBJReader('data/scene-example.obj')

# Initialize the scene
scene = Scene(describer=w)

cam1 = scene.getCamera('Camera1')
cam2 = scene.getCamera('Camera2')

ray1 = cam1.addRay(500, 400)
ray2 = cam2.addRay(500, 450)

ray1.collidePlanZ(0)
ray2.collidePlanZ(0)

dist, p1, p2, p = Ray.find_closest_point(ray1, ray2);

print('****************************************')
print('Distance between points:\t', dist)
print('Point in the Camera1 ray:\t', p1.tolist())
print('Point in the Camera2 ray:\t', p2.tolist())
print('Closest point:\t\t\t', p)
print('****************************************')
