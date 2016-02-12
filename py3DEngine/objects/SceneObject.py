import numpy as np
import py3DEngine.thirdparty.transformations as trans
try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')


class SceneObject(object):

	def __init__(self, name='Untitled'):

		
		self.parentObj 		= None
		self.active 		= True
		self.name 			= name
		self.color 			= 0,0,1,1
		self._incandescence = None
		self._specularity 	= None
		self._reflectivity 	= None
		self._childs 		= []
		self._refraction 	= None
		
		self._obj_position 		= [0, 0, 0]
		self._obj_centerOfMass 	= [0, 0, 0]
		self.rotation 			= [0, 1, 0, 0]

		self.updateMesh()

		

	def cleanChilds(self): 
		for child in self._childs: child.parentObj = None
		self._childs = []

	def addChild(self, child):
		child.parentObj = self
		self._childs.append(child)

	
	def updateMesh(self): pass

	##################################################################################################################
	######## Transformations #########################################################################################
	##################################################################################################################


	def Translate(self, pos):
		self.positionMatrix += np.matrix(pos)
		for child in self._childs: child.Translate(pos)

	def Rotate(self, angleX=0, angleY=0, angleZ=0):
		Rx = trans.rotation_matrix( angleX, (1.0,0.0,0) )
		Ry = trans.rotation_matrix( angleY, (0,1.0,0) 	)
		Rz = trans.rotation_matrix( angleZ, (0,0.0,1.0) )
		self._R = self.rotationMatrix * np.matrix(Rx)*np.matrix(Ry)*np.matrix(Rz)
		self.updateMesh()

	def projectIn(self, camera): return []


	def collide_with_ray(self, ray): return False
	def pointIn(self, p): 			 return False

	##################################################################################################################
	######## Draw ####################################################################################################
	##################################################################################################################


	def drawCenterOfMass(self):
		glPushMatrix()
		
		glTranslatef(*self.position)
		#glTranslatef(*self.centerOfMass)

		w = 0.08
		
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

	def DrawGL(self): 
		self.drawCenterOfMass()
		#for x in self._childs: x.DrawGL()
		pass




	##################################################################################################################
	######## PROPERTIES ##############################################################################################
	##################################################################################################################
	@property
	def refraction(self): return self._refraction
	@refraction.setter
	def refraction(self, value):  self._refraction = value



	@property
	def incandescence(self): return self._incandescence
	@incandescence.setter
	def incandescence(self, value): self._incandescence = value

	@property
	def specularity(self): return self._specularity
	@specularity.setter
	def specularity(self, value): self._specularity = value

	@property
	def reflectivity(self): return self._reflectivity
	@reflectivity.setter
	def reflectivity(self, value): self._reflectivity = value

	@property
	def name(self): return self._name
	@name.setter
	def name(self, value): self._name = value

	@property
	def color(self): return self._color
	@color.setter
	def color(self, value): self._color = value

	@property
	def parentObj(self): return self._parentObj
	@parentObj.setter
	def parentObj(self, value):  self._parentObj = value



	@property
	def position(self): return self._obj_position
	@position.setter
	def position(self, value):  self._obj_position = value; self.updateMesh()

	@property
	def rotation(self): return self._obj_rotation
	@rotation.setter
	def rotation(self, value):   
		self._obj_rotation = value; 
		angle 	= self._obj_rotation[3]
		axis 	= list(self._obj_rotation)[:3]
		self._R = trans.rotation_matrix(angle, axis)
		self.updateMesh()

	@property
	def centerOfMass(self): return self._obj_centerOfMass
	@centerOfMass.setter
	def centerOfMass(self, value):  self._obj_centerOfMass = value; self.updateMesh()

	

	

	@property
	def positionMatrix(self): return np.matrix( self.position )
	@positionMatrix.setter
	def positionMatrix(self, value): self.position = value.tolist()[0]
	
	@property
	def centerOfMassMatrix(self): return np.matrix( self.centerOfMass )

	@property
	def rotationMatrix(self): return self._R
		


	@property
	def active(self): 			return self._active
	@active.setter
	def active(self, value): 	self._active = value

