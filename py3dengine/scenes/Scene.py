from py3dengine.cameras.Camera 			import Camera
from py3dengine.objects.MarkerObject 	import MarkerObject
from py3dengine.objects.RectangleObject import RectangleObject
from py3dengine.objects.TriangleObject 	import TriangleObject
from py3dengine.objects.SceneObject 	import SceneObject
from py3dengine.objects.TriangleObject 	import TriangleObject
from py3dengine.objects.PointObject 	import PointObject
from py3dengine.objects.RectangleObject import RectangleObject
from py3dengine.objects.EllipsoidObject import EllipsoidObject
from py3dengine.objects.MarkerObject 	import MarkerObject
from py3dengine.objects.EllipseObject 	import EllipseObject
from py3dengine.objects.CylinderObject 	import CylinderObject
from py3dengine.objects.PlaneObject 	import PlaneObject
from py3dengine.objects.WavefrontObject import WavefrontObject
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJObject import WavefrontOBJObject


class Scene(object):

	def __init__(self, describer=None):
		self.selected_object = None

		if describer is not None:
			self.objects = describer.objects
		else:
			self._objects = []

		if describer is not None:
			self.cameras = describer.cameras
		else:
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

	def set_hierarchy(self, value):
		for o in value:
			parentName = o.getProperty('parent', None)
			objName = o.name
			if parentName!=None:
				parent 	= self.getObject(parentName)
				obj 	= self.getObject(objName)
				parent.add_child(obj)

	def add_point(self, p, name=None, color=None):
		self._objects.append(
			PointObject(f'point-{len(self._objects)}', p, color=color)
		)

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

		if from_WavefrontOBJObject: self.set_hierarchy(value)
		


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


