#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>

"""
  Ported from javascript via chrome experiments. Doesn't scale too well right now, heh

  Super Simple Particle System
  Eric Ishii Eckhardt for Adapted
  http://adaptedstudio.com
"""


import gtk
from lib import graphics
from random import random
import collections


class Particle(object):
    def __init__(self, x, y):
        self.x, self.y = x, y


        self.prev_x, self.prev_y = x, y

        self.speed_mod_x = random() * 20 + 8
        self.speed_mod_y = random() * 20 + 8
        self.speed_mod_target_x = random() * 3 + 2
        self.speed_mod_target_y = random() * 3 + 2

        self.max_speed = random() * 20 + 5

        self.speed_x, self.speed_y = 0, 0

    def update(self, mouse_x, mouse_y):


        target_speed_x = (mouse_x - self.x) / self.speed_mod_target_x
        target_speed_y = (mouse_y - self.y) / self.speed_mod_target_y

        if abs(self.speed_x) > self.max_speed:
            if self.speed_x < 0:
                self.speed_x = -self.max_speed
            else:
                self.speed_x = self.max_speed

        if abs(self.speed_y) > self.max_speed:
            if self.speed_y < 0:
                self.speed_y = -self.max_speed
            else:
                self.speed_y = self.max_speed


        self.speed_x = self.speed_x + (target_speed_x - self.speed_x) / self.speed_mod_x
        self.speed_y = self.speed_y + (target_speed_y - self.speed_y) / self.speed_mod_y

        self.prev_x = self.x
        self.prev_y = self.y

        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y



class Scene(graphics.Scene):
    def __init__(self):
        graphics.Scene.__init__(self)

        self.connect("on-enter-frame", self.on_enter_frame)
        self.connect("mouse-move", self.on_mouse_move)
        self.particles = []
        self.mouse_x, self.mouse_y = 0, 0
        self.paths = collections.deque()

    def on_mouse_move(self, scene, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def on_enter_frame(self, scene, context):
        g = graphics.Graphics(context)

        if not self.particles:
            for i in range(30):
                self.particles.append(Particle(random() * self.width, random() * self.height))


        for i, path in enumerate(self.paths):
            context.append_path(path)
            g.set_color("#333", i / float(len(self.paths)))
            context.stroke()

        for particle in self.particles:
            particle.update(self.mouse_x, self.mouse_y)
            g.move_to(particle.prev_x, particle.prev_y)
            g.line_to(particle.x, particle.y)

        self.paths.append(context.copy_path())
        if len(self.paths) > 50:
            self.paths.popleft()

        g.set_color("#333")
        g.stroke()

        self.redraw_canvas()




class BasicWindow:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(600, 500)
        window.connect("delete_event", lambda *args: gtk.main_quit())
        window.add(Scene())
        window.show_all()

example = BasicWindow()
gtk.main()
