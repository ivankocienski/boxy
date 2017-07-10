
import pygame as pg
from OpenGL.GL import *

from .box import Box

class Cursor:
    def __init__(self, spacing, app):
        self.spacing = spacing
        self.app = app
        self.step_x = 0
        self.step_y = 0
        self.real_x = 0
        self.real_y = 0

    def move(self, to_x, to_y):
        self.real_x = to_x
        self.real_y = to_y

        new_x = int((self.real_x + self.spacing * 0.5) / self.spacing) * self.spacing
        new_y = int((self.real_y + self.spacing * 0.5) / self.spacing) * self.spacing

        if new_x != self.step_x:
            self.app.repaint()
            self.step_x = new_x

        if new_y != self.step_y:
            self.app.repaint()
            self.step_y = new_y

    def draw(self):
        x1 = self.step_x - 2
        y1 = self.step_y - 2
        x2 = x1 + 4
        y2 = y1 + 4
  
        glColor3f(0.7, 0.7, 1)
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()

    
class MainWindow:

    def __init__(self, app):
        self.app = app
        self.box = Box()
        self.cursor = Cursor(20, app)
        self.in_plot = False

        print("Press Q to quit")
        print("Move mouse about. Press SPACE-BAR to start / end plotting of box")

    def mouse_move(self, xp, yp):
        self.cursor.move(xp, yp)
        if self.in_plot:
            self.box.set_size_from(self.cursor.step_x, self.cursor.step_y)
            self.app.repaint()

        #self.app.repaint()
        pass

    def mouse_down(self, btn): 
        #print("mouse_down=%s" % btn)
        pass


    def mouse_up(self, btn): 
        #print("mouse_up=%s" % btn)
        pass

    def key_down(self, key):
        #print("key=%s" % key)
        if key == pg.K_q: 
            self.app.stop_loop()
            return

        if key == pg.K_SPACE:
            if self.in_plot:
                self.in_plot = False
                self.box.set_size_from(self.cursor.step_x, self.cursor.step_y)
                self.app.repaint()

            else:
                self.in_plot = True 
                self.box.set_pos_from(self.cursor.step_x, self.cursor.step_y)
                self.app.repaint()
                
            pass


    def draw(self):

        self.box.draw()
        self.cursor.draw()


