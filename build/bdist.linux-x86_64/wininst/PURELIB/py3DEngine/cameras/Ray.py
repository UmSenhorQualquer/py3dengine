try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print 'No OpenGL libs'
import math, itertools
import numpy as np

def lin3d_distance(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2 )



class Ray(object):

	def __init__(self, p0, p1, color=(1.,1.,1.), depth=1 ): 
		self._a, self._b = p0, p1
		self.color = color

		self._depth 	= depth #How many rays can be calculated after a collision
		self.children 	= None  #Ray reflected or refracted from a collision

	@property
	def vector(self): return np.array([self._b[0]-self._a[0], self._b[1]-self._a[1], self._b[2]-self._a[2]])

	@property
	def normalizedVector(self): 
		a = self.vector
		return a/np.linalg.norm(a)


	def fresnel_refraction(self, normal, n1=1.00027712, n2=1.33):
		vector = self.vector
		normal = normal/np.linalg.norm(normal)
		nvector = vector/np.linalg.norm(vector)

		n = n1/n2
		dot = np.dot(nvector, normal)
		c = np.sqrt(1 - n**2 * (1 - dot**2))
		sign = 1 if dot >= 0.0 else -1
		refraction = n * nvector + sign*(c - sign*n*dot) * normal
		return refraction/np.linalg.norm(refraction)
		

	@property
	def children(self): return self._children
	@children.setter
	def children(self, value): self._children = value
	


	@property
	def color(self): return self._color
	@color.setter
	def color(self, value): self._color = value[:3]
	

	@property
	def raydepth(self): return self._depth
	@raydepth.setter
	def raydepth(self, value): self._depth = value

	@property
	def endPoint(self): return self._children.endPoint if self._children else self._b 

	
	@property
	def points(self): return self._a, self._b

	@points.setter
	def points(self, value):  self._a, self._b = value

	@property 
	def length(self):
		return lin3d_distance(self._a, self._b)


	def collidePlanZ(self, z):
		p0, p1 = self.points
		x0, y0, z0 = p0
		x1, y1, z1 = p1
		v0, v1, v2 	= x1-x0, y1-y0, z1-z0

		t = (z-z0)/v2		
		x = x0+t*v0
		y = y0+t*v1
		z = z0+t*v2

		self._b = x,y,z
		return x,y,z

		if z>self._b[2]:
			if self._children: 
				return self._children.collidePlanZ(z)
			else:
				return self._b
		else:
			self._b = x,y,z
			return x,y,z
		
	def collide(self, objects):
		collisions = []
		for obj in objects:
			collision = obj.collide_with_ray(self)
			if collision!=None:
				b, normal = collision
				dist = lin3d_distance(self._a, b)
				collisions.append( (dist, b, normal, obj) )

		if len(collisions)>0:
			collisions = sorted(collisions, key=lambda x:x[0])
			dist, b, normal, obj = collisions[0]
			self._b = b


			self.color = obj.color

			#############################################
			#Reflect or refract image
			if self._depth>0 and obj.refraction!=None:
				if obj.refraction==None:
					i = self.vector; n = normal; r = i-(n*2*np.dot(i,n)); c = np.array(b)+r
				else:
					c = self.fresnel_refraction(normal, n2=obj.refraction)*10
					c += b

				if self.children!=None: self.children.points = [b, c]
				else: self.children = Ray(b, c, depth=self._depth-1)

				if obj.refraction!=None: 
					objs = [o for o in objects if o!=obj]
					self.children.collide(objs)
			else:
				self._children=None
			
			#############################################
			return dist, b, obj
		else:
			self.children=None
			return None
		
	def DrawGL(self):
		a, b = self.points

		glColor3f( *self.color )
		glBegin(GL_LINES)
		glVertex3f(*a)
		glVertex3f(*b)
		glEnd()

		if self._children!=None: self._children.DrawGL()






	@staticmethod
	def __FindClosestPointBetweenRays(ray0, ray1,clamp=True):
		''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
		Return distance, and the two closest points
		Use the clamp option to limit results to line segments
		'''
		v0 = ray0.points
		v1 = ray1.points

		a0, a1 = np.array(v0[0]), np.array(v0[1])
		b0, b1 = np.array(v1[0]), np.array(v1[1])
		A = a1 - a0
		B = b1 - b0
		_A = A / np.linalg.norm(A)
		_B = B / np.linalg.norm(B)
		
		cros = np.cross(_A, _B);
		# If denominator is 0, lines are parallel
		denom = np.linalg.norm(cros)**2
		if (denom == 0): return None
		# Calculate the dereminent and return points
		t = (b0 - a0);
		det0 = np.linalg.det([t, _B, cros])
		det1 = np.linalg.det([t, _A, cros])
		t0 = det0/denom;
		t1 = det1/denom;
		pA = a0 + (_A * t0);
		pB = b0 + (_B * t1);
		# Clamp results to line segments if requested
		if clamp:
			if t0 < 0: pA = a0
			elif t0 > np.linalg.norm(A): pA = a1
			if t1 < 0: pB = b0
			elif t1 > np.linalg.norm(B): pB = b1
		d = np.linalg.norm(pA-pB)
		#return d,pA,pB, ( (pB[0]+pB[0])/2, (pA[1]+pB[1])/2, (pA[2]+pB[2])/2 )
		return d,pA,pB, ( (pA[0]+pB[0])/2, (pA[1]+pB[1])/2, (pA[2]+pB[2])/2 )





	@staticmethod
	def FindClosestPointBetweenRays(ray0, ray1):
		''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
	    Return distance, and the two closest points
	    Use the clamp option to limit results to line segments
		'''
		rays0 = []
		rays1 = []

		while ray0!=None: rays0.append(ray0); ray0=ray0.children
		while ray1!=None: rays1.append(ray1); ray1=ray1.children

		results = []
		for ray0, ray1 in itertools.product(rays0, rays1):
			res = Ray.__FindClosestPointBetweenRays(ray0, ray1)
			results.append( res )

		if len(results)==0: return None
		results = sorted(results, key=lambda x:x[0])
		return results[0]
