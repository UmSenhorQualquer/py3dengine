import numpy as np
from py3DEngine.objects.SceneObject import SceneObject
from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJObject import WavefrontOBJObject

class WavefrontOBJSceneObject(SceneObject):

	def __init__(self, name='Untitled'): SceneObject.__init__(self,name)


	def afterLoadSceneObject(self):
		"""
		Function called after the object is loaded from a file
		"""
		pass

	@property
	def wavefrontobject(self):
		obj = WavefrontOBJObject(self.name)
		obj.color = self.color

		obj.addProperty('position', 	','.join(map(str, self.position 	)))
		obj.addProperty('centerOfMass', ','.join(map(str, self.centerOfMass )))
		obj.addProperty('rotation', 	','.join(map(str, self.rotation		)))
		obj.addProperty('active', 		str(self.active))
		obj.addProperty('refraction', 	str(self.refraction))
		
		if self.parentObj!=None: obj.addProperty('parent', self.parentObj.name )

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.color 	= value.color
		self.name 	= value.name

		self.position 			= list(eval(value.getProperty('position', 		'0.0,0.0,0.0')))
		self.centerOfMass 		= list(eval(value.getProperty('centerOfMass', 	'0.0,0.0,0.0')))
		self.rotation 			= list(eval(value.getProperty('rotation', 		'0.0,1.0,0.0,0.0')))
		self.active 			= value.getProperty('active', 'True')=='True'
		self.refraction 		= eval(value.getProperty('refraction', 			'None'))
		
		self.afterLoadSceneObject()
		self.updateMesh()
		
		
