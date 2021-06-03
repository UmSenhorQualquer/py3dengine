#!/usr/bin/env pythonw
try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')

import string, sys,  math


class VirtualCamera(object):

	def __init__(self, **args):
		self.color = 1.0,1.0,1.0,0.5
		self.showFaces = False
		

	def __drawGLAxis(self):
		# Draw x-axis line.
		glLineWidth(5.0)
		glColor3f( 1, 0, 0 )
		glBegin( GL_LINES ); glVertex3f( 0, 0, 0 ); glVertex3f( 1, 0, 0 ); glEnd()
		# Draw y-axis line.
		glColor3f( 0, 1, 0 )
		glBegin( GL_LINES ); glVertex3f( 0, 0, 0 ); glVertex3f( 0, 1, 0 ); glEnd()
		# Draw z-axis line.
		glColor3f( 0, 0, 1 )
		glBegin( GL_LINES ); glVertex3f( 0, 0, 0 ); glVertex3f( 0, 0, 1 ); glEnd()
		glLineWidth(1.0)


	def __updatcameraMatrix(self, angle, decimals):
		decimals = float(decimals)*0.01
		fy = math.tan(math.radians(angle+decimals) )*1000.0
		self.cameraMatrix[1,1] = self.cameraMatrix[0,0] = float(fy)

		# Warn OpenGL that the projection matrix will be changed
		#glMatrixMode(GL_PROJECTION)
		# Reset The Projection Matrix
		#glLoadIdentity()
		# Change the projection matrix
		#gluPerspective(angle+decimals, float(self.width)/float(self.height), 0.1, 800.0)
		# Get back to the model matrix
		#glMatrixMode(GL_MODELVIEW)

		

		
	def lookFrom(self):
		glRotatef( -self.rotationAngleDegrees, *self.rotationVector)
		glTranslatef( -self.positionTuple[0], -self.positionTuple[1],-self.positionTuple[2] )

	def DrawGL(self, objects=[]):
		"""
		Draw the marker in the OpenGL
		"""
		glPushMatrix()
		#self.__drawGLAxis()
		
		# glPushAttrib is done to return everything to normal after drawing
		glPushAttrib(GL_ENABLE_BIT);
		glLineStipple(1, 0x00FF)
		glEnable(GL_LINE_STIPPLE)

		p0 = self.positionTuple
		p1 = self.calcPoint( 0,0, 								 self.maxFocalLength )
		p2 = self.calcPoint( self.cameraWidth,0, 				 self.maxFocalLength )
		p3 = self.calcPoint( self.cameraWidth,self.cameraHeight, self.maxFocalLength )
		p4 = self.calcPoint( 0,self.cameraHeight, 				 self.maxFocalLength )

		glColor4f(*self._color)
		if self._showFaces:
			
			glBegin(GL_TRIANGLES)
			glVertex3f(*p0)
			glVertex3f(*p1)
			glVertex3f(*p2)
			glEnd()
			glBegin(GL_TRIANGLES)
			glVertex3f(*p0)
			glVertex3f(*p2)
			glVertex3f(*p3)
			glEnd()
			glBegin(GL_TRIANGLES)
			glVertex3f(*p0)
			glVertex3f(*p3)
			glVertex3f(*p4)
			glEnd()
			glBegin(GL_TRIANGLES)
			glVertex3f(*p0)
			glVertex3f(*p4)
			glVertex3f(*p1)
			glEnd()

		
		for p in [p1,p2,p3, p4]:
			glBegin(GL_LINES)
			glVertex3f(*p0)
			glVertex3f(*p)
			glEnd()

		for a, b in [(p1,p2),(p2,p3),(p3,p4),(p4,p1)]:
			glBegin(GL_LINES)
			glVertex3f(*a)
			glVertex3f(*b)
			glEnd()

		glPopAttrib()

		for ray in self.rays:
			#ray.collide(objects) 
			ray.DrawGL()
		glPopMatrix()

		
			

	


	@property
	def color(self): return self._color
	@color.setter
	def color(self, value): self._color = value

	@property
	def showFaces(self): return self._showFaces
	@showFaces.setter
	def showFaces(self, value): self._showFaces = value

