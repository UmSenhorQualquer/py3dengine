import numpy as np

class WavefrontOBJObject(object):

	def __init__(self, name):
		self.name 			= name
		self._vertices 		= []
		self._faces 		= []
		self._points		= []
		self._properties 	= {}
		self._color 		= None

	def addProperty(self, key, value): 	self._properties[key] = value
	def addVertice(self, vertice): 		self._vertices.append(vertice)
	def addFace(self, facepoints ): 	self._faces.append(facepoints)
	def addPoint(self, point ): 		self._points.append(point)

	def getProperty(self, key, alt=''): return self._properties.get(key, alt)
	def getVertice(self, index): return self._vertices[index]

	@property 
	def name(self): return self._name
	@name.setter
	def name(self, value): self._name = value


	@property 
	def color(self): return self._color
	@color.setter
	def color(self, value): self._color = value


	def __value2String(self, value):
		if isinstance(value, tuple): 
			return ",".join( list(map(str, value) ))

		if isinstance(value, list): 
			return ",".join( list(map(str, value) ))

		if isinstance(value, np.ndarray): 
			return ",".join( list(map(str, value) ))


		return str(value)

	def exportObject(self, writer):
		nvertices = writer.numOfvertices

		out = []
		out.append('o %s' % self.name)
		if self.color is not None: out.append('usemtl %sMaterial' % self.name)
		
		for vertice in self._vertices:
			out.append('v %.9f %.9f %.9f' % tuple(vertice) )
			writer.numOfvertices += 1

		for face in self._faces:
			values = [nvertices+n for n in face]
			#values = face
			out.append('f %s' % ' '.join(list(map(str,values)) ))

		for pointIndex in self._points:
			out.append('p %s' % str(pointIndex+nvertices) )
		
		for prop, value in self._properties.items():
			out.append('# %s: %s' % (prop, self.__value2String(value)) )
		return '\n'.join(out)


	@property
	def verticesCount(self): return len(self._vertices)




	def exportMaterial(self):
		if self.color is None: return ''

		out = []
		out.append('newmtl %sMaterial' % self.name)
		out.append('Ka %.9f %.9f %.9f' % tuple(self.color[:3]) ) # Ambient color
		out.append('Kd %.9f %.9f %.9f' % tuple(self.color[:3]) ) # Diffuse color
		out.append('Ks %.9f %.9f %.9f' % tuple(self.color[:3]) ) # Specular color
		out.append('d %s' % self.color[3]) # Transparency
		out.append('illum 1') # illumination model
		return '\n'.join(out)


