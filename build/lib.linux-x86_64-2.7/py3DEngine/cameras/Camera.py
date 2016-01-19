#!/usr/bin/env pythonw

from py3DEngine.cameras.BaseCamera import BaseCamera
from py3DEngine.cameras.VirtualCamera import VirtualCamera
from py3DEngine.cameras.PhysicsFromCamera import PhysicsFromCamera
from py3DEngine.cameras.WavefrontOBJCamera import WavefrontOBJCamera


class Camera(WavefrontOBJCamera, VirtualCamera, PhysicsFromCamera, BaseCamera):

	def __init__(self):
		BaseCamera.__init__(self)
		PhysicsFromCamera.__init__(self)
		VirtualCamera.__init__(self)
		WavefrontOBJCamera.__init__(self)