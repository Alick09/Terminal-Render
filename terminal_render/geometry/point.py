#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Point class
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import numpy as np
import re


class Point(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self._length = None

    @staticmethod
    def spherical_point(theta, phi, length=1.0):
        """
            theta must be in [0, 2pi]
            phi must be in [0, pi]
        """
        x = np.sin(phi) * np.cos(theta) * length
        y = np.sin(phi) * np.sin(theta) * length
        z = np.cos(phi) * length
        return Point(x, y, z)

    @staticmethod
    def spherical_random(length=1.0):
        """ 
            returns random point by sphere uniform distribution 
        """
        theta = 2 * np.pi * np.random.random();
        phi = np.arccos(1 - 2 * np.random.random());
        return Point.spherical_point(theta, phi, length)

    @staticmethod
    def semispherical_random(up_vector, length=1.0):
        """
            returns random point by semisphere uniform distribution
            semisphere defined by up_vector (up_vector.dot(x) > 0)
        """
        while 1:
            point = Point.spherical_random(length)
            if up_vector.dot(point) > 0:
                return point

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
        """ returns length as a length of vector """
        if self._length is None:
            self._length = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return self._length

    def copy(self):
        """ copies points """
        p = Point(self.x, self.y, self.z)
        p._length = self._length
        return p

    def normalize(self):
        """ normalize and return new value """
        self.x /= self.length()
        self.y /= self.length()
        self.z /= self.length()
        self._length = 1.0
        return self

    def normalized(self):
        """ return normalized value """
        return self.copy().normalize()

    def dot(self, other):
        """ dot operation between two points """
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise NotImplementedError()

    def cosine_to(self, other):
        """ returns cosine between self and other """
        if isinstance(other, Point):
            return self.dot(other)/(self.length() * other.length())
        else:
            raise NotImplementedError()

    def cross(self, other):
        """ cross operation between point self and other """
        if isinstance(other, Point):
            return Point(self.y * other.z - self.z * other.y,
                         self.z * other.x - self.x * other.z,
                         self.x * other.y - self.y * other.x)
        else:
            raise NotImplementedError()

    def rotate(self, angle, axis):
        """ 
            returns rotated vector 
            angle in degrees
        """
        e = axis.normalized()
        angle = np.deg2rad(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return e * self.dot(e)*(1-cos_a) + self.cross(e)*sin_a + self.copy()*cos_a