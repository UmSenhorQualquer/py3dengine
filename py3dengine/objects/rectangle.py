from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject
from py3dengine.objects.base_object import SceneObject
from py3dengine.objects.triangle import TriangleObject
import numpy as np

class RectangleObject(SceneObject):

	def __init__(self, *args, **kwargs):

		name = kwargs.get('name', 'Untitled')
		p0 = kwargs.get('p0', (0, 0, 0))
		p1 = kwargs.get('p1', (1, 0, 0))
		p2 = kwargs.get('p2', (1, 0, 1))
		p3 = kwargs.get('p3', (0, 0, 1))
		
		self._triangleA = TriangleObject(name, p0, p1, p2)
		self._triangleB = TriangleObject(name, p2, p3, p0)

		super().__init__(*args, **kwargs)

	@classmethod
	def from_json(cls, json):
		obj = super().from_json(json)
		obj.point0 = json.get('point0')
		obj.point1 = json.get('point1')
		obj.point2 = json.get('point2')
		obj.point3 = json.get('point3')
		return obj

	def to_json(self, data={}):
		data = super().to_json(data)
		data['point0'] = self.point0
		data['point1'] = self.point1
		data['point2'] = self.point2
		data['point3'] = self.point3
		return data

	@property
	def color(self): return self._triangleA.color
	@color.setter
	def color(self, value): 
		self._triangleA.color = value
		self._triangleB.color = value

	@property
	def point0(self): return self._triangleA.point0
	@point0.setter
	def point0(self, value): 
		self._triangleA.point0 = value
		self._triangleB.point2 = value

	@property
	def point1(self): return self._triangleA.point1
	@point1.setter
	def point1(self, value): 
		self._triangleA.point1 = value


	@property
	def point2(self): return self._triangleA.point2
	@point2.setter
	def point2(self, value): 
		self._triangleA.point2 = value
		self._triangleB.point0 = value


	@property
	def point3(self): return self._triangleB.point1
	@point3.setter
	def point3(self, value): 
		self._triangleB.point1 = value

	@property
	def points(self): return np.array([self.point0, self.point1, self.point2, self.point3])
	


	def collide_with_ray(self, ray):
		res = self._triangleA.collide_with_ray(ray)
		if res!=None: return res
		res = self._triangleB.collide_with_ray(ray)
		if res!=None: return res
		return None

	def DrawGL(self):
		self._triangleA.DrawGL()
		self._triangleB.DrawGL()
		super(RectangleObject, self).DrawGL()


	@property
	def wavefrontobject(self):
		obj = super(RectangleObject, self).wavefrontobject
		
		obj.addProperty('type', self._type)
		obj.addVertice( self.point0 )
		obj.addVertice( self.point1 )
		obj.addVertice( self.point2 )
		obj.addVertice( self.point3 )

		obj.addFace( (1,2,3,4) )

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.point0 			= value.getVertice(0)
		self.point1 			= value.getVertice(1)
		self.point2 			= value.getVertice(2)
		self.point3 			= value.getVertice(3)

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )
		
		