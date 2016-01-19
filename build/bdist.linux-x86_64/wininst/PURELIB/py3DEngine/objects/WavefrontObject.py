from py3DEngine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject
from py3DEngine.utils.WavefrontFileLoader import WavefrontFileLoader
from py3DEngine.objects.TriangleObject import TriangleObject
import math, cv2, numpy as np
try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print 'No OpenGL libs'

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class WavefrontObject(WavefrontOBJSceneObject):

	def __init__(self, name='Untitled'):

		self._terrain 		= None
		self._resolution	= 4
		self._amplitude		= 100.0
		self._terrainFile 	= ''
		self.__createTerrain( self._resolution, self._terrain )
		
		super(WavefrontObject,self).__init__(name)


	def __createTerrain(self, resolution, terrainMap=None, amplitude=100.0):
		
		height,width 	= terrainMap.shape[:2] if terrainMap is not None else (resolution,resolution)
		nWidthPoints 	= int(round(float(width)/float(resolution)))
		maxNumPoints 	= (width/resolution)*(height//resolution)

		self._points  = []
		for iy, y in enumerate( range(0, height, resolution)):
			for ix, x in enumerate( range(0, width, resolution)):
				xx, yy = float(x)/100.0, float(y)/100.0
				zz = (float(terrainMap[y,x])/float(amplitude) ) if terrainMap is not None else 0
				self._points.append( [xx,yy,zz] )
		self._points = np.array(self._points)

		self._originals = self._points.copy()
		

		self._indexes = []
		for iy, y in enumerate( range(0, height-resolution, resolution)):
			for ix, x in enumerate( range(0, width-resolution, resolution)):
				self._indexes.append(ix+iy*nWidthPoints)
				self._indexes.append(ix+1+iy*nWidthPoints)
				self._indexes.append(ix+(iy+1)*nWidthPoints)

				self._indexes.append(ix+(iy+1)*nWidthPoints)
				self._indexes.append(ix+1+(iy+1)*nWidthPoints)
				self._indexes.append(ix+1+(iy)*nWidthPoints)
		self._indexes = np.array(self._indexes)

		self.__calculateTriangles()

	def __calculateTriangles(self):
		self._triangles = []
		for index in range(0, len(self._indexes), 3):
			i = self._indexes[index]
			ii = self._indexes[index+1]
			iii = self._indexes[index+2]
			p0 = self._points[i]
			p1 = self._points[ii]
			p2 = self._points[iii]

			self._triangles.append( TriangleObject(p0=p0,p1=p1,p2=p2) )
			
	def projectIn(self, cam):
		return [cam.calcPixel(*vertice) for vertice in self._points if vertice[2]<=0.1]



	def updateMesh(self):
		if len(self._originals)>0:
			Tmass 	= self.centerOfMassMatrix
			T 		= self.positionMatrix
			R 		= self.rotationMatrix
			
			self._points = np.array( (np.matrix(self._originals)-Tmass)*R+T )
			self.__calculateTriangles()
		

	def collide_with_ray(self, ray):
		collisions = []
		p0 = ray.points[0]
		for triangle in self._triangles:
			res = triangle.collide_with_ray(ray)
			if res is not None: collisions.append([DistanceBetween(res[0],p0),res])

		if len(collisions)==0: return None
		collisions = sorted(collisions, key=lambda x:x[0] )
		return collisions[0][1]

	def DrawGL(self):
		glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );

		glColor4f(*self.color)

		self.drawCenterOfMass()
		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3, GL_FLOAT, 0, self._points)
		glDrawElements( GL_TRIANGLES, len(self._indexes), GL_UNSIGNED_SHORT, self._indexes)
		glDisableClientState(GL_VERTEX_ARRAY)
		glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );
		super(WavefrontObject, self).DrawGL()


	@property
	def points(self): return self._points		

	@property
	def amplitude(self): return self._amplitude

	@amplitude.setter
	def amplitude(self, value): 
		self._amplitude = value
		self.__createTerrain(self._resolution, self._terrain, self._amplitude)
	
	@property
	def resolution(self): return self._resolution

	@resolution.setter
	def resolution(self, value): 
		self._resolution = value
		self.__createTerrain(self._resolution, self._terrain, self._amplitude)

	@property
	def terrain(self): return self._terrain

	@terrain.setter
	def terrain(self, value):
		self._terrainFile = value
		try:
			self._terrain = cv2.imread(value,0)
		except:
			self._terrain = None

		if value.lower().endswith('.obj'):

			try:
				obj = WavefrontFileLoader(value)
				self._points = np.array(obj.vertices)
				self._originals = self._points.copy()

				self._indexes = []
				for face in obj.faces:
					self._indexes += face
				self._indexes = np.array(self._indexes)-1
				self.updateMesh()
			except:
				print "Was not possible to import the file {0}".format(value)
		else:

			self.__createTerrain(self._resolution, self._terrain, self._amplitude)



	@property
	def wavefrontobject(self):
		obj = super(WavefrontObject, self).wavefrontobject
		
		obj.addProperty('type', 		'WavefrontObject'		)
		obj.addProperty('terrain', 		self._terrainFile 	)
		obj.addProperty('resolution', 	self.resolution 	)
		obj.addProperty('amplitude', 	self.amplitude 		)
		obj.addProperty('indexes', 		self._indexes 		)
		obj.addProperty('npoints', 		len(self._points) 	)

		for p in self._points: obj.addVertice( p )
		for i, p in enumerate(self._originals): obj.addProperty('p_{0}'.format(i), p )

		for index in range(0, len(self._indexes)-2, 3):
			i 	= self._indexes[index] 		+ 1
			ii 	= self._indexes[index+1] 	+ 1
			iii = self._indexes[index+2]	+ 1

			obj.addFace( (i,ii,iii) )

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
	
		self._terrainFile 	= value.getProperty('terrain','')
		self.resolution = int(value.getProperty('resolution',2))
		self.amplitude 	= float(value.getProperty('amplitude',1))
		npoints 		= int(value.getProperty('npoints',0))

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )

		self._indexes 	= np.array(eval(value.getProperty('indexes','[]')))

		points = []
		for i in range(npoints): points.append( value.getVertice(i) )
		self._points = np.array(points)

		try:
			points = []
			for i in range(npoints): points.append( eval(value.getProperty('p_{0}'.format(i))) )
			self._originals = np.array(points)
		except:
			self._originals = self._points.copy()
			print "Old file format imported"

		
		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )
		self.__calculateTriangles()



		
		