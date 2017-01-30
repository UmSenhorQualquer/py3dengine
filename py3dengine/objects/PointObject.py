try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
import math, numpy as np
from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class PointObject(WavefrontOBJSceneObject):

	_type = 'PointObject'

	def __init__(self, name='Untitled', p0=(0.0, 0.0,0.0)):
		WavefrontOBJSceneObject.__init__(self,name)
		self._radius = 10.0
		self._point = p0

	@property
	def point(self): return self._point
	@point.setter
	def point(self, value): self._point = value


	def DrawGL(self):
		glPointSize(self._radius)
		glColor4f(*self.color)
		glBegin(GL_POINTS)
		glVertex3f(*self.point)
		glEnd()
		glPointSize(1.0)
		
		#super(PointObject, self).DrawGL()
		
	

	def collide_with_ray(self, ray): return None





	@property
	def wavefrontobject(self):
		obj = super(PointObject, self).wavefrontobject

		obj.addProperty('type', 'PointObject')
		obj.addVertice( self.point )
		obj.addPoint(1)

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.point 			= value.getVertice(0)

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )