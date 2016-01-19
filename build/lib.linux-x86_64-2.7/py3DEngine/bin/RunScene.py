from __init__ import *
import sys,cv2, numpy as np, os, sys, csv
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

class RunScene(object):

	def __init__(self, scene, videowriter=None):
		self._windowSize 	= 640, 480
		self._rotation 		= [0,0,0]
		self._zoom 			= 9
		self._mouseButton 	= 1
		self._mouseState 	= 1
		self._lastMouseX 	= 0
		self._lastMouseY 	= 0
		self._position 		= [-114.11685213,  -27.68483338]
		self._videowriter 	= videowriter
		self._spamreader  	= None
		self._currentTime 	= 0
		self._fullsceen	 	= False

		self._scene 		= scene
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
		gluPerspective(47.50, float(Width)/float(Height), 0.1,15000.0)
		glMatrixMode(GL_MODELVIEW)

	def ReSizeGLScene(self, Width, Height):
	    if Height == 0: Height = 1
	    glViewport(0, 0, Width, Height)
	    glMatrixMode(GL_PROJECTION)
	    glLoadIdentity()
	    gluPerspective(47.50, float(Width)/float(Height), 0.1, 15000.0)
	    glMatrixMode(GL_MODELVIEW)

	def process(self, runscene):
		pass

	def DrawGL(self):
		self.process(self)
		
		glClearColor(0.0, 0.0, 0.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glScalef(-1,-1,-1)
		
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
		if args[0] == '\033': sys.exit()
		if args[0] == 'f':
			if not self._fullsceen: 
				glutFullScreen()
				self._fullsceen = True
			else:
				glutReshapeWindow(*self._windowSize)
				self._fullsceen = False


	def onMouseHandler(self, button, state, x, y):
		if button==3 and state==1: self._zoom -=50
		if button==4 and state==1: self._zoom +=50

		self._lastMouseX = x
		self._lastMouseY = y
		self._mouseButton = button
		self._mouseState  = state

		#print self._rotation, self._position, self._zoom



	def mouseMotionHandler(self,x, y):
		
		xdiff = self._lastMouseX-x
		ydiff = self._lastMouseY-y
		
		if self._mouseButton==0 and self._mouseState==0 and xdiff>0: self._rotation[2] += 0.9
		if self._mouseButton==0 and self._mouseState==0 and xdiff<0: self._rotation[2] -= 0.9
		if self._mouseButton==0 and self._mouseState==0 and ydiff>0: self._rotation[0] -= 0.9
		if self._mouseButton==0 and self._mouseState==0 and ydiff<0: self._rotation[0] += 0.9
		
		if self._mouseButton==2 and self._mouseState==0 and xdiff>0: self._position[0] -= 50
		if self._mouseButton==2 and self._mouseState==0 and xdiff<0: self._position[0] += 50
		if self._mouseButton==2 and self._mouseState==0 and ydiff>0: self._position[1] -= 50
		if self._mouseButton==2 and self._mouseState==0 and ydiff<0: self._position[1] += 50
		
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
		print "Load finnished"
		glutMainLoop()





if __name__ == "__main__":
	SCENE = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/13_02_2015/sceneWithPool2.obj'
	
	run = RunScene(SCENE)
	run.startScene()

