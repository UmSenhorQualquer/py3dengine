from py3dengine.cameras.ray import Ray

class PhysicsFromCamera(object):

	def getRay(self, u, v):
		ray = Ray(space=None, rlen=self.maxFocalLength)
		p0, p1 = self.pixelLinePoints(u,v)

		ray.setPosition(p0)
		ray.setQuaternion( (0,p1[0],p1[1],p1[2]) )
		
		return ray