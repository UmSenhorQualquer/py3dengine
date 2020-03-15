#!/usr/bin/env pythonw

from py3dengine.cameras.base_camera import BaseCamera
from py3dengine.cameras.virtual_camera import VirtualCamera
from py3dengine.cameras.physics_from_camera import PhysicsFromCamera
from py3dengine.cameras.WavefrontOBJCamera import WavefrontOBJCamera


class Camera(WavefrontOBJCamera, VirtualCamera, PhysicsFromCamera, BaseCamera):

	def __init__(self):
		BaseCamera.__init__(self)
		PhysicsFromCamera.__init__(self)
		VirtualCamera.__init__(self)
		WavefrontOBJCamera.__init__(self)