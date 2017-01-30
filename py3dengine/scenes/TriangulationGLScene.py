try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
import itertools
import numpy as np
from py3DEngine.scenes.GLScene import GLScene

def closestDistanceBetweenLines(a0,a1,b0,b1,clamp=False):
	''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
	    Return distance, and the two closest points
	    Use the clamp option to limit results to line segments
	'''
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
	return d,pA,pB


class TriangulationGLScene(GLScene):

	def getIntersection(self, z=1.7):
		lines = []
		for cam in self.cameras:
			rays = cam.rays
			for ray in rays:
				line = ray.points
				lines.append( line )

		if len(lines)==0: return None

		if len(lines)==1:
			l = lines[0]
			p1,p2 = l
			lines.append( [(p1[0],p1[1],-1.7), (p2[0],p2[1],-z)] )

		points = []
		for line1, line2 in itertools.permutations(lines, 2):
			res = closestDistanceBetweenLines( np.float32(line1[0]), np.float32(line1[1]), 
				np.float32(line2[0]), np.float32(line2[1]) )
			points.append(res[1])
			points.append(res[2])
			
		avgX, avgY, avgZ = 0.0,0.0,0.0
		for p in points:
			avgX += p[0]
			avgY += p[1]
			avgZ += p[2]

		n = len(points)
		avgX /= n
		avgY /= n
		avgZ /= n
		p0 = avgX, avgY, avgZ

		return avgX,avgY,avgZ


	# The main drawing function.
	def DrawGLScene(self):
		for cam in self.cameras: cam.DrawGL(  );
		for obj in self.objects: 
			if obj.active: obj.DrawGL();

		for p in self._points: self.drawPoint(p)


	def drawPoint(self, p):
		glPushMatrix()
		
		glTranslatef(*p)
		
		w = 0.1

		glColor3f(1,1,1,1)
		
		glBegin( GL_TRIANGLES );
		glVertex3f( 0.0, w, 0.0 );
		glVertex3f( -w, -w, w );
		glVertex3f( w, -w, w);

		glVertex3f( 0.0, w, 0.0);
		glVertex3f( -w, -w, w);
		glVertex3f( 0.0, -w, -w);

		glVertex3f( 0.0, w, 0.0);
		glVertex3f( 0.0, -w, -w);
		glVertex3f( w, -w, w);

		glVertex3f( -w, -w, w);
		glVertex3f( 0.0, -w, -w);
		glVertex3f( w, -w, w);
		glEnd();

		glPopMatrix()