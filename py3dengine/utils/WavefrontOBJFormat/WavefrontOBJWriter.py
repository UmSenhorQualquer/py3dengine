import os


class WavefrontOBJWriter(object):
	
	def __init__(self, scene):
		self._scene = scene
		self._nvertices = 0

	@property
	def numOfvertices(self): return self._nvertices
	@numOfvertices.setter
	def numOfvertices(self, value): self._nvertices=value
	

	@property 
	def objects(self): return self._scene.objects
	@property 
	def cameras(self): return self._scene.cameras

	def export(self, objFilePath):
		objFilePath = str(objFilePath)

		objFileName = os.path.basename(objFilePath)
		objFileDir = os.path.dirname(objFilePath)
		scenename, _ = os.path.splitext(objFileName)

		mtlfileout = open(os.path.join(objFileDir, scenename+'.mtl'), 'w')

		for camera in self.cameras:
			desc = camera.wavefrontobject
			mtlfileout.write( desc.exportMaterial() )
			mtlfileout.write('\n\n\n')

		for obj in self.objects:
			desc = obj.wavefrontobject
			mtlfileout.write( desc.exportMaterial() )
			mtlfileout.write('\n\n\n')

		mtlfileout.close()
		
		fileout = open( objFilePath , 'w')
		fileout.write('mtllib '+scenename+'.mtl')
		fileout.write('\n\n')

		for camera in self.cameras:
			desc = camera.wavefrontobject
			fileout.write( desc.exportObject(self) )
			fileout.write('\n\n')
		
		for obj in self.objects:
			desc = obj.wavefrontobject
			fileout.write( desc.exportObject(self) )
			fileout.write('\n\n')
		
		fileout.close()
