#!/usr/bin/env pythonw
if __name__ == '__build__': raise Exception

from OSC import OSCServer, OSCClient, OSCMessage
from py3dengine.cameras.Camera import Camera

class ClientCamera(Camera):

	def __init__(self, client):
		super(ClientCamera, self).__init__()
		self.client = client

		
	def cleanRays(self):
		super(ClientCamera,self).cleanRays()

		#msg = self.client.msg
		#msg.append( 'cleanRays' )
		#msg.append( self.name )


	####################################################################
	#### PICKLE ########################################################
	####################################################################

	def __getstate__(self):
		"""Return state values to be pickled."""
		return [self._tvecs,
		self._rvecs,
		self._camRotM,
		self._cameraMatrix,
		self._cameraDistortion,
		self._name,
		self._maxFocalLength,
		self._cameraWidth,
		self._cameraHeight,
		self._rays,
		self._showFaces,
		self._color]


	def __setstate__(self, state):
		"""Restore state from the unpickled state values."""
		
		[self._tvecs,
		self._rvecs,
		self._camRotM,
		self._cameraMatrix,
		self._cameraDistortion,
		self._name,
		self._maxFocalLength,
		self._cameraWidth,
		self._cameraHeight,
		self._rays,
		self._showFaces,
		self._color] = state