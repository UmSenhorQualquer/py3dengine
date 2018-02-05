try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')
from py3dengine.scenes.Scene import Scene

class GLScene(Scene):

	def __drawGLAxis(self):
		# Draw x-axis line.
		glLineWidth(5.0)
		glColor3f( 1, 0, 0 )
		glBegin( GL_LINES ); glVertex3f( 0, 0, 0 ); glVertex3f( 1, 0, 0 ); glEnd()
		# Draw y-axis line.
		glColor3f( 0, 1, 0 )
		glBegin( GL_LINES ); glVertex3f( 0, 0, 0 );glVertex3f( 0, 1, 0 ); glEnd()
		# Draw z-axis line.
		glColor3f( 0, 0, 1 )
		glBegin( GL_LINES ); glVertex3f( 0, 0, 0 ); glVertex3f( 0, 0, 1 ); glEnd()
		glLineWidth(1.0)


	# The main drawing function.
	def DrawGLScene(self):
		cameras = self.cameras
		objects = self.objects
		
		if self.selected_object!=None: self.selected_object.lookFrom()
		
		#self.__drawGLAxis()

		for cam in self.cameras:
			cam.DrawGL();
		for obj in objects: 
			if obj.active: obj.DrawGL();

