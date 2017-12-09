#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from terminal_render.renderer import ConsoleRenderer
from terminal_render.scene import Scene
from terminal_render.camera import Camera
from terminal_render.geometry import Point
from terminal_render.objects import Light, Box
from terminal_render.material import SevenColorsMaterial


def initialize_scene():
    s = Scene()
    camera = Camera(Point(-3.5,0,1), Point(0,0,0), 30)
    light = Light(Point(-1, 1, 1))
    outer_box = Box(Point(-2.5,0,2), 10, 3, 5)
    inner_box = Box(Point(0,0,0), 1, 1, 1)
    inner_box.rotate(30, Point(0,0,1))
    outer_box.set_material(SevenColorsMaterial(1))
    inner_box.set_material(SevenColorsMaterial(2))
    s.add_objects(camera, light, outer_box, inner_box)
    return s


def main():
    scene = initialize_scene()
    r = ConsoleRenderer()
    r.render(scene)


if __name__ == "__main__":
    main()
    # c = '\xfa\xb1\xb2\xdb'
    # print c, [c.decode('cp866')]