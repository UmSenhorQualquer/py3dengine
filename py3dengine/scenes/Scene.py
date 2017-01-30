from py3DEngine.cameras.Camera 			import Camera
from py3DEngine.objects.MarkerObject 	import MarkerObject
from py3DEngine.objects.RectangleObject import RectangleObject
from py3DEngine.objects.TriangleObject 	import TriangleObject
from py3DEngine.objects.SceneObject 	import SceneObject
from py3DEngine.objects.TriangleObject 	import TriangleObject
from py3DEngine.objects.PointObject 	import PointObject
from py3DEngine.objects.RectangleObject import RectangleObject
from py3DEngine.objects.EllipsoidObject import EllipsoidObject
from py3DEngine.objects.MarkerObject 	import MarkerObject
from py3DEngine.objects.EllipseObject 	import EllipseObject
from py3DEngine.objects.CylinderObject 	import CylinderObject
from py3DEngine.objects.PlaneObject 	import PlaneObject
from py3DEngine.objects.WavefrontObject import WavefrontObject
from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJObject import WavefrontOBJObject


class Scene(object):

	def __init__(self):
		self.selectedObject = None
		self._objects = []
		self._cameras = []
		
	def synchronize(self):pass

	def getCamera(self, name):
		for obj in self.cameras:
			if name==obj.name: return obj
		return None

	def getObject(self, name):
		for obj in self.objects:
			if name==obj.name: return obj
		return None

	def initHierarchy(self, value):
		for o in value:
			parentName = o.getProperty('parent', None)
			objName = o.name
			if parentName!=None:
				parent 	= self.getObject(parentName)
				obj 	= self.getObject(objName)
				parent.addChild(obj)

	@property
	def objects(self): return self._objects
	@objects.setter
	def objects(self, value):
		self._objects = []

		from_WavefrontOBJObject = False
		for o in value:
			if isinstance(o, WavefrontOBJObject):
				objtype = o.getProperty('type')
				
				if objtype=='TriangleObject': 	obj = TriangleObject()
				if objtype=='MarkerObject': 	obj = MarkerObject()
				if objtype=='RectangleObject': 	obj = RectangleObject()
				if objtype=='EllipsoidObject': 	obj = EllipsoidObject()
				if objtype=='EllipseObject': 	obj = EllipseObject()
				if objtype=='CylinderObject': 	obj = CylinderObject()
				if objtype=='PlaneObject': 		obj = PlaneObject()
				if objtype=='PointObject': 		obj = PointObject()
				#For historical reasons
				if objtype=='WavefrontObject' or objtype=='TerrainObject': 	obj = WavefrontObject(self)

				obj.wavefrontobject = o; self._objects.append(obj)

				from_WavefrontOBJObject = True
			else:
				self._objects.append(o)

		if from_WavefrontOBJObject: self.initHierarchy(value)
		


	@property
	def cameras(self): return self._cameras
	@cameras.setter
	def cameras(self, value):
		self._cameras =[]
		for o in value:
			if isinstance(o, WavefrontOBJObject):
				if o.getProperty('type')=='Camera': 
					win = Camera()
					win.wavefrontobject = o
					self._cameras.append(win)
			else:
				self._cameras.append(o)


