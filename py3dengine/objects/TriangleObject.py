try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
import math, numpy as np
from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class TriangleObject(WavefrontOBJSceneObject):

	_type = 'TriangleObject'

	def __init__(self, name='Untitled', 
		p0=(-20.0, 0.0, -20.0), p1=(20, 0.0, -20.0),p2=(20, 0.0, 20)):
		WavefrontOBJSceneObject.__init__(self,name)

		self._point0 = p0
		self._point1 = p1
		self._point2 = p2
		self.__calculatePlane()

		
	def __calculatePlane(self):
		ax, ay, az = self._point0
		bx, by, bz = self._point1
		cx, cy, cz = self._point2

		self._a = ((by-ay)*(cz-az))-((cy-ay)*(bz-az))
		self._b = ((bz-az)*(cx-ax))-((cz-az)*(bx-ax))
		self._c = ((bx-ax)*(cy-ay))-((cx-ax)*(by-ay))
		self._d = ((self._a*ax)+(self._b*ay)+(self._c*az))

	@property
	def point0(self): return self._point0
	@point0.setter
	def point0(self, value): self._point0 = value; self.__calculatePlane()

	@property
	def point1(self): return self._point1
	@point1.setter
	def point1(self, value): self._point1 = value; self.__calculatePlane()

	@property
	def point2(self): return self._point2
	@point2.setter
	def point2(self, value): self._point2 = value; self.__calculatePlane()

	@property
	def normal(self): 
		a = np.array( [self._a, self._b, self._c] )
		return a/np.linalg.norm(a)


	def DrawGL(self):
		glColor4f(*self.color)
		glBegin(GL_TRIANGLES)
		glVertex3f(*self.point0); 
		glVertex3f(*self.point1)
		glVertex3f(*self.point2)
		glEnd()

		super(TriangleObject, self).DrawGL()
		
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
		p0, p1 = ray.points
		x0, y0, z0 = p0
		x1, y1, z1 = p1
		v0, v1, v2 	= x1-x0, y1-y0, z1-z0
		d1 = ( (self._a*v0)+(self._b*v1)+(self._c*v2) )
		

		if d1==0: return None
		d0 = (self._d-(self._a*x0)- (self._b*y0)-(self._c*z0) )
		t = d0 / d1

		if t<0: return None
		
		collision = x,y,z = x0+v0*t, y0+v1*t, z0+v2*t

		#print 'dist',DistanceBetween(collision,p0)
		if  DistanceBetween(collision,p0)>0.0001 and \
		 	self.__point_in_triangle( 
				np.array(self.point0),
				np.array(self.point1),
				np.array(self.point2),
				np.array([x,y,z]) ):
			return (x,y,z), self.normal

		return None





	@property
	def wavefrontobject(self):
		obj = super(TriangleObject, self).wavefrontobject

		obj.addProperty('type', 'TriangleObject')
		obj.addVertice( self.point0 )
		obj.addVertice( self.point1 )
		obj.addVertice( self.point2 )

		obj.addFace( (1,2,3) )

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.point0 			= value.getVertice(0)
		self.point1 			= value.getVertice(1)
		self.point2 			= value.getVertice(2)

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )

