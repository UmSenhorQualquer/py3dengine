from __init__ import *
import sys,cv2, numpy as np, os, sys, itertools
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.TriangulationGLScene import TriangulationGLScene


scene = TriangulationGLScene()

w = WavefrontOBJReader('DolphinsSceneCalibration2.obj')
scene.objects = w.objects
scene.cameras = w.cameras

windowSize 	= 800, 600
rotation 	= [-67.49999999999994, 0, -71.99999999999997]
zoom 		= 9
mouseButton = 1
mouseState 	= 1
lastMouseX 	= 0
lastMouseY 	= 0
position 	= [-4.6, 0.5999999999999998]


fx_range = np.arange(400,700,10)
fy_range = np.arange(400,700,10)
cx_range = np.arange(630,650,10.0)
cy_range = np.arange(350,370,10.0)
k0_range = np.arange(0,2,1)
k1_range = np.arange(0,2,1)
p0_range = np.arange(0,2,1)
p1_range = np.arange(0,2,1)
k2_range = np.arange(0,2,1)

values = list(itertools.product(fx_range,fy_range,cx_range,cy_range,k0_range,k1_range,p0_range,p1_range,k2_range))

def InitGL(Width, Height):             	# We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
	glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
	glDisable(GL_DEPTH_TEST)            # Enables Depth Testing
	glEnable(GL_BLEND)         
	glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
	glBlendFunc(GL_SRC_ALPHA,GL_ONE)          
	glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
	glHint(GL_POINT_SMOOTH_HINT,GL_NICEST);   
	glEnable(GL_COLOR_MATERIAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()                    # Reset The Projection Matrix
	gluPerspective(47.50, float(Width)/float(Height), 0.1, 400.0)
	glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
    if Height == 0: Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(47.50, float(Width)/float(Height), 0.1, 400.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGL():
	global scene, zoom, rotation, windowSize, values

	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glScalef(1,-1,-1)
	glTranslatef( position[0], position[1], zoom)
	glRotatef( rotation[0], 1,0,0 )
	glRotatef( rotation[1], 0,1,0 )
	glRotatef( rotation[2], 0,0,1 )

	if len(values)>0:
		fx,fy,cx,cy,k0,k1,p0,p1,k2 = values.pop()
		#print fx,fy,cx,cy,k0,k1,p0,p1,k2

		camera = scene.cameras[0]
		camera.cameraFx = fx
		camera.cameraFy = fy
		camera.cameraCx = cx
		camera.cameraCy = cy
	
	scene.DrawGLScene()
	p=False
	if p:
		
		glPushMatrix()
		glColor4f(0.0,1.0,1.0, 1.0)
		glTranslatef( p[0], p[1], p[2])
		glutSolidSphere(.1,12,12)
		glPopMatrix()

	
		

	glutSwapBuffers()



# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
	global scene, infile, windowSize

	# If escape is pressed, kill everything.
	if args[0] == '\033': sys.exit()
	if args[0] == 'f': glutFullScreen()


def onMouseHandler(button, state, x, y):
	global zoom, mouseState, mouseButton
	if button==3 and state==1: zoom -=1
	if button==4 and state==1: zoom +=1

	lastMouseX = x
	lastMouseY = y
	mouseButton = button
	mouseState  = state



def mouseMotionHandler(x, y):
	global lastMouseX, lastMouseY, mouseButton, mouseState

	xdiff = lastMouseX-x
	ydiff = lastMouseY-y
	
	if mouseButton==0 and mouseState==0 and xdiff>0: rotation[2] += 0.9
	if mouseButton==0 and mouseState==0 and xdiff<0: rotation[2] -= 0.9
	if mouseButton==0 and mouseState==0 and ydiff>0: rotation[0] -= 0.9
	if mouseButton==0 and mouseState==0 and ydiff<0: rotation[0] += 0.9
	
	if mouseButton==2 and mouseState==0 and xdiff>0: position[0] -= 0.1
	if mouseButton==2 and mouseState==0 and xdiff<0: position[0] += 0.1
	if mouseButton==2 and mouseState==0 and ydiff>0: position[1] -= 0.1
	if mouseButton==2 and mouseState==0 and ydiff<0: position[1] += 0.1
	
	lastMouseX = x
	lastMouseY = y



glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

glutInitWindowSize(*windowSize)
glutInitWindowPosition(0, 0)
glutCreateWindow("World simulator")
#glutDisplayFunc(    DrawGL   )
glutIdleFunc(       DrawGL   )
glutReshapeFunc(    ReSizeGLScene )
glutKeyboardFunc(   keyPressed    )
glutMouseFunc(      onMouseHandler  )
glutMotionFunc(     mouseMotionHandler  )
InitGL(*windowSize)

glutMainLoop()
