try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
except:
	print('No OpenGL libs')

import math, numpy as np
import cv2
from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


class PlaneObject(WavefrontOBJSceneObject):

	_type = 'PlaneObject'

	def __init__(self, name='Untitled', width=1.0,height=1.0):
		
		self._obj_width  = width
		self._obj_height = height
		
		self._mask_file = None
		self._mask   	= None

		self._texture 	= None
		self._compare_mask = None

		WavefrontOBJSceneObject.__init__(self,name)


	def __updateTexture(self):
		if not isinstance(self._mask, (np.ndarray, np.generic) ): return
		if self._texture!=None: glDeleteTextures(self._texture)

		h, w 			= self._mask.shape[:2]
		self._texture 	= glGenTextures(1)

		glEnable(GL_TEXTURE_2D)
		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glBindTexture(GL_TEXTURE_2D, self._texture)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, self._mask)


	def updateMesh(self):
		p0 = [0,0,0]
		p1 = p0[0]+self._obj_width, p0[1], 					p0[2]
		p2 = p0[0]+self._obj_width, p0[1]+self._obj_height, p0[2]
		p3 = p0[0]	  			  , p0[1]+self._obj_height, p0[2]

		Tmass 	= self.centerOfMassMatrix
		T 		= self.positionMatrix
		R 		= self.rotationMatrix
		
		self._point0 = np.array( (np.matrix(p0)-Tmass)*R+T )[0]
		self._point1 = np.array( (np.matrix(p1)-Tmass)*R+T )[0]
		self._point2 = np.array( (np.matrix(p2)-Tmass)*R+T )[0]
		self._point3 = np.array( (np.matrix(p3)-Tmass)*R+T )[0]

		ax, ay, az = self._point0
		bx, by, bz = self._point1
		cx, cy, cz = self._point2

		self._a = ((by-ay)*(cz-az))-((cy-ay)*(bz-az))
		self._b = ((bz-az)*(cx-ax))-((cz-az)*(bx-ax))
		self._c = ((bx-ax)*(cy-ay))-((cx-ax)*(by-ay))
		self._d = ((self._a*ax)+(self._b*ay)+(self._c*az))



	@property
	def point0(self): return self._point0
	@point0.setter
	def point0(self, value): 
		self._op = value
		self._point0 = value; 
		

	@property
	def point1(self): return self._point1
	
	@property
	def point2(self): return self._point2

	@property
	def point3(self): return self._point3

	@property
	def objwidth(self): return self._obj_width
	@objwidth.setter
	def objwidth(self, value): 
		self._obj_width = value; 
		self.updateMesh()
		if isinstance(self._mask, (np.ndarray, np.generic) ): 	
			self._compare_mask = cv2.resize( self._mask, (int(self._obj_width*100), int(self._obj_height*100)) )
		

	@property
	def objheight(self): return self._obj_height
	@objheight.setter
	def objheight(self, value): 
		self._obj_height = value; 
		self.updateMesh()
		if isinstance(self._mask, (np.ndarray, np.generic) ): 	
			self._compare_mask = cv2.resize( self._mask, (int(self._obj_width*100), int(self._obj_height*100)) )
		

	@property
	def maskimg(self): return self._mask_file if self._mask_file!=None else ''
	@maskimg.setter
	def maskimg(self, value): 
		self._mask_file = value
		self._mask = cv2.imread(value, 0) if value!=None else None
		if isinstance(self._mask, (np.ndarray, np.generic) ): 	
			self._compare_mask = cv2.resize( self._mask, (int(self._obj_width*100), int(self._obj_height*100)) )
			#self.__updateTexture()

	@property
	def normal(self): 
		a = np.array( [self._a, self._b, self._c] )
		return a/np.linalg.norm(a)


	def DrawGL(self):
		if isinstance(self._mask, (np.ndarray, np.generic) ): 	
			if self._texture==None: self.__updateTexture()
			glEnable(GL_TEXTURE_2D)
			glBindTexture(GL_TEXTURE_2D, self._texture)
		else: 					
			glDisable(GL_TEXTURE_2D)
		glColor4f(*self.color)
		
		glBegin(GL_QUADS)
		glTexCoord2f( 0.0, 0.0 ); glVertex3f(*self.point0); 
		glTexCoord2f( 1.0, 0.0 ); glVertex3f(*self.point1);
		glTexCoord2f( 1.0, 1.0 ); glVertex3f(*self.point2);
		glTexCoord2f( 0.0, 1.0 ); glVertex3f(*self.point3);
		glEnd()

		if isinstance(self._mask, (np.ndarray, np.generic) ): 	glDisable(GL_TEXTURE_2D)

		

		super(PlaneObject, self).DrawGL()
		
		
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

	def collide_with_ray(self, ray):
		
		p0, p1 = ray.points
		x0, y0, z0 = p0
		x1, y1, z1 = p1
		v0, v1, v2 	= x1-x0, y1-y0, z1-z0
		d1 = ( (self._a*v0)+(self._b*v1)+(self._c*v2) )
		
		if d1==0: return None

		d0 = (self._d-(self._a*x0)- (self._b*y0)-(self._c*z0) )
		t = d0 / d1

		if t<0: return None
		
		collision = x,y,z = x0+v0*t, y0+v1*t, z0+v2*t

		Tmass 	= self.centerOfMassMatrix
		T 		= self.positionMatrix
		R 		= self.rotationMatrix
		
		p0, p1, p2, p3 = self.point0, self.point1, self.point2, self.point3

		p0 = np.array( (np.matrix(p0)-T)*R.T+Tmass )[0]
		x,y,z = np.array( (np.matrix(collision)-T)*R.T+Tmass )[0]
		
		xx,yy = int((x-p0[0])*100.0),int( (y-p0[1])*100.0)
		
		if not isinstance(self._mask, (np.ndarray, np.generic) ): return collision, self.normal

		if  0<xx<self._compare_mask.shape[1] and 0<yy<self._compare_mask.shape[0] \
			and self._compare_mask[yy,xx]>10: 
			
		
			return collision, self.normal

		return None





	@property
	def wavefrontobject(self):
		obj = super(PlaneObject, self).wavefrontobject
		obj.addProperty('type', 'PlaneObject')
		obj.addProperty('width', self.objwidth)
		obj.addProperty('height',  self.objheight)
		obj.addProperty('mask file',  self.maskimg)

		obj.addVertice( self.point0 )
		obj.addVertice( self.point1 )
		obj.addVertice( self.point2 )
		obj.addVertice( self.point3 )

		obj.addFace( (1,2,3,4) )

		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self.point0 			= value.getVertice(0)
		self.objwidth 			= float(value.getProperty('width',1))
		self.objheight 			= float(value.getProperty('height',1))
		self.maskimg				= value.getProperty('mask file',None)

		WavefrontOBJSceneObject.wavefrontobject.fset(self, value )