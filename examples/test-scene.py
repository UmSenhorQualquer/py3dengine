from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.Scene import Scene
from py3dengine.cameras.Ray import Ray

from py3dengine.scenes.GLScene import GLScene
from py3dengine.bin.RunScene import RunScene

w = WavefrontOBJReader('scene-example.obj')

scene = Scene()
scene = GLScene()

scene.objects = w.objects
scene.cameras = w.cameras

cam1 = scene.getCamera('Camera1')
cam2 = scene.getCamera('Camera2')

floor = scene.getObject('Floor')

ray1 = cam1.addRay(500, 400)
ray2 = cam2.addRay(500, 450)

ray1.collidePlanZ(0)
ray2.collidePlanZ(0)

dist, p1, p2, p = Ray.find_closest_point(ray1, ray2);

scene.add_point(p)

print('point', dist, p1, p2, p )


run = RunScene(scene)
run.startScene()
