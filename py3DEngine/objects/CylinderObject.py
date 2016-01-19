try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print 'No OpenGL libs'
import math, numpy as np
from py3DEngine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject


def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class CylinderObject(WavefrontOBJSceneObject):

	_type = 'CylinderObject'

	def __init__(self, name='Untitled', fA=1.0, fB=1.0, height=1.0):
		WavefrontOBJSceneObject.__init__(self,name)

		self._position = (0.0,0.0,0.0)
		self._fa = fA
		self._fb = fB
		self._cylinderHeight = height
		

		self.__calculatePlane()

		
	def __calculatePlane(self):
		self._topPoints = []
		self._bottomPoints = []

		uiSlices = 10
		fA, fB = self.fA, self.fB
		tStep = np.pi / float(uiSlices)
		for rad in np.arange(0, np.pi*2, tStep): 
			p0 = math.cos(rad)*fA, math.sin(rad)*fB, self._cylinderHeight/2
			p1 = math.cos(rad)*fA, math.sin(rad)*fB, -self._cylinderHeight/2
			self._topPoints.append( 	p0 )
			self._bottomPoints.append( 	p1 )
			
		


	@property
	def fA(self): return self._fa
	@fA.setter
	def fA(self, value): self._fa = value; self.__calculatePlane()

	@property
	def fB(self): return self._fb
	@fB.setter
	def fB(self, value): self._fb = value; self.__calculatePlane()

	@property
	def cylinderHeight(self): return self._cylinderHeight
	@cylinderHeight.setter
	def cylinderHeight(self, value): self._cylinderHeight = value; self.__calculatePlane()


	"""
	@property
	def normal(self): 
		a = np.array( [self._a, self._b, self._c] )
		return a/np.linalg.norm(a)
	"""

	def DrawGL(self):
		glColor4f(*self.color)
		
		glBegin(GL_TRIANGLE_FAN);
		glVertex3f(0,0,self._cylinderHeight/2)
		for i in range(len(self._topPoints)): glVertex3f(*self._topPoints[i])
		glVertex3f(*self._topPoints[0])
		glEnd();

		glBegin(GL_TRIANGLE_FAN);
		glVertex3f(0,0,-self._cylinderHeight/2)
		for i in range(len(self._bottomPoints)): glVertex3f(*self._bottomPoints[i])
		glVertex3f(*self._bottomPoints[0])
		glEnd();
		
		glBegin(GL_QUAD_STRIP);
		for i in range(len(self._topPoints)): 
			glVertex3f(*self._topPoints[i])
			glVertex3f(*self._bottomPoints[i])
		glVertex3f(*self._topPoints[0])
		glVertex3f(*self._bottomPoints[0])
		glEnd();

		super(CylinderObject, self).DrawGL()

		
	def __same_side(self, p1,p2,A,B):
		cp1 = np.cross(B-A, p1-A)
		cp2 = np.cross(B-A, p2-A)
		if np.dot(cp1, cp2)>=0: return True
		return False;

	def __point_in_triangle(self, A, B, C, P):
		if self.__same_side(P, A, B, C) and self.__same_side(P, B, A, C) and self.__same_side(P, C, A, B):
			vc1 = np.cross(A-B, A-C)
			if abs(np.dot(A-P, vc1)) <= .01: return True;
		return False

	def collide_with_ray(self, ray):
		p0 = ray.points[0]
		p1 = ray.points[1]

		Tmass 	= self.centerOfMassMatrix
		T 		= self.positionMatrix
		R 		= self.rotationMatrix
		
		#Apply the inverse transformations of the Ellipse to the ray points
		p0 = x0, y0, z0 = np.array( (np.matrix(p0)-T)*R.T+Tmass )[0]
		p1 = np.array( (np.matrix(p1)-T)*R.T+Tmass )[0]

		#Normalize the vector of the rotated ray
		v0, v1, v2 	= self.normalizedVector(p0, p1)

		#TODO
		"""
		1 = (( (x0+k*vx)**2)/(r**2)) + ((y0+k*vy**2)/(r**2))

		r**2 = (x0**2 + 2k*vx + (k*vx)**2) + (y0**2 + 2k*vy + (k*vy)**2)
		r**2 - x0**2 - y0**2 = k( vx+vx**2)
		(x0 + kvx) * (x0+kvx) = x0**2 + 2kvx + kvx**2


		
		v1 = v0+k*v
		x1 = x0+k*vx
		"""
		
		return None





	@property
	def wavefrontobject(self):
		obj = super(CylinderObject, self).wavefrontobject

		obj.addProperty('type', 'CylinderObject')
		obj.addProperty('fa', self.fA)
		obj.addProperty('fb', self.fB)
		obj.addProperty('height', self.cylinderHeight)

		for i in range(0, len(self._topPoints), 1):
			obj.addVertice( self._topPoints[i]   )

		for i in range(1, len(self._topPoints)+2):
			obj.addFace( (i,i+1,i+2) )
			
		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.fA 			= float(value.getProperty('fa'))
		self.fB 			= float(value.getProperty('fb'))
		self.cylinderHeight = float(value.getProperty('height'))

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )