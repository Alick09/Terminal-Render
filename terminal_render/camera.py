#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Camera.
Created 08.10.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""


from geometry import Ray, Point
import numpy as np



class Camera(object):
    def __init__(self, position, looking_point, view_angle, up_vec=None):
        self.position = position
        self.looking_point = looking_point
        self.view_angle = view_angle
        self.update(up_vec)

    def update(self, up_vec=None):
        start = self.position
        self.direction = self.looking_point - start
        self.direction.normalize()
        self.screen_pos = start + self.direction
        if up_vec is None:
            up_vec = Point(0, 0, 1)
        if abs(self.direction.cosine_to(up_vec)) > 1. - 1e-8:
            raise RuntimeError("Can't reveal up vector")
        self.right_vec = -self.direction.cross(up_vec).normalized()
        self.up_vec = self.direction.cross(self.right_vec).normalized()
        self.side_length = np.tan(np.deg2rad(self.view_angle))

    def get_ray(self, nx, ny):
        """ nx and ny from (-1, 1) """
        end = self.screen_pos + (self.right_vec * nx + self.up_vec * ny) * self.side_length
        return Ray(self.position, end - self.position)