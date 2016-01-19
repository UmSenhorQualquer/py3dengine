try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print 'No OpenGL libs'
import math, numpy as np
from py3DEngine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class EllipsoidObject(WavefrontOBJSceneObject):

	_type = 'EllipsoidObject'

	def __init__(self, name='Untitled', fA=1.0, fB=1.0, fC=1.0):
		
		self._fa = fA
		self._fb = fB
		self._fc = fC
		self._points = []
		
		WavefrontOBJSceneObject.__init__(self,name)

		
	def updateMesh(self):
		self._points = []
		
		uiStacks, uiSlices, fA, fB, fC = 10,10, self.fA, self.fB, self.fC
		tStep = np.pi / float(uiSlices);
		sStep = np.pi / float(uiStacks);

		Tmass 	= self.centerOfMassMatrix
		T 		= self.positionMatrix
		R 		= self.rotationMatrix
		
		for t in np.arange( -np.pi/2.0, (np.pi/2.0)+.0001, tStep):
			for s in np.arange( -np.pi, np.pi+.0001, sStep):
				p0 = fA * math.cos(t) * math.cos(s), fB * math.cos(t) * math.sin(s), fC * math.sin(t)
				p1 = fA * math.cos(t+tStep) * math.cos(s), fB * math.cos(t+tStep) * math.sin(s), fC * math.sin(t+tStep)
				
				p0 = np.array( (np.matrix(p0)-Tmass)*R+T )[0]
				p1 = np.array( (np.matrix(p1)-Tmass)*R+T )[0]
		
				self._points.append( p0 )
				self._points.append( p1 )
			

	@property
	def fA(self): return self._fa
	@fA.setter
	def fA(self, value): self._fa = value; self.updateMesh()

	@property
	def fB(self): return self._fb
	@fB.setter
	def fB(self, value): self._fb = value; self.updateMesh()

	@property
	def fC(self): return self._fc
	@fC.setter
	def fC(self, value): self._fc = value; self.updateMesh()




	def DrawGL(self):		
		glColor4f(*self.color)
		glBegin(GL_TRIANGLE_STRIP);
		for i in range(0, len(self._points)-1,2):
			glVertex3f(*self._points[i]);
			glVertex3f(*self._points[i+1]);
		glEnd();
		super(EllipsoidObject, self).DrawGL()
				
	
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

	def normalizedVector(self, a, b): 
		v = np.array([b[0]-a[0],b[1]-a[1],b[2]-a[2]])
		return v/np.linalg.norm(v)

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
		
		fa, fb, fc = self.fA, self.fB, self.fC

		a = (v0**2)/(fa**2) + (v1**2)/(fb**2) + (v2**2)/(fc**2)
		b = (2*x0*v0)/(fa**2) + (2*y0*v1)/(fb**2) + (2*z0*v2)/(fc**2)
		c = (x0**2)/(fa**2) + (y0**2)/(fb**2) + (z0**2)/(fc**2) - 1
		d = (b**2)-(4*a*c)

		if d < 0: return None
		
		d 			= math.sqrt(d)
		hit 		= (-b + d)/(2*a)
		hitsecond 	= (-b - d)/(2*a)
		
		t = hit if hit < hitsecond else hitsecond

		collision = x,y,z = x0+v0*t, y0+v1*t, z0+v2*t
		collision = np.array( (np.matrix(collision)-Tmass)*R+T )[0]
		
		#return the collision point and the collision normal
		return collision, (1.0,0,0)


	def pointIn(self, p):
		Tmass 	= self.centerOfMassMatrix
		T 		= self.positionMatrix
		R 		= self.rotationMatrix
		
		#Apply the inverse transformations of the Ellipse to the point
		x, y, z = np.array( (np.matrix(p)-T)*R.T+Tmass )[0]

		return (x**2/self.fA**2 + y**2/self.fB**2 + z**2/self.fC**2)<=1.0



	@property
	def wavefrontobject(self):
		obj = super(EllipsoidObject, self).wavefrontobject

		obj.addProperty('type', 'EllipsoidObject')
		obj.addProperty('fa', self.fA)
		obj.addProperty('fb', self.fB)
		obj.addProperty('fc', self.fC)

		for i in range(0, len(self._points)-1, 2):
			obj.addVertice( self._points[i]   )
			obj.addVertice( self._points[i+1] )

		for i in range(1, len(self._points)-1):
			if (i % 2)==1:
				obj.addFace( (i,i+1,i+2) )
			else:
				obj.addFace( (i+2,i+1,i) )
		
		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.fA 			= float(value.getProperty('fa'))
		self.fB 			= float(value.getProperty('fb'))
		self.fC 			= float(value.getProperty('fc'))

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )
