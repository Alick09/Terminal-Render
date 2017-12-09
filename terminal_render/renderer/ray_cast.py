#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 09.12.2017 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""


import numpy as np
from ..geometry import Ray


class RayCaster(object):
    def __init__(self, scene, width, height, fix_coeff=1.0, antialiasing_level = 2):
        """ 
            width and height - pixel size of output image 
            fix_coeff - pixel_height/pixel_width ratio
        """
        self.scene = scene
        self.antialiasing_level = antialiasing_level
        self.width = width
        self.height = height
        self.fix_coeff = fix_coeff
        self.initialize_grid()

    def initialize_grid(self):
        step = 1./(self.width + 1)
        hmax = self.height * step * self.fix_coeff
        self.xs = np.linspace(-1, 1, self.width * self.antialiasing_level)
        self.ys = np.linspace(hmax, -hmax, self.height * self.antialiasing_level)

    def get_pixel_rays(self, x, y):
        for dy in xrange(self.antialiasing_level):
            for dx in xrange(self.antialiasing_level):
                yield self.scene.camera.get_ray(
                    self.xs[x*self.antialiasing_level+dx],
                    self.ys[y*self.antialiasing_level+dy]
                )

    def cast_light(self, point, normal, light):
        ray = Ray(point, light.position - point)
        max_length = (light.position - point).length()
        first_point = self.scene.intersect(ray)
        if first_point is not None and (first_point[0] - point).length() < max_length:
            return 0
        else:
            cos_a = ray.direction.dot(normal)
            return max(0, cos_a) * light.force


    def cast_lights(self, point, normal):
        """ Returns light coefficient """
        result = sum([self.cast_light(point, normal, light) for light in self.scene.lights])
        return result / self.scene.get_light_force()