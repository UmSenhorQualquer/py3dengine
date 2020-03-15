from py3dengine.cameras.camera 			import Camera
from py3dengine.objects.marker 	import MarkerObject
from py3dengine.objects.rectangle import RectangleObject
from py3dengine.objects.triangle 	import TriangleObject
from py3dengine.objects.base_object 	import SceneObject
from py3dengine.objects.triangle 	import TriangleObject
from py3dengine.objects.point 	import PointObject
from py3dengine.objects.rectangle import RectangleObject
from py3dengine.objects.ellipsoid import EllipsoidObject
from py3dengine.objects.marker 	import MarkerObject
from py3dengine.objects.ellipse 	import EllipseObject
from py3dengine.objects.cylinder 	import CylinderObject
from py3dengine.objects.plane 	import PlaneObject
from py3dengine.objects.wavefront import WavefrontObject
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

	@classmethod
	def from_json(cls, json):
		obj = cls()

		for data in json.get('objects'):
			obj.objects.append(
				eval(data['type']).from_json(data)
			)

		for data in json.get('cameras'):
			obj.cameras.append(
				eval(data['type']).from_json(data)
			)

		return obj

	def to_json(self, data={}):

		data['objects'] = []
		for o in self.objects:
			data['objects'].append(o.to_json())

		data['cameras'] = []
		for c in self.cameras:
			data['cameras'].append(c.to_json())

		return data
		
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

	def add_object(self,obj):
		self._objects.append(obj)

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


