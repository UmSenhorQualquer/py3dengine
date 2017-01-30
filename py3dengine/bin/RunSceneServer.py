#!/usr/bin/env python2.7
from __init__ import *

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.GLScene import GLScene
from py3dengine.cameras.Ray import Ray
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from time import sleep
import sys, cv2, types, numpy as np, pickle, socket, thread, argparse, atexit, traceback


server_socket = None
scene 		= GLScene()
windowSize 	= 640, 480
rotation 	= [-67.49999999999994, 0, -71.99999999999997]
zoom 		= 9
mouseButton = 1
mouseState 	= 1
lastMouseX 	= 0
lastMouseY 	= 0
position 	= [0,0,0]
outvideo 	= None
spamreader  = None
currentTime = 0
currentFrame = None




"""
	if len(args)>0:
		if not outvideo:
			print "open"
			outvideo = cv2.VideoWriter('3dscene.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 5, windowSize)
		if outvideo: outvideo.write(currentFrame)
"""
			

def InitGL(Width, Height):             # We call this right after our OpenGL window is created.

	glClearColor(0.0, 0.0, 0.0, 0.0)        # This Will Clear The Background Color To Black

	glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
	glDisable(GL_DEPTH_TEST)                # Enables Depth Testing
	glEnable(GL_BLEND)         
	glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
	glBlendFunc(GL_SRC_ALPHA,GL_ONE)          
	glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
	glHint(GL_POINT_SMOOTH_HINT,GL_NICEST);   

	glEnable(GL_COLOR_MATERIAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()                        # Reset The Projection Matrix
	gluPerspective(47.50, float(Width)/float(Height), 0.1, 900.0)
	glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
	if Height == 0: Height = 1
	glViewport(0, 0, Width, Height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(47.50, float(Width)/float(Height), 0.1, 900.0)
	glMatrixMode(GL_MODELVIEW)

def DrawGL():
	global scene, zoom, rotation, windowSize, outvideo, currentTime, spamreader, scene, currentFrame

	glClearColor(0.1, 0.1, 0.1, 1.0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glScalef(1,-1,-1)
	glTranslatef( position[0], position[1], zoom)
	glRotatef( rotation[0], 1,0,0 )
	glRotatef( rotation[1], 0,1,0 )
	glRotatef( rotation[2], 0,0,1 )
	
	scene.DrawGLScene()
	if outvideo: 
		currentFrame = readScreen(0, 0, windowSize[0], windowSize[1])
		

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



# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
	global outvideo

	# If escape is pressed, kill everything.
	if args[0] == '\033': 
		if outvideo: outvideo.release()
		sys.exit()
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

@atexit.register
def close_server():
	global server_socket
	if server_socket:
		print("-> closing server")
		server_socket.close()
		print("<- server closed")

def server_handler():
	global scene, server_socket

	while True:
		conn, addr 	= server_socket.accept()
		print("Connected to", addr)

		try:
			while True:
				command = conn.recv(12)

				if command=='update-scene':
					nbytes 	= int(conn.recv(30))
					data 	= ''
					while len(data)<nbytes: data += conn.recv(nbytes)
					scene 	= pickle.loads(data)
					command = ''
				elif not command:
					conn.close()
					break
				sleep(0.33)
		except: 
			pass
			print traceback.print_exc()
			
		print("Connection to", addr,"down")

def init():pass

def main():
	global server_socket

	parser = argparse.ArgumentParser()
	parser.add_argument("--server-address", help='Server address (default=0.0.0.0)', default='0.0.0.0')
	parser.add_argument("--server-port", help='Server port (default=5005)',type=int, default=5005)
	args = parser.parse_args()
	
	#################################################################
	### Start the network server and wait for the client connection #
	#################################################################
	server_socket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	server_socket.bind( (args.server_address, args.server_port) )
	server_socket.listen(1)
	thread.start_new_thread(server_handler, ())
	#################################################################

	#################################################################
	### Start the OpenGL window #####################################
	#################################################################

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(*windowSize)
	glutInitWindowPosition(0, 0)
	glutCreateWindow("Scene server")
	glutDisplayFunc(	DrawGL)
	glutIdleFunc(       DrawGL   )
	glutReshapeFunc(    ReSizeGLScene )
	glutKeyboardFunc(   keyPressed    )
	glutMouseFunc(      onMouseHandler  )
	glutMotionFunc(     mouseMotionHandler  )
	InitGL(*windowSize)
	glutMainLoop()
	#################################################################

	conn.close() #Close the server connection

if __name__ == "__main__": main()

	