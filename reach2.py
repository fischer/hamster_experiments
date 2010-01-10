#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>

"""
 * Reach 2. 
 * Based on code from Keith Peters (www.bit-101.com). 
 * 
 * The arm follows the position of the mouse by
 * calculating the angles with atan2(). 
 *
 Ported from processing (http://processing.org/) examples.
"""
 
import math
import gtk
from lib import graphics

SEGMENT_LENGTH = 25

class Segment(object):
    def __init__(self, x, y, color, width):
        self.x = x
        self.y = y
        self.angle = 1
        self.color = color
        self.width = width
    
    def draw(self, area):
        area.set_color(self.color)

        area.draw_rect(self.x - 5, self.y - 5, 10, 10, 3)
        area.context.fill()
        
        area.context.set_line_width(self.width)
        area.context.move_to(self.x, self.y)
        area.context.line_to(self.x + math.cos(self.angle) * SEGMENT_LENGTH,
                             self.y + math.sin(self.angle) * SEGMENT_LENGTH)
        area.context.stroke()
            
    def drag(self, x, y):
        # moves segment towards x, y, keeping the original angle and preset length
        dx = x - self.x
        dy = y - self.y
        
        self.angle = math.atan2(dy, dx)
        
        self.x = x - math.cos(self.angle) * SEGMENT_LENGTH
        self.y = y - math.sin(self.angle) * SEGMENT_LENGTH
        

class Canvas(graphics.Area):
    def __init__(self):
        graphics.Area.__init__(self)
        
        
        self.segments = []

        parts = 20
        for i in range(parts):
            self.segments.append(Segment(0, 0, "#666666", i))
            
        self.connect("mouse-move", self.on_mouse_move)        


    def on_mouse_move(self, area, coords):
        x, y = coords

        def get_angle(segment, x, y):
            dx = x - segment.x
            dy = y - segment.y
            return math.atan2(dy, dx)
        
        # point each segment to it's predecessor
        for segment in self.segments:
            angle = get_angle(segment, x, y)
            segment.angle = angle

            x = x - math.cos(angle) * SEGMENT_LENGTH
            y = y - math.sin(angle) * SEGMENT_LENGTH

        # and now move the pointed nodes, starting from the last one
        # (that is the beginning of the arm)
        for prev, segment in reversed(list(zip(self.segments, self.segments[1:]))):
            prev.x = segment.x + math.cos(segment.angle) * SEGMENT_LENGTH
            prev.y = segment.y + math.sin(segment.angle) * SEGMENT_LENGTH
            

        self.redraw_canvas()

    def on_expose(self):
        self.segments[-1].y = self.height
        
        # on expose is called when we are ready to draw
        for segment in self.segments:
            segment.draw(self)


class BasicWindow:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Graphics Module")
        window.set_size_request(600, 400)
        window.connect("delete_event", lambda *args: gtk.main_quit())
    
        canvas = Canvas()
        
        box = gtk.VBox()
        box.pack_start(canvas)
        
    
        window.add(box)
        window.show_all()
        
        
if __name__ == "__main__":
    example = BasicWindow()
    gtk.main()
