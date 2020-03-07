#!/usr/bin/env pythonw
import cv2, math, numpy as np, itertools, sys
from py3dengine.cameras.Ray import Ray

try: from multiprocessing import Pool
except: print('No multiprocessing library')

try: import sharedmem
except: print('No sharedmem library')


class BaseCamera(object):

	def __init__(self, name='Untitled', width=1280, height=960, 
		position=None, rotationVector=None, maxFocalLength=None,
		cameraMatrix=None, cameraDistortion=None):
		self.position 		= 0,0,0
		self.rotationVector = 0,0,0
		self.maxFocalLength = 100.0
		self.cameraWidth    = 1280.0
		self.cameraHeight    = 960.0
		self.cameraMatrix 	  = np.matrix([[ 973.83868801,0.,667.4617181 ],[0.,973.55147583,542.32850545],[0.,0.,1.]])
		self.cameraDistortion = np.array([ -3.55507046e-01, 1.76486050e-01, 1.65274132e-03, -1.38058855e-04, -5.18798911e-02] )
		self.name = name
		self._rays = []

		if position!=None: 		 	self.position 		 	= position
		if maxFocalLength!=None: 	self.maxFocalLength 	= maxFocalLength
		if rotationVector!=None: 	self.rotationVector 	= rotationVector
		if cameraMatrix!=None:   	self.cameraMatrix 		= cameraMatrix
		if cameraDistortion!=None: 	self.cameraDistortion 	= cameraDistortion
		
		
		
	
	####################################################################################
	######### FUNCTIONS ################################################################
	####################################################################################

	def pixelTo3D(self, u, v, z=1.0): 
		""" 
		Map a camera pixel to a 3D coordenate with z without 
		counting with the camera rotation and position
		"""
		src = np.array([ [[ u, v]] ], dtype=np.float32)
		
		points = cv2.undistortPoints(src, self.cameraMatrix, self.cameraDistortion)
		
		return points[0][0][0]*z,points[0][0][1]*z, 1.0*z
		#u,v = points[0][0][0],points[0][0][1]

		#return ((u - self.cameraCx)/self.cameraFx)*z, ((v - self.cameraCy)/self.cameraFy)*z, z

	def __pixelTo3DMatrix(self, u,v, z=1.0): 
		""" 
		Return the pixelTo3D coordenate in matrix to be used in calcs
		"""
		return np.matrix([list(self.pixelTo3D(u,v,z))])

	def calcPoint(self, u,v, z):
		""" 
		Map a camera pixel to a 3D coordenate with z having in 
		consideration the camera rotation and position in relation to the world axis
		"""
		p2 = self.__pixelTo3DMatrix(u,v,z)*self._camRotM.T + np.matrix(self._tvecs)
		return tuple(p2.tolist()[0])

	def calcPixel(self,x,y,z):
		p = (np.float32([x,y,z]) - self._tvecs)*self._camRotM

		res = cv2.projectPoints(
			np.float32([p]),
			np.zeros(3), np.zeros(3),
			np.float32(self.cameraMatrix),
			np.float32(self.cameraDistortion))[0].ravel()
		
		return tuple(res)
		


	def pixelLinePoints(self, u, v, z=1):
		""" 
		Camera pixel ray coords
		"""
		p1 = self._tvecs
		p2 = self.calcPoint(u,v, z)
		return tuple(p1.tolist()[0]), p2

	def createRay(self, u, v, z=1, color=(0.5, 0.0, 1.0) ):
		p0, p1 = self.pixelLinePoints(u,v,z)
		ray = Ray(p0, p1, color)
		return ray

	def addRay(self, u, v, z=1, color=(0.5, 0.0, 1.0) ):
		ray = self.createRay(u, v, z, color=color)
		self._rays.append(ray)
		return ray

	def cleanRays(self): self.rays = []


	def Translate(self, pos):
		self.position += pos

	def Rotate(self, rotMatrix):
		self._camRotM = self._camRotM * rotMatrix
		



	####################################################################################
	######### PROPERTIES ###############################################################
	####################################################################################
	
	@property
	def rotationAngle(self): return math.sqrt(self._rvecs[0]**2+self._rvecs[1]**2+self._rvecs[2]**2)
		
	@property
	def rotationAngleDegrees(self): return math.degrees(self.rotationAngle)

	@property
	def positionTuple(self): return self._tvecs.tolist()[0]

	@property
	def position(self): return self._tvecs
	@position.setter
	def position(self, value):
		if isinstance(value, tuple) or isinstance(value, list): 
			self._tvecs = np.matrix([list(value)])
		else:
			self._tvecs = value

	@property
	def rotationVector(self): return self._rvecs
	@rotationVector.setter
	def rotationVector(self, value):
		if isinstance(value, tuple ): 
			self._rvecs = np.float32(list(value)).T
		elif isinstance(value, list ): 
			self._rvecs = np.float32( value ).T
		elif isinstance(value, str ): 
			self._rvecs = np.float32( list(map(float,value.split(','))) ).T
		else: 
			self._rvecs = value

		self._camRotM = np.matrix( cv2.Rodrigues(self._rvecs)[0] )

	@property
	def cameraMatrix(self): return self._cameraMatrix
	@cameraMatrix.setter
	def cameraMatrix(self, value): 
		if isinstance(value, tuple ):
			value = list(value) 
			self._cameraMatrix = np.matrix([value[0:3], value[3:6], value[6:9]])
		elif isinstance(value, list ): 
			self._cameraMatrix = np.matrix([value[0:3], value[3:6], value[6:9]])
		elif isinstance(value, str ): 
			value = list(map(float,value.split(',')))
			self._cameraMatrix = np.matrix([value[0:3], value[3:6], value[6:9]])
		else: 
			self._cameraMatrix = value

	

	@property
	def cameraDistortion(self): return self._cameraDistortion
	@cameraDistortion.setter
	def cameraDistortion(self, value):
		if isinstance(value, tuple ):
			self._cameraDistortion = np.matrix(list(value))
		elif isinstance(value, list ): 
			self._cameraDistortion = np.matrix(value)
		elif isinstance(value, str ): 
			self._cameraDistortion = np.matrix( list(map(float,value.split(','))) )
		else: 
			self._cameraDistortion = value 
	
	@property
	def cameraWidth(self): return self._cameraWidth
	@cameraWidth.setter
	def cameraWidth(self, value): self._cameraWidth = value

	@property
	def cameraHeight(self): return self._cameraHeight
	@cameraHeight.setter
	def cameraHeight(self,value): self._cameraHeight = value

	@property
	def cameraFx(self): return self._cameraMatrix[0,0]
	@cameraFx.setter
	def cameraFx(self, value): self._cameraMatrix[0,0] = value

	@property
	def cameraFy(self): return self._cameraMatrix[1,1]
	@cameraFy.setter
	def cameraFy(self, value): self._cameraMatrix[1,1] = value

	@property
	def cameraCx(self): return self._cameraMatrix[0,2]
	@cameraCx.setter
	def cameraCx(self, value): self._cameraMatrix[0,2] = value

	@property
	def cameraCy(self): return self._cameraMatrix[1,2]
	@cameraCy.setter
	def cameraCy(self, value): self._cameraMatrix[1,2] = value

	@property
	def maxFocalLength(self): return self._maxFocalLength
	@maxFocalLength.setter
	def maxFocalLength(self, value): 
		if isinstance(value, float):  value = int(value)
		if isinstance(value, str):  value = int(float(value))
		self._maxFocalLength = value

	@property
	def name(self): return self._name
	@name.setter
	def name(self, value): self._name = value


	@property
	def rays(self): return self._rays
	@rays.setter
	def rays(self, value): self._rays = value

	def rayCastingImage(self, pixelStep, objects, multipleprocessing=False, box=None):
		initial = int(round(pixelStep/2))
		if box==None: box = 0, 0, int(self.cameraWidth), int(self.cameraHeight)
		xsRange = range( initial+box[0], box[2], pixelStep )
		ysRange = range( initial+box[1], box[3], pixelStep )
		positions = list(itertools.product(xsRange, ysRange))
		
		total = float(len(xsRange)*len(ysRange))-1.0

		if not multipleprocessing:
			img = np.zeros( ( int(self.cameraHeight), int(self.cameraWidth), 3), dtype=np.uint8 )
			for i, (x,y) in enumerate(positions):
				p0, p1 = self.pixelLinePoints(x,y)
				ray = Ray(p0, p1, depth=0)
				res = ray.collide(objects)
				color = ray.color[2]*255, ray.color[1]*255, ray.color[0]*255
				if res: img[y-initial:y+initial+1,x-initial:x+initial+1] = color

				sys.stdout.write('\r%f%%' %  (float(i)/total*100.0) )
		else:
			img = sharedmem.zeros( (self.cameraHeight, self.cameraWidth, 3), dtype=np.uint8 )
			split = 10
			jump = int(total / split)
		
			pool = Pool(10)
			parms = []
			for i in range(0,split):
				parms.append( ( self, objects, img, positions[i*jump:(i+1)*jump], initial ) )
			pool.map(RayCastingCall, parms)
		return img



def RayCastingCall(parms):
	camera, objects, img, positions, initial = parms
	
	for i, (x,y) in enumerate(positions):
		p0, p1 = camera.pixelLinePoints(x,y)
		ray = Ray(p0, p1, depth=0)
		res = ray.collide(objects)

		color = ray.color[2]*255, ray.color[1]*255, ray.color[0]*255
		if res: img[y-initial:y+initial+1,x-initial:x+initial+1] = color

		


		