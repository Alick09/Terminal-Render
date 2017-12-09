#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
<Project description>
Created 08.12.2017 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""


import locale
import curses 
import numpy as np
from ..material import SevenColorsMaterial
from abstract_renderer import Renderer
from ray_cast import RayCaster
import sys


class Line(object):
        def __init__(self):
            self.x, self.y, self.cc = None, None, None
            self.s = ""

        def get(self):
            return self.y, self.x, self.s, curses.color_pair(self.cc)

        def set(self, x, y, symb, cc):
            self.x, self.y = x, y
            self.cc = cc
            self.s = symb

        def update(self, x, y, symb, cc):
            if self.cc is not None and (cc != self.cc or x == 0):
                what_to_return = self.get()
                self.set(x, y, symb, cc)
                return what_to_return

            if self.cc is None:
                self.set(x, y, symb, cc)
            else:
                self.s += symb


class TerminalSymbolsCollection(object):
    def __init__(self):
        self.symbols = u'\xb7#\u2592\u2593\u2588';
        self.size = len(self.symbols)

    def get_symbol(self, darkness):
        index = min(int(darkness * self.size), self.size-1)
        return self.symbols[index].encode(sys.stdout.encoding)


class ConsoleRenderer(Renderer):
    def __init__(self):
        self.term_symbols = TerminalSymbolsCollection()
        locale.setlocale(locale.LC_ALL, '')
        self.screen = curses.initscr()
        curses.curs_set(0) 
        curses.start_color()
        self.screen.keypad(1) 
        self.initialize_colors()
        self.height, self.width = self.screen.getmaxyx()

    def render(self, scene, camera_index = -1):
        self.rc = RayCaster(scene, self.width, self.height, fix_coeff=1.9, antialiasing_level=1)
        Renderer.render(self, scene, camera_index)

    def initialize_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def transform(self, mat, dark):
        if not isinstance(mat, SevenColorsMaterial):
            raise AttributeError("ConsoleRenderer can render only SevenColorsMaterial")
        if mat.color == 0:
            return ' ', 7
        return self.term_symbols.get_symbol(dark), mat.color

    def get_cell(self, cells):
        ray, cell = cells[0]
        darkness = 1.0
        if cell is None:
            cell = (None, None, SevenColorsMaterial(0))
        else:
            darkness = self.rc.cast_lights(cell[0], cell[1])
        return self.transform(cell[2], darkness)

    def update(self, first_frame=False):
        self.line = Line()
        step = 1./(self.width + 1)
        fix_coeff = 1.9
        hmax = self.height * step * fix_coeff

        for y in xrange(self.height-1):
            for x in xrange(self.width):
                cells = [(r, self.scene.intersect(r)) for r in self.rc.get_pixel_rays(x, y)]
                symb, cc = self.get_cell(cells)
                res = self.line.update(x, y, symb, cc)
                # if cell[0].x < 0 and cell[0].z > -2:
                #     open('test.txt', 'a').write(str(cell[0]) + '\n')

                if res is not None:
                    self.screen.addstr(*res)
                    
        self.screen.addstr(*self.line.get())
        self.screen.refresh()
