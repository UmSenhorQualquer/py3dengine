from py3DEngine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject
from py3DEngine.objects.RectangleObject import RectangleObject
try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')

class MarkerObject(RectangleObject):

	def __init__(self, name='Untitled', 
		p0=(0,0,0), p1=(1,0,0), p2=(1,0,1), p3=(0,0,1), p4=(0,1,1)):
		super(MarkerObject,self).__init__(name, p0, p1, p2, p3)

		self.point4 = p4

	@property
	def point4(self): return self._point4
	@point4.setter
	def point4(self, value): self._point4 = value


	@property
	def wavefrontobject(self):
		obj = WavefrontOBJSceneObject.wavefrontobject.fget(self)

		obj.addProperty('type', 'MarkerObject')
		obj.addVertice( self.point0 )
		obj.addVertice( self.point1 )
		obj.addVertice( self.point2 )
		obj.addVertice( self.point3 )
		obj.addVertice( self.point4 )
		obj.addFace( (1,2,3,4,5) )
		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.point4 			= value.getVertice(4)

		RectangleObject.wavefrontobject.fset(self, value )

	def DrawGL(self):
		glColor4f(*self.color)
		glBegin(GL_POLYGON)
		glVertex3f(*self.point0)
		glVertex3f(*self.point1)
		glVertex3f(*self.point2)
		glVertex3f(*self.point3)
		glVertex3f(*self.point4)
		glEnd()


