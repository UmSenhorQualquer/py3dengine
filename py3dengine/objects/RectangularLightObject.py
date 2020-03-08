from py3dengine.objects.WavefrontOBJSceneObject import WavefrontOBJSceneObject
from py3dengine.objects.TriangleObject import TriangleObject
import numpy as np, math
from .RectangleObject import RectangleObject
from ..cameras.Ray import Ray


class RectangularLightObject(RectangleObject):
    _type = 'RectangularLightObject'

    def __init__(self,
                 name='Untitled',
                 p0=(0, 0, 0), p1=(1, 0, 0), p2=(1, 0, 1), p3=(0, 0, 1),
                 focal_point=-1000, rays_step=1.0
                 ):



        self._triangleA = TriangleObject(name, p0, p1, p2)
        self._triangleB = TriangleObject(name, p2, p3, p0)

        self._focal_point = focal_point
        self._rays_step = rays_step
        self._rays = []

        super().__init__(name)

    @property
    def focal_point(self):
        return self._focal_point

    @property
    def rays_step(self):
        return self._rays_step

    @property
    def rays(self):
        return self._rays

    def calculate_rays(self):
        self._rays = []

        xs = [self.point0[0], self.point1[0], self.point2[0], self.point3[0]]
        ys = [self.point0[1], self.point1[1], self.point2[1], self.point3[1]]
        zs = [self.point0[2], self.point1[2], self.point2[2], self.point3[2]]

        p0 = min(xs), min(ys), min(zs)
        p1 = max(xs), max(ys), max(zs)

        p2 = (p1[0]-p0[0])/2, (p1[1]-p0[1])/2, (p1[2]-p0[2])/2

        for x in np.arange(p0[0], p1[0], self.rays_step):
            for y in np.arange(p0[1], p1[1], self.rays_step):
                for z in np.arange(p0[2], p1[2], self.rays_step):
                    c0 = p2[0], p2[1], p2[2] + self.focal_point
                    c1 = p0[0]+x, p0[1]+y, p0[2]+z
                    r = Ray(c0, c1, depth=2)
                    self._rays.append(r)


    def DrawGL(self):
        super().DrawGL()
        for r in self._rays:
            r.DrawGL()

    @property
    def wavefrontobject(self):
        obj = RectangularLightObject.wavefrontobject.fget(self)
        obj.addProperty('focal_point', self.focal_point)
        obj.addProperty('rays_step', self.rays_step)
        return obj

    @wavefrontobject.setter
    def wavefrontobject(self, value):
        RectangularLightObject.wavefrontobject.fset(self, value)
