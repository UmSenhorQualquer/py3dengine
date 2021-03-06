import sys,cv2, numpy as np, os, sys, itertools
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.bin.GLScene import GLScene


scene = GLScene()

w = WavefrontOBJReader('../data/marcia/scene1.obj')
scene.objects = w.objects
scene.cameras = w.cameras

windowSize 	= 640, 480
rotation 	= [-67.49999999999994, 0, -71.99999999999997]
zoom 		= 9
mouseButton = 1
mouseState 	= 1
lastMouseX 	= 0
lastMouseY 	= 0
position 	= [-4.6, 0.5999999999999998]

head = scene.getObject('Head')
body = scene.getObject('Body')
tail = scene.getObject('Tail')
leftWing = scene.getObject('Left wing')
rightWing = scene.getObject('Right wing')

#body.Translate( (-10,0,0) )
#tail.Rotate(angleZ=np.pi/2)
#tail.Rotate(angleY=np.pi/2)
#tail.Rotate(angleZ=np.pi/2)
leftWing.Rotate(angleZ=-np.pi/2)
rightWing.Rotate(angleZ=np.pi/2)



def InitGL(Width, Height):             # We call this right after our OpenGL window is created.
    

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

def ReSizeGLScene(Width, Height):
    if Height == 0: Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(47.50, float(Width)/float(Height), 0.1, 400.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGL():
	global scene, zoom, rotation, windowSize, outvideo, currentTime, currentTag, tags

	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glScalef(1,-1,-1)
	glTranslatef( position[0], position[1], zoom)
	glRotatef( rotation[0], 1,0,0 )
	glRotatef( rotation[1], 0,1,0 )
	glRotatef( rotation[2], 0,0,1 )
	
	scene.DrawGLScene()


	glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
	global scene, infile, outvideofile, outvideo, windowSize

	# If escape is pressed, kill everything.
	if args[0] == b'\033': sys.exit()
	if args[0] == b'f': glutFullScreen()


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


def __main__():
	"""glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

	glutInitWindowSize(*windowSize)
	glutInitWindowPosition(0, 0)
	glutCreateWindow("World simulator")
	glutDisplayFunc(    DrawGL   )
	glutIdleFunc(       DrawGL   )
	glutReshapeFunc(    ReSizeGLScene )
	glutKeyboardFunc(   keyPressed    )
	glutMouseFunc(      onMouseHandler  )
	glutMotionFunc(     mouseMotionHandler  )
	InitGL(*windowSize)
	"""
	import timeit
	start = timeit.default_timer()

	img = scene.cameras[0].rayCastingImage(5, [x for x in scene.objects if x.active], multipleprocessing=False)

	stop = timeit.default_timer()
	
	cv2.imshow('img', img)
	cv2.waitKey(0)

	#glutMainLoop()

__main__()