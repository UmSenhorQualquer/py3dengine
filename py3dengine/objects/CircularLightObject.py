try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
import math, numpy as np
from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject
from .CircleObject import CircleObject
from ..cameras.Ray import Ray

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class CircularLightObject(CircleObject):

	_type = 'CircularLightObject'

	def __init__(self, name='Untitled', fA=1.0, fB=1.0, focal_point=-1000, rays_step=1.0):

		self._focal_point = focal_point
		self._rays_step = rays_step
		self._rays = []

		CircleObject.__init__(self, name, fA, fB)


	def calculate_rays(self):
		self._rays = []

		c0 = self.position[0], self.position[1], self.position[2]+self.focal_point

		ui_slices = 10
		fA, fB = self.fA, self.fB
		t_step = np.pi / float(ui_slices)
		for step in np.arange(1.0, 0, -self.rays_step):
			for rad in np.arange(0, np.pi * 2, t_step):
				p0 = math.cos(rad) * fA * step+ self.position[0], math.sin(rad) * fB * step+ self.position[1], self.position[2]
				r = Ray(c0, p0, depth=2)
				self._rays.append(r)

	def DrawGL(self):
		super().DrawGL()
		for r in self._rays:
			r.DrawGL()



	@property
	def focal_point(self):
		return self._focal_point

	@property
	def rays_step(self):
		return self._rays_step

	@property
	def rays(self):
		return self._rays