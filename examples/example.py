from py3dengine.objects.ellipse import EllipseObject
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.glscene import GLScene
from py3dengine.bin.run_scene import RunScene
import pprint, json, numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

#w = WavefrontOBJReader('data/scene-example.obj')
scene = GLScene()
scene.add_object(
    EllipseObject(name='Ellipse 1')
)
#scene.objects = w.objects
#scene.cameras = w.cameras


"""
camera = scene.getCamera('Camera1')

ray 	= camera.addRay( 100, 100 )
collision = ray.collidePlanZ(0); 

print('Point of collision with the Z plain', collision)

floor	= scene.getObject('Floor')
collision = ray.collide([floor])

print('Point of collision with object Foor,', collision)

#run = RunScene(scene)
#run.startScene()

"""
pp = pprint.PrettyPrinter(depth=6)

data = scene.to_json()
pp.pprint(data)


s = GLScene.from_json(data)
print( s )

print(s.objects)

#data = json.dumps(data, cls=NumpyEncoder)
#pp.pprint(data)
