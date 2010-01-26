#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>
"""
    Draws initial canvas to play flood filling on (based on truchet.py).
    Then on mouse click performs queue-based flood fill.
    We are combining cairo with gdk.Image here to operate on pixel level (yay!)
"""

import gtk
from lib import graphics
import math
import random


class Canvas(graphics.Area):
    def __init__(self):
        graphics.Area.__init__(self)
        self.connect("mouse-move", self.on_mouse_move)
        self.connect("mouse-click", self.on_mouse_click)
        self.tile_size = 60
        self.image = None


    def on_mouse_move(self, area, coords, mouse_areas):
        #self.tile_size = int(coords[0] / float(self.width) * 200 + 5) # x changes size of tile from 20 to 200(+20)
        #self.tile_size = min([max(self.tile_size, 10), self.width, self.height])
        self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SPRAYCAN))

    def on_mouse_click(self, area, coords, mouse_areas):
        x, y = coords

        colormap = self.image.get_colormap()
        color1 = colormap.alloc_color(self.colors.gdk("#ff0000"))

        self.flood_fill(self.image, x, y, color1.pixel)
        self.redraw_canvas()


    def stroke_tile(self, x, y, size, orient):
        # draws a tile, there are just two orientations
        arc_radius = size / 2
        x2, y2 = x + size, y + size

        # i got lost here with all the Pi's
        if orient == 1:
            self.context.move_to(x + arc_radius, y)
            self.context.arc(x, y, arc_radius, 0, math.pi / 2);

            self.context.move_to(x2 - arc_radius, y2)
            self.context.arc(x2, y2, arc_radius, math.pi, math.pi + math.pi / 2);
        elif orient == 2:
            self.context.move_to(x2, y + arc_radius)
            self.context.arc(x2, y, arc_radius, math.pi - math.pi / 2, math.pi);

            self.context.move_to(x, y2 - arc_radius)
            self.context.arc(x, y2, arc_radius, math.pi + math.pi / 2, 0);

    def on_expose(self):
        """here happens all the drawing"""
        if not self.height: return

        if not self.image:
            self.two_tile_random()
        else:
            self.window.draw_image(self.get_style().black_gc, self.image, 0, 0, 0, 0, -1, -1)

        self.image = self.window.get_image(0, 0, self.width, self.height)


    def two_tile_random(self):
        """stroke area with non-filed truchet (since non filed, all match and
           there are just two types"""
        self.set_color("#000")
        self.context.set_line_width(1)

        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                self.stroke_tile(x, y, self.tile_size, random.choice([1, 2]))
        self.context.stroke()

    def flood_fill(self, image, x, y, new_color, old_color = None):
        """whoa, a queue based 4-direction bucket fill
           linescan could improve things
        """
        x, y = int(x), int(y)
        old_color = old_color or image.get_pixel(x, y)

        queue = [(x,y)]

        operations = 0
        while queue:
            x, y = queue.pop(0)
            if image.get_pixel(x, y) == new_color:
                operations += 1

            current_color = image.get_pixel(x, y)
            if current_color!= new_color and abs(current_color - old_color) < 3000000:
                image.put_pixel(x, y, new_color)
                if x-1 > 0 and image.get_pixel(x-1, y) != new_color: queue.append((x - 1, y))
                if x+1 < self.width and image.get_pixel(x+1, y) != new_color: queue.append((x + 1, y))
                if y-1 > 0 and image.get_pixel(x, y-1) != new_color: queue.append((x, y - 1))
                if y+1 < self.height and image.get_pixel(x, y+1) != new_color: queue.append((x, y + 1))
        print operations, "operations on fill"


class BasicWindow:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(500, 500)
        window.connect("delete_event", lambda *args: gtk.main_quit())

        canvas = Canvas()

        box = gtk.VBox()
        box.pack_start(canvas)


        window.add(box)
        window.show_all()


if __name__ == "__main__":
    example = BasicWindow()
    gtk.main()