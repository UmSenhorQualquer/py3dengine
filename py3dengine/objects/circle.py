from py3dengine.objects.base_object import SceneObject

try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
import math, numpy as np
from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject


def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class CircleObject(SceneObject):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._fa = kwargs.get('fA', 1.0)
		self._fb = kwargs.get('fB', 1.0)

		self.__calculate_plane()

	@classmethod
	def from_json(cls, json):
		obj = cls()
		return obj

	def to_json(self, data={}):
		data = super().to_json(data)
		data['fa'] = self.fA
		data['fb'] = self.fB
		return data
		
	def __calculate_plane(self):
		self._points = []

		ui_slices = 10
		fA, fB = self.fA, self.fB
		t_step = np.pi / float(ui_slices)
		for rad in np.arange(0, np.pi*2, t_step): 
			p0 = math.cos(rad)*fA+self.position[0], math.sin(rad)*fB+self.position[1], self.position[2]
			self._points.append(p0)

	def updateMesh(self):
		self.__calculate_plane()

	@property
	def fA(self): return self._fa
	@fA.setter
	def fA(self, value): self._fa = value; self.__calculate_plane()

	@property
	def fB(self): return self._fb
	@fB.setter
	def fB(self, value): self._fb = value; self.__calculate_plane()


	def DrawGL(self):

		glColor4f(*self.color)
		
		glBegin(GL_TRIANGLE_FAN)
		glVertex3f(*self.position)
		for i in range(len(self._points)):
			glVertex3f(*self._points[i])
		glVertex3f(*self._points[0])
		glEnd()

		super().DrawGL()

		
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

		Tmass 	= self.center_of_mass_matrix
		T 		= self.position_matrix
		R 		= self.rotation_matrix
		
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
		obj = super(CircleObject, self).wavefrontobject

		obj.addProperty('type', self._type)
		obj.addProperty('fa', self.fA)
		obj.addProperty('fb', self.fB)

		for i in range(0, len(self._points), 1):
			obj.addVertice(self._points[i])

		for i in range(1, len(self._points) + 2):
			obj.addFace( (i,i+1,i+2) )
			
		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.fA = float(value.getProperty('fa'))
		self.fB = float(value.getProperty('fb'))

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value)