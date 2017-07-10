
import pygame as pg
from OpenGL.GL import *

from .box import Box

class MainWindow:

    def __init__(self, app):
        self.app = app
        self.box = Box()

    def mouse_move(self, xp, yp):
        #self.app.repaint()
        pass

    def mouse_down(self): 
        pass


    def mouse_up(self): 
        pass

    def key_down(self, key):
        pass


    def draw(self):

        self.box.draw()



