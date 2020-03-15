#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script loads a scene and calculate the closest point between 2 rays traced from 2 different cameras.
At the end it synchronizes the scene with a server.
This functionality is quite useful for debugging proposes, where you can visualize how your algorithm is performing by
using a remote server to visualize what is happening.

To run the server, execute:
python py3dengine/bin/run_scene_server.py
"""

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.cameras.ray import Ray
from py3dengine.scenes.scene_client import SceneClient

w = WavefrontOBJReader('data/scene-example.obj')

scene = SceneClient(('127.0.0.1', 5005), describer=w )

cam1 = scene.getCamera('Camera1')
cam2 = scene.getCamera('Camera2')

ray1 = cam1.addRay(500, 400)
ray2 = cam2.addRay(500, 450)

ray1.collidePlanZ(0)
ray2.collidePlanZ(0)

dist, p1, p2, p = Ray.find_closest_point(ray1, ray2);

scene.add_point(p, color=(1,0,0,1))

scene.synchronize()
