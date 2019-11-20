from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.GLScene import GLScene
from py3dengine.bin.RunScene import RunScene


w = WavefrontOBJReader('scene-example.obj')

scene = GLScene()
scene.objects = w.objects
scene.cameras = w.cameras

camera = scene.getCamera('Camera1')

ray 	= camera.addRay( 100, 100 )
collision = ray.collidePlanZ(0); 

print('Point of collision with the Z plain', collision)

floor	= scene.getObject('Floor')
collision = ray.collide([floor])

print('Point of collision with object Foor,', collision)

run = RunScene(scene)
run.startScene()
