#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Other geometries
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import numpy as np
from point import Point


class Ray(object):
    def __init__(self, start, direction):
        self.start = start
        self.direction = direction
        self.direction.normalize()

    def get_closest_index(self, points):
        """ return closest point to ray (only forward points) """
        info = [(i, (p-self.start).length()) for i, p in enumerate(points) if self.direction.dot(p-self.start) > 0]
        info = [x for x in info if x[1] > 1e-6]
        return min(info, key=lambda x: x[1])[0] if info else None

    def __repr__(self):
        return '<Ray start({}), dir({})>'.format(self.start, self.direction)


class Object3D(object):
    def intersect(self, ray):
        """ must return None or tuple(point, normal) """
        raise NotImplementedError()


class Rectangle(Object3D):
    def __init__(self, center, width, height, vec_up, normal):
        self.center = center
        self.w = width
        self.h = height
        self.vec_up = vec_up.normalized() / (self.h/2.)
        self.normal = normal.normalized()
        self.vec_right = self.vec_up.cross(self.normal).normalized() / (self.w/2.)

    def intersect(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            p0l0 = self.center - ray.start; 
            t = p0l0.dot(self.normal) / denom;
            if t < 0:
                return None
        else:
            return None

        intersection_point = ray.start + ray.direction * t
        rel_point = intersection_point - self.center
        y = rel_point.dot(self.vec_up)
        x = rel_point.dot(self.vec_right)

        if abs(y) > 1.0 or abs(x) > 1.0:
            return None

        normal = self.normal.copy()
        if ray.direction.dot(self.normal) > 0:
            normal = -normal

        return intersection_point, normal

    def rotate(self, angle, rot_axis, center):
        old_vec = self.center - center
        new_vec = old_vec.rotate(angle, rot_axis)

        self.center = center + new_vec
        self.vec_up = self.vec_up.rotate(angle, rot_axis)
        self.normal = self.normal.rotate(angle, rot_axis)
        self.vec_right = self.vec_right.rotate(angle, rot_axis)


