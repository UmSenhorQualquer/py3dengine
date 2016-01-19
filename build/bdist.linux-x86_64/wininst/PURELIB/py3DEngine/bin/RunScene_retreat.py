import sys,cv2, numpy as np, os, sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from TriangulationGLScene import TriangulationGLScene


scene = TriangulationGLScene()

w = WavefrontOBJReader('scene_retreat.obj')
scene.objects = w.objects
scene.cameras = w.cameras

windowSize 	= 640, 480/2
rotation 	= [-67.49999999999994, 0, -71.99999999999997]
zoom 		= 9
mouseButton = 1
mouseState 	= 1
lastMouseX 	= 0
lastMouseY 	= 0
position 	= [-4.6, 0.5999999999999998]
outvideo 	= None


tags, currentTime, currentTag = [1.7 for x in range(400)], -1, -1

#inputdatafile = sys.argv[1]#'../retreat_data/processedData/tracking2014-06-18T08_54_01.csv'
inputdatafile = '../retreat_data/processedData/tracking2014-06-18T09_32_45.csv'
print inputdatafile
inputdatafilebasefile = os.path.basename(inputdatafile)


outvideofile = os.path.join('..','results', inputdatafilebasefile)+'.avi'
outfile = open( os.path.join('..','results', inputdatafilebasefile), 'w')
infile  = open(inputdatafile, 'r')


outvideo = cv2.VideoWriter(outvideofile, cv2.cv.CV_FOURCC('M','J','P','G'), 25, windowSize)




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

	p = scene.getIntersection( z=tags[ currentTag ] )
	
	if p:
		outfile.write("%s;%s;%f;%f;%f\n" % (currentTime,currentTag,p[0],p[1],p[2] ) )

		tags[ currentTag ] = abs(p[2])

		glPushMatrix()
		glColor4f(0.0,1.0,1.0, 1.0)
		glTranslatef( p[0], p[1], p[2])
		glutSolidSphere(.1,12,12)
		glPopMatrix()

	if outvideo: 
		img = readScreen(0, 0, windowSize[0], windowSize[1])

		if p: cv2.putText(img, "Pos: %.3f, %.3f,  %.3f" % (p[0],p[1],abs(p[2])) , (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255,255,255))
		cv2.putText(img, "Time: " + str(currentTime), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255))
		cv2.putText(img, "Tag: " + str(currentTag), (5, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255))

		outvideo.write(img)
		v = readNewLine()
		if v==None: exit()
		currentTime, currentTag = v
		

	glutSwapBuffers()



def readScreen(x, y, width, height):
	glFinish()
	glPixelStorei(GL_PACK_ALIGNMENT, 4)
	glPixelStorei(GL_PACK_ROW_LENGTH, 0)
	glPixelStorei(GL_PACK_SKIP_ROWS, 0)
	glPixelStorei(GL_PACK_SKIP_PIXELS, 0)
	data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
	data = np.fromstring(data, dtype=np.uint8)
	data.shape = (height, width, 3)
	data = cv2.flip(data, 0)
	return data

def readNewLine():
	global scene, infile

	line = infile.readline()
	if not line==None and len(line)>0:
		values = eval(line)			
		counter, tagID, cameras = values
		#print counter, tagID

		for i, row in enumerate(cameras):
			scene.cameras[i].rays = []
			if row!=None:
				color = ( (255**3/100 )) * tagID
				rgb = (color % 255)/255.0, ((color // 256) % 256)/255.0, ((color // 256 // 256) % 256) /255.0
				camera 		   = scene.cameras[i]
				camera.addRay( row[0],row[1], 20, rgb )
	else:
		return None

	return counter, tagID

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
	global scene, infile, outvideofile, outvideo, windowSize

	# If escape is pressed, kill everything.
	if args[0] == '\033': sys.exit()
	if args[0] == 'f': glutFullScreen()

	if args[0] == 'a':
		camera = scene.cameras[0]
		camera.addRay(600,100, 50)

		camera = scene.cameras[1]
		camera.addRay(600,100, 50)

		camera = scene.cameras[2]
		camera.addRay(600,100, 50)

		camera = scene.cameras[3]
		camera.addRay(600,100, 50)

	if args[0] == ' ': readNewLine()
	if args[0] == 'r' and outvideofile:

		outvideo = cv2.VideoWriter(outvideofile, cv2.cv.CV_FOURCC('M','J','P','G'), 25, windowSize)



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
	#print rotation, position, zoom



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
