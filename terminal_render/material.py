#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Materials
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""



class Material(object):
    def __init__(self):
        pass

    
class SevenColorsMaterial(Material):
    def __init__(self, color=7):
        self.color = color

    def __repr__(self):
        return '<Mat7C:{}>'.format(self.color)

