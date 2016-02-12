try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
import math, numpy as np
from py3DEngine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject


def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class EllipseObject(WavefrontOBJSceneObject):

	_type = 'EllipseObject'

	def __init__(self, name='Untitled', fA=1.0, fB=1.0):
		WavefrontOBJSceneObject.__init__(self,name)

		self._position = (0.0,0.0,0.0)
		self._fa = fA
		self._fb = fB
		self._points = []
		self.__calculatePlane()

		
	def __calculatePlane(self):
		self._points = []
		
		uiSlices = 10
		fA, fB = self.fA, self.fB
		tStep = np.pi / float(uiSlices)
		for rad in np.arange(0, np.pi*2, tStep): self._points.append( (math.cos(rad)*fA, math.sin(rad)*fB,0) )
		

	@property
	def fA(self): return self._fa
	@fA.setter
	def fA(self, value): self._fa = value; self.__calculatePlane()

	@property
	def fB(self): return self._fb
	@fB.setter
	def fB(self, value): self._fb = value; self.__calculatePlane()


	"""
	@property
	def normal(self): 
		a = np.array( [self._a, self._b, self._c] )
		return a/np.linalg.norm(a)
	"""

	def DrawEllipse(self,uiStacks, uiSlices, fA, fB, fC):
		tStep = np.pi / float(uiSlices);
		sStep = np.pi / float(uiStacks);
		#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
		for t in np.arange( -np.pi/2.0, (np.pi/2.0)+.0001, tStep):
			glBegin(GL_LINE_LOOP);
			for s in np.arange( -np.pi, np.pi+.0001, sStep):
				glVertex3f(fA * math.cos(t) * math.cos(s), fB * math.cos(t) * math.sin(s), fC * math.sin(t));
				glVertex3f(fA * math.cos(t+tStep) * math.cos(s), fB * math.cos(t+tStep) * math.sin(s), fC * math.sin(t+tStep));
			glEnd();

	def DrawGL(self):
		glColor4f(*self.color)
		
		glBegin(GL_TRIANGLE_FAN);
		glVertex3f(0,0,0)
		for i in range(len(self._points)): glVertex3f(*self._points[i])
		glVertex3f(*self._points[0])
		glEnd();

		super(EllipseObject, self).DrawGL()
	
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
		return None
		pass
		x0, y0, z0 = p0
		x1, y1, z1 = p1
		v0, v1, v2 	= x1-x0, y1-y0, z1-z0
		
		"""
		ray_normal = v0, v1, v2
		float rayEllipsoidIntersect(Ogre::Vector3 ray_origin, Ogre::Vector3 ray_normal, Ogre::Vector3 ellipsoid_origin, Ogre::Vector3 ellipsoid_radius) {
	    ray_origin -= ellipsoid_origin;
	    ray_normal.normalise();
	    float a = ((ray_normal.x*ray_normal.x)/(ellipsoid_radius.x*ellipsoid_radius.x))
	            + ((ray_normal.y*ray_normal.y)/(ellipsoid_radius.y*ellipsoid_radius.y))
	            + ((ray_normal.z*ray_normal.z)/(ellipsoid_radius.z*ellipsoid_radius.z));
	    float b = ((2*ray_origin.x*ray_normal.x)/(ellipsoid_radius.x*ellipsoid_radius.x))
	            + ((2*ray_origin.y*ray_normal.y)/(ellipsoid_radius.y*ellipsoid_radius.y))
	            + ((2*ray_origin.z*ray_normal.z)/(ellipsoid_radius.z*ellipsoid_radius.z));
	    float c = ((ray_origin.x*ray_origin.x)/(ellipsoid_radius.x*ellipsoid_radius.x))
	            + ((ray_origin.y*ray_origin.y)/(ellipsoid_radius.y*ellipsoid_radius.y))
	            + ((ray_origin.z*ray_origin.z)/(ellipsoid_radius.z*ellipsoid_radius.z))
	            - 1;

	    float d = ((b*b)-(4*a*c));
	    if ( d < 0 ) { return -1; }
	    else { d = Ogre::Math::Sqrt(d); }
	    float hit = (-b + d)/(2*a);
	    float hitsecond = (-b - d)/(2*a);

	    //DEBUG
	    //std::cout << "Hit1: " << hit << " Hit2: " << hitsecond << std::endl;

	    if( hit < hitsecond) { return hit; }
	    else { return hitsecond; }
		}
		"""

		return None





	@property
	def wavefrontobject(self):
		obj = super(EllipseObject, self).wavefrontobject

		obj.addProperty('type', 'EllipseObject')
		obj.addProperty('fa', self.fA)
		obj.addProperty('fb', self.fB)

		for i in range(0, len(self._points), 1):
			obj.addVertice( self._points[i]   )

		for i in range(1, len(self._points)+2):
			obj.addFace( (i,i+1,i+2) )
			
		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):		
		self.fA 			= float(value.getProperty('fa'))
		self.fB 			= float(value.getProperty('fb'))

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )
