#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 09.12.2017 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""


import numpy as np
from ..geometry import Ray, Point


class RayCaster(object):
    def __init__(self, scene, width, height, options):
        """ 
            width and height - pixel size of output image 
            fix_coeff - pixel_height/pixel_width ratio
        """
        self.options = options
        self.scene = scene
        self.width = width
        self.height = height
        self.antialiasing_level = options.get('antialiasing_level', 1)
        self.fix_coeff = options.get('fix_coeff', 1.0)
        self.use_ssao = options.get('use_ssao', False)
        self.ssao_mc_tests = options.get('ssao_mc_tests', 10)
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

    def cast_ssao(self, point, normal, move=1e-6):
        """ monte-carlo method """
        start_point = point + normal * move
        success = 1.0
        for i in xrange(self.ssao_mc_tests):
            ray = Ray(start_point, Point.semispherical_random(normal))
            intersection = self.scene.intersect(ray)
            distance = (intersection[0] - point).length()
            success += min(distance**2, 1.)
        return success / self.ssao_mc_tests

    def cast_light(self, point, normal, light, shadow_coff=0.4):
        """ returns illumination of the point by the given light """
        ray = Ray(point, light.position - point)
        max_length = (light.position - point).length()
        first_point = self.scene.intersect(ray)
        force = light.force

        if first_point is not None and (first_point[0] - point).length() < max_length:
            force *= shadow_coff

        cos_a = ray.direction.dot(normal)
        return max(0, cos_a) * force


    def cast_lights(self, point, normal):
        """ Returns light coefficient """
        result = sum([self.cast_light(point, normal, light) for light in self.scene.lights])
        if self.use_ssao:
            result *= self.cast_ssao(point, normal)
        return result / self.scene.get_light_force()