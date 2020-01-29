'''
Created on 2013-10-4

@author: Jesse MENG
'''
import pyglet
from math import fabs


class Motion(object):
    def __init__(self, obj):
        super(Motion, self).__init__()
        self.obj = obj

    def update(self, dt):
        step = self.time / dt * 1.0
        self.obj.w += self.w / step
        self.cnt_w += self.w / step
        self.obj.h += self.h / step
        self.cnt_h += self.h / step
        if fabs(self.cnt_w) > fabs(self.w) and fabs(self.cnt_h) > fabs(self.h):
            pyglet.clock.unschedule(self.update)

    def expand(self, w, h, time):
        self.old_w, self.old_h = self.obj.w, self.obj.h
        self.cnt_w, self.cnt_h = 0, 0
        self.w, self.h, self.time = w, h, time
        pyglet.clock.schedule_interval(self.update, 1 / 40.0)


class Box(object):
    def __init__(self, x=0, y=0, w=1, h=1, wnd=None):
        super(Box, self).__init__()
        assert wnd != None
        wnd.push_handlers(self.on_draw, self.on_mouse_press)
        self.window = wnd
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.x, self.y, self.w, self.h = x, y, w, h
        self.m = Motion(self)

    def on_draw(self):
        self.window.clear()
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_QUAD_STRIP,
                                     [0, 1, 2, 3], ('v2f', (self.x, self.y,
                                                            self.x + self.w, self.y,
                                                            self.x, self.y + self.h,
                                                            self.x + self.w, self.y + self.h)),
                                     ('c3B', (0, 0, 255,
                                              0, 255, 0,
                                              255, 0, 0,
                                              255, 255, 255)))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.m.expand(100, 100, 3)
        else:
            self.m.expand(-100, -100, 3)
        return True


window = pyglet.window.Window(480, 640)
box = Box(0, 0, 20, 20, window)
pyglet.app.run()