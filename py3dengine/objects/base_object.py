import numpy as np
import py3dengine.thirdparty.transformations as trans
try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')

from .WavefrontOBJSceneObject import WavefrontOBJSceneObject

class SceneObject(WavefrontOBJSceneObject):

	def __init__(self, *args, **kwargs):

		self.name = args[0] if len(args) > 0 else kwargs.get('name', 'Untitled')
		self.color = kwargs.get('color', (0, 0, 1, 1))

		self._obj_uid = None
		self._parent_object = None
		self.parent_object = None
		self.active = True
		self._incandescence = None
		self._specularity = None
		self._reflectivity = None
		self._children = []
		self._refraction = None

		self._obj_position = kwargs.get('position', [0, 0, 0])
		self._obj_center_of_mass = kwargs.get('center_of_mass', [0, 0, 0])
		self.rotation = kwargs.get('rotation', [0, 1, 0, 0])

		self.updateMesh()

		

	def cleanChilds(self): 
		for child in self._children: child.parent_object = None
		self._children = []

	def add_child(self, child):
		child._parent_object = self
		self._children.append(child)

	def remove_child(self, child):
		child._parent_object = None
		self._children.remove(child)


	
	def updateMesh(self): pass

	##################################################################################################################
	######## Transformations #########################################################################################
	##################################################################################################################


	def Translate(self, pos):
		self.position_matrix += np.matrix(pos)
		for child in self._children: child.Translate(pos)

	def Rotate(self, angleX=0, angleY=0, angleZ=0):
		Rx = trans.rotation_matrix( angleX, (1.0,0.0,0) )
		Ry = trans.rotation_matrix( angleY, (0,1.0,0) 	)
		Rz = trans.rotation_matrix( angleZ, (0,0.0,1.0) )
		self._R = (self.rotation_matrix)*np.matrix(Rx)*np.matrix(Ry)*np.matrix(Rz)
		self.updateMesh()

		#for child in self._childs: child.Rotate(angleX, angleY, angleZ)
		#for child in self._childs: 
		#	child._R *= self._R
		#	self.updateMesh()


	def projectIn(self, camera): return []


	def collide_with_ray(self, ray): return False
	def pointIn(self, p): 			 return False

	##################################################################################################################
	######## Draw ####################################################################################################
	##################################################################################################################


	def drawcenter_of_mass(self):
		glPushMatrix()
		
		glTranslatef(*self.position)
		#glTranslatef(*self.center_of_mass)

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
		#self.drawcenter_of_mass()
		#for x in self._childs: x.DrawGL()
		pass

	@classmethod
	def from_json(cls, json):
		obj = cls()

		obj.name = json.get('name', None)
		obj.color = json.get('color', None)
		obj.active = json.get('active', None)
		obj.rotation = json.get('rotation', None)
		obj.position = json.get('position', None)
		obj.parent_object = json.get('parent_object', None)
		obj.incandescence = json.get('incandescence', None)
		obj.specularity = json.get('specularity', None)
		obj.reflectivity = json.get('reflectivity', None)
		obj.rotation = json.get('rotation', None)
		obj.center_of_mass = json.get('center-of-mass', None)
		obj.children_objects = json.get('children', [])

		return obj

	def to_json(self, data={}):

		data['type'] = type(self).__name__
		data['name'] = self.name
		data['color'] = self.color
		data['active'] = self.active
		data['rotation'] = self.rotation
		data['position'] = self.position
		data['parent-object'] = self.parent_object
		data['incandescence'] = self.incandescence
		data['specularity'] = self.specularity
		data['reflectivity'] = self.reflectivity
		data['refraction'] = self.rotation
		data['center-of-mass'] = self._obj_center_of_mass
		data['children'] = [c.to_json() for c in self.children_objects]

		return data

	def after_load_scene_object(self):
		pass

	##################################################################################################################
	######## PROPERTIES ##############################################################################################
	##################################################################################################################
	@property
	def children_objects(self): return self._children

	@children_objects.setter
	def children_objects(self, value):
		self._children = value

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
	def parent_object(self): return self._parent_object

	@parent_object.setter
	def parent_object(self, value):
		#remove from the old parent
		if self._parent_object: self._parent_object.remove_child(self)
		#add to the parent
		if value:
			value.add_child(self)
		else:
			self._parent_object = None

	@property
	def position(self): return self._obj_position

	@position.setter
	def position(self, value):  
		self._obj_position = value; 
		self.updateMesh()

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
	def center_of_mass(self): return self._obj_center_of_mass

	@center_of_mass.setter
	def center_of_mass(self, value):  self._obj_center_of_mass = value; self.updateMesh()

	

	

	@property
	def position_matrix(self): return np.matrix( self.position )

	@position_matrix.setter
	def position_matrix(self, value): self.position = value.tolist()[0]
	
	@property
	def center_of_mass_matrix(self): return np.matrix( self.center_of_mass )

	@property
	def rotation_matrix(self): return self._R

	@property
	def active(self): return self._active

	@active.setter
	def active(self, value): self._active = value

