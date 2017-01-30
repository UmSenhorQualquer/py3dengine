from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJObject import WavefrontOBJObject

class WavefrontOBJCamera(object):

	@property
	def wavefrontobject(self):
		obj = WavefrontOBJObject(self.name)
		obj.color = self.color

		obj.addProperty('type', 'Camera')
		obj.addProperty('cameraMatrix', 	self.cameraMatrix.flatten().tolist() )
		obj.addProperty('cameraDistortion', self.cameraDistortion.tolist() )
		obj.addProperty('rotationVector', 	self.rotationVector.tolist() )
		obj.addProperty('maxFocalLength', 	self.maxFocalLength )
		obj.addProperty('cameraWidth', 		self.cameraWidth )
		obj.addProperty('cameraHeight', 	self.cameraHeight )
		obj.addProperty('showFaces', 		self.showFaces )
		obj.addVertice( tuple(self.position.tolist()[0]) )

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.color 	= value.color
		self.name 	= value.name

		self.cameraWidth 		= float(value.getProperty('cameraWidth'))
		self.cameraHeight 		= float(value.getProperty('cameraHeight'))
		self.maxFocalLength 	= value.getProperty('maxFocalLength')
		self.rotationVector 	= value.getProperty('rotationVector')
		self.cameraDistortion 	= value.getProperty('cameraDistortion')
		self.cameraMatrix 		= value.getProperty('cameraMatrix')
		self.showFaces 			= value.getProperty('showFaces')=='True'
		self.position 			= value.getVertice(0)
		

