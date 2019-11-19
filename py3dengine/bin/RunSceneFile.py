
import sys,cv2, numpy as np, os, sys, csv
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.TriangulationGLScene import TriangulationGLScene




"""
inputdatafile = DATA_FILE
inputdatafilebasefile = os.path.basename(inputdatafile).replace('.csv', '')
inputdatafiledirname = os.path.dirname(inputdatafile)


outvideofile = os.path.join(inputdatafiledirname, inputdatafilebasefile)+'.avi'
outfile = open( os.path.join(inputdatafiledirname, inputdatafilebasefile)+'_res.csv', 'w')
infile  = open(inputdatafile, 'rb')
"""
"""
head = scene.getObject('Head')
body = scene.getObject('Body')
tail = scene.getObject('Tail')
leftWing = scene.getObject('Left wing')
rightWing = scene.getObject('Right wing')

#body.Translate( (-10,0,0) )
#tail.Rotate(angleZ=np.pi/2)
#tail.Rotate(angleY=np.pi/2)
#tail.Rotate(angleZ=np.pi/2)
leftWing.Rotate(angleZ=-np.pi/10)
rightWing.Rotate(angleZ=np.pi/2)
tail.Rotate(angleY=np.pi/8)
"""
#tail.RotateY( np.pi/2)
#print scene.cameras[0].calcPoint(100,100, 1)

class RunSceneFile(object):

	def __init__(self, scenefilename, videowriter=None):
		self._windowSize 	= 640, 480
		self._rotation 		= [-67.49999999999994, 0, -71.99999999999997]
		self._zoom 			= 9
		self._mouseButton 	= 1
		self._mouseState 	= 1
		self._lastMouseX 	= 0
		self._lastMouseY 	= 0
		self._position 		= [-4.6, 0.5999999999999998]
		self._videowriter 	= videowriter
		self._spamreader  	= None
		self._currentTime 	= 0
		self._fullsceen	 	= False

		self._scene 		= TriangulationGLScene()
		w 					= WavefrontOBJReader(scenefilename)
		self._scene.objects = w.objects
		self._scene.cameras = w.cameras
		self._objects 		= self._scene.objects
		

	def InitGL(self, Width, Height):             # We call this right after our OpenGL window is created.

		glClearColor(0.0, 0.0, 0.0, 0.0)        # This Will Clear The Background Color To Black
		#glClearDepth(1.0)                       # Enables Clearing Of The Depth Buffer
		#glDepthFunc(GL_LESS)                    # The Type Of Depth Test To Do
		#glEnable(GL_DEPTH_TEST)                 # Enables Depth Testing
		#glShadeModel(GL_SMOOTH)                 # Enables Smooth Color Shading

		glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
		glDisable(GL_DEPTH_TEST)                # Enables Depth Testing
		glEnable(GL_BLEND)         
		glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
		glBlendFunc(GL_SRC_ALPHA,GL_ONE)          
		glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
		glHint(GL_POINT_SMOOTH_HINT,GL_NICEST);   

		#glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 0.0, 1.0)) # Position The Light
		#glEnable(GL_LIGHT0)
		#glEnable(GL_LIGHTING)

		glEnable(GL_COLOR_MATERIAL)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()                        # Reset The Projection Matrix
		gluPerspective(47.50, float(Width)/float(Height), 0.1, 400.0)
		glMatrixMode(GL_MODELVIEW)

	def ReSizeGLScene(self, Width, Height):
	    if Height == 0: Height = 1
	    glViewport(0, 0, Width, Height)
	    glMatrixMode(GL_PROJECTION)
	    glLoadIdentity()
	    gluPerspective(47.50, float(Width)/float(Height), 0.1, 400.0)
	    glMatrixMode(GL_MODELVIEW)

	def DrawGL(self):
		glClearColor(0.0, 0.0, 0.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glScalef(1,-1,-1)
		glTranslatef( self._position[0], self._position[1], self._zoom)
		glRotatef( self._rotation[0], 1,0,0 )
		glRotatef( self._rotation[1], 0,1,0 )
		glRotatef( self._rotation[2], 0,0,1 )
		
		self._scene.DrawGLScene()
		
		self.drawData()

		if self._videowriter!=None:
			img = self.readScreen(0, 0, self._windowSize[0], self._windowSize[1])
			self._videowriter.write(img)
			
		
		glutSwapBuffers()

		#self._started = True


	def readScreen(self, x, y, width, height):
		glFinish()
		glPixelStorei(GL_PACK_ALIGNMENT, 4)
		glPixelStorei(GL_PACK_ROW_LENGTH, 0)
		glPixelStorei(GL_PACK_SKIP_ROWS, 0)
		glPixelStorei(GL_PACK_SKIP_PIXELS, 0)
		data = glReadPixels(x, y, width, height, GL_BGR, GL_UNSIGNED_BYTE)
		data = np.fromstring(data, dtype=np.uint8)
		data.shape = (height, width, 3)
		data = cv2.flip(data, 0)
		return data



	# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
	def keyPressed(self, *args):
		
		# If escape is pressed, kill everything.
		if args[0] == b'\033': sys.exit()
		if args[0] == b'f':
			if not self._fullsceen: 
				glutFullScreen()
				self._fullsceen = True
			else:
				glutReshapeWindow(*self._windowSize)
				self._fullsceen = False


	def onMouseHandler(self, button, state, x, y):
		if button==3 and state==1: self._zoom -=1
		if button==4 and state==1: self._zoom +=1

		self._lastMouseX = x
		self._lastMouseY = y
		self._mouseButton = button
		self._mouseState  = state


	def mouseMotionHandler(self,x, y):
		
		xdiff = self._lastMouseX-x
		ydiff = self._lastMouseY-y
		
		if self._mouseButton==0 and self._mouseState==0 and xdiff>0: self._rotation[2] += 0.9
		if self._mouseButton==0 and self._mouseState==0 and xdiff<0: self._rotation[2] -= 0.9
		if self._mouseButton==0 and self._mouseState==0 and ydiff>0: self._rotation[0] -= 0.9
		if self._mouseButton==0 and self._mouseState==0 and ydiff<0: self._rotation[0] += 0.9
		
		if self._mouseButton==2 and self._mouseState==0 and xdiff>0: self._position[0] -= 0.1
		if self._mouseButton==2 and self._mouseState==0 and xdiff<0: self._position[0] += 0.1
		if self._mouseButton==2 and self._mouseState==0 and ydiff>0: self._position[1] -= 0.1
		if self._mouseButton==2 and self._mouseState==0 and ydiff<0: self._position[1] += 0.1
		
		self._lastMouseX = x
		self._lastMouseY = y

	def loadData(self): pass
	def drawData(self): pass

	def startScene(self):
		
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

		glutInitWindowSize(*self._windowSize)
		glutInitWindowPosition(0, 0)
		glutCreateWindow("World simulator")
		glutIdleFunc(       self.DrawGL   )
		glutReshapeFunc(    self.ReSizeGLScene )
		glutKeyboardFunc(   self.keyPressed    )
		glutMouseFunc(      self.onMouseHandler  )
		glutMotionFunc(     self.mouseMotionHandler  )
		self.InitGL(*self._windowSize)

		self.loadData()
		glutMainLoop()





if __name__ == "__main__":
	SCENE = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/13_02_2015/sceneWithPool2.obj'
	
	run = RunSceneFile(SCENE)
	run.startScene()

