#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 08.12.17 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from ag_render.renderer import ConsoleRenderer
from ag_render.scene import Scene
from ag_render.camera import Camera
from ag_render.geometry import Point
from ag_render.objects import Light, Box
from ag_render.material import SevenColorsMaterial


def initialize_scene():
    s = Scene()
    camera = Camera(Point(-2.5,0,1), Point(0,0,0), 30)
    light = Light(Point(-1, 1, 1))
    outer_box = Box(Point(-0.5,0,0), 5, 5, 5)
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