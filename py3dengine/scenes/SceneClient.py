import traceback, pickle, socket, time
from py3dengine.scenes.GLScene 			import GLScene
from py3dengine.cameras.ClientCamera 	import ClientCamera
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJObject import WavefrontOBJObject


class SceneClient(GLScene):

	def __init__(self, host, describer=None):
		super(SceneClient, self).__init__(describer=describer)
		self._host = host
		self.__try_connection()

	def __try_connection(self):
		try:
			self._client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
			self._client.connect ( self._host )
		except Exception as e:
			traceback.print_exc()
			print('No server available')
			self._last_try = time.time()
			self._client = None

	def close_connection(self):
		if self._client: self._client.close()

	def synchronize(self):
		if self._client:
			
			data = pickle.dumps(self)
			self._client.send(b'update-scene')
			self._client.send(f'{len(data)}'.zfill(30).encode())
			self._client.send(data)

		#If there is no connection available try it every 5 seconds
		elif (time.time()-self._last_try)>5.0:
			self.__try_connection()


	@property
	def cameras(self): return self._cameras
	@cameras.setter
	def cameras(self, value):
		self._cameras =[]
		for o in value:
			if isinstance(o, WavefrontOBJObject):
				if o.getProperty('type')=='Camera': 
					win = ClientCamera(self)
					win.wavefrontobject = o
					self._cameras.append(win)
			else:
				self._cameras.append(o)


	####################################################################
	#### PICKLE ########################################################
	####################################################################

	def __getstate__(self):
		"""Return state values to be pickled."""
		return (self.cameras, self.objects, self.selected_object)

	def __setstate__(self, state):
		"""Restore state from the unpickled state values."""
		self.selected_object = None
		self.cameras, self.objects, self.selected_object = state