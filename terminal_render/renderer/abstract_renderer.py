#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 08.12.2017 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""


import numpy as np


class Renderer(object):
    def __init__(self):
        self.antialiasing_level = 2

    def render(self, scene, camera_index = -1):
        self.scene = scene
        self.camera = scene.get_camera(camera_index)
        self.update(True)

    def update(self, first_frame=False):
        """ only one method need to implement """
        raise NotImplementedError()

    def switch_camera(self, new_camera_index):
        self.camera = self.scene.get_camera(new_camera_index)
        self.update()