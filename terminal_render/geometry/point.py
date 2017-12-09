#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import numpy as np
import re


class Point(object):
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self._length = None

    def __repr__(self):
        return re.sub('([^\d])(0.00)([^\d])', '\g<1>0\g<3>', '<P({i.x:.2f}, {i.y:.2f}, {i.z:.2f})>'.format(i=self))

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise NotImplementedError()

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise NotImplementedError()

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        if isinstance(other, Point):
            raise AttributeError('Use a.dot(b) for points.')
        else:
            return Point(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        if isinstance(other, Point):
            raise AttributeError('Use a.cross(b) for points.')
        else:
            return Point(self.x / other, self.y / other, self.z / other)

    def length(self):
        if self._length is None:
            self._length = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return self._length

    def copy(self):
        p = Point(self.x, self.y, self.z)
        p._length = self._length
        return p

    def normalize(self):
        self.x /= self.length()
        self.y /= self.length()
        self.z /= self.length()
        self._length = 1.0
        return self

    def normalized(self):
        return self.copy().normalize()

    def dot(self, other):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise NotImplementedError()

    def cosine_to(self, other):
        if isinstance(other, Point):
            return self.dot(other)/(self.length() * other.length())
        else:
            raise NotImplementedError()

    def cross(self, other):
        if isinstance(other, Point):
            return Point(self.y * other.z - self.z * other.y,
                         self.z * other.x - self.x * other.z,
                         self.x * other.y - self.y * other.x)
        else:
            raise NotImplementedError()

    def rotate(self, angle, axis):
        e = axis.normalized()
        angle = np.deg2rad(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return e * self.dot(e)*(1-cos_a) + self.cross(e)*sin_a + self.copy()*cos_a