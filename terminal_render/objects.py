#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from geometry import Point, Rectangle

class Light(object):
    def __init__(self, position, force=1.0):
        self.position = position
        self.force = force


class Object(object):
    def __init__(self):
        pass

    def intersect(self, ray):
        """ 
            Must return None if not intersect 
            and tuple(P, N, M) otherwise
            where P - is a point of intersection
                  N - normal to this point
                  M - material on this point
        """
        raise NotImplementedError



class Box(Object):
    def __init__(self, center, width, height, depth):
        self.material = None
        self.center = center
        self.rects = [
            Rectangle(center - Point(width/2., 0, 0), height, depth, Point(0,0,1), Point(-1,0,0)),
            Rectangle(center + Point(width/2., 0, 0), height, depth, Point(0,0,1), Point(1,0,0)),
            Rectangle(center - Point(0, height/2., 0), width, depth, Point(0,0,1), Point(0,-1,0)),
            Rectangle(center + Point(0, height/2., 0), width, depth, Point(0,0,1), Point(0,1,0)),
            Rectangle(center - Point(0, 0, depth/2.), width, height, Point(0,1,0), Point(0,0,-1)),
            Rectangle(center + Point(0, 0, depth/2.), width, height, Point(0,1,0), Point(0,0,1)),
        ]

    def rotate(self, angle, rot_axis, center=None):
        if center is None:
            center = self.center
        [x.rotate(angle, rot_axis, center) for x in self.rects]

    def set_material(self, mat):
        self.material = mat

    def intersect(self, ray):
        points = filter(None, [x.intersect(ray) for x in self.rects])
        best = ray.get_closest_index([x[0] for x in points])
        if best is None:
            return None
        point, normal = points[best]
        return point, normal, self.material